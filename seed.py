from app import app
from models import db, Usuario, Rol
from werkzeug.security import generate_password_hash

def run_seed():
    with app.app_context():
        # 1. Crear las tablas si no existen
        print("Verificando tablas en la base de datos...")
        db.create_all()

        # 2. Crear Roles básicos
        if not Rol.query.filter_by(nombre_rol='Admin').first():
            rol_admin = Rol(nombre_rol='Admin')
            rol_empleado = Rol(nombre_rol='Empleado')
            db.session.add_all([rol_admin, rol_empleado])
            db.session.commit()
            print("Roles 'Admin' y 'Empleado' creados.")

        # 3. Crear tu usuario administrador (Jimena)
        if not Usuario.query.filter_by(nombre_usuario='JimenaAdmin').first():
            # Contraseña segura encriptada
            password_encriptada = generate_password_hash("Admin123*", method='pbkdf2:sha256')
            
            admin_user = Usuario(
                nombre_usuario='JimenaAdmin',
                contrasenia=password_encriptada,
                id_rol=1, # El ID del rol Admin que acabamos de crear
                estatus='ACTIVO'
            )
            db.session.add(admin_user)
            db.session.commit()
            print("--- ÉXITO ---")
            print("Usuario: JimenaAdmin")
            print("Password: Admin123*")
        else:
            print("El usuario ya existe en la base de datos.")

if __name__ == "__main__":
    run_seed()