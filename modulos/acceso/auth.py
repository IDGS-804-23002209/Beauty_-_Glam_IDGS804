@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()

    # 1. Verificar si está bloqueado (A08/A09)
    if user and user.bloqueado:
        registrar_auditoria(email, "Intento en cuenta bloqueada", "Denegado")
        flash('Tu cuenta está bloqueada por demasiados intentos fallidos.', 'danger')
        return redirect(url_for('auth.login'))

    # 2. Validar contraseña
    if not user or not check_password_hash(user.password, password):
        if user:
            user.intentos_fallidos += 1
            if user.intentos_fallidos >= 3:
                user.bloqueado = True
            db.session.commit()
        
        registrar_auditoria(email, "Fallo de Login", "Fallido")
        flash('Email y/o contraseña incorrectos.', 'danger')
        return redirect(url_for('auth.login'))

    # 3. Login Exitoso
    user.intentos_fallidos = 0 # Reiniciar contador
    user.ultimo_acceso = datetime.now()
    db.session.commit()
    
    login_user(user)
    registrar_auditoria(email, "Inicio de Sesión", "Exitoso")
    
    return redirect(url_for('main.profile'))

@auth.route('/auditoria')
@roles_required('admin') # Solo Jimena/Admin entra aquí
def ver_auditoria():
    # Consultamos los últimos 50 registros de MongoDB
    # logs = bitacora_db.bitacora.find().sort("fecha", -1).limit(50)
    return render_template('security/auditoria.html', logs=[]) # Aquí pasas los logs de Mongo

 @auth.route('/logout')
@login_required