import random
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from models import db, Usuario
from datetime import datetime

# ELIMINAMOS: from app import bitacora_mongo de aquí arriba

acceso_bp = Blueprint('acceso', __name__, url_prefix='/seguridad')

def registrar_bitacora(usuario, accion, resultado):
    # IMPORTACIÓN LOCAL (Truco para evitar error circular)
    from app import bitacora_mongo 
    
    log = {
        "usuario": usuario,
        "accion": accion,
        "resultado": resultado,
        "ip": request.remote_addr,
        "fecha": datetime.now(),
        "navegador": request.user_agent.string
    }
    bitacora_mongo.insert_one(log)

@acceso_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        captcha_usuario = request.form.get('captcha_res')
        captcha_real = session.get('captcha_total')

        if not captcha_usuario or int(captcha_usuario) != captcha_real:
            flash('Captcha incorrecto. Demuestra que eres humano.', 'warning')
            return redirect(url_for('acceso.login'))

        username = request.form.get('nombre_usuario')
        password = request.form.get('contrasenia')
        
        user = Usuario.query.filter_by(nombre_usuario=username).first()

        if user and user.bloqueado:
            registrar_bitacora(username, "Login", "BLOQUEADO")
            flash('Cuenta bloqueada por seguridad tras 3 intentos fallidos.', 'danger')
            return redirect(url_for('acceso.login'))

        if not user or not check_password_hash(user.contrasenia, password):
            if user:
                user.intentos_fallidos += 1
                if user.intentos_fallidos >= 3:
                    user.bloqueado = True
                db.session.commit()
            
            registrar_bitacora(username, "Login", "FALLIDO")
            flash('Usuario o contraseña incorrectos.', 'danger')
            return redirect(url_for('acceso.login'))

        user.intentos_fallidos = 0
        user.ultimo_acceso = datetime.now()
        db.session.commit()
        
        login_user(user)
        registrar_bitacora(username, "Login", "EXITOSO")
        
        return redirect(url_for('index'))

    n1 = random.randint(1, 9)
    n2 = random.randint(1, 9)
    session['captcha_total'] = n1 + n2
    
    return render_template('security/login.html', n1=n1, n2=n2)

@acceso_bp.route('/logout')
@login_required
def logout():
    registrar_bitacora(current_user.nombre_usuario, "Logout", "EXITOSO")
    logout_user()
    return redirect(url_for('acceso.login'))

@acceso_bp.route('/auditoria')
@login_required
def ver_auditoria():
    from app import bitacora_mongo # También aquí
    if current_user.id_rol != 1:
        flash("No tienes permisos para ver la bitácora.", "danger")
        return redirect(url_for('index'))
    
    logs = bitacora_mongo.find().sort("fecha", -1).limit(50)
    return render_template('security/auditoria.html', logs=logs)