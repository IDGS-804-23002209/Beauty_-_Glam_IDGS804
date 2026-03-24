from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# 1. TABLAS BASE (Independientes)
# ---------------------------------------------------------------------
class Persona(db.Model):
    __tablename__ = 'persona'
    id_persona = db.Column(db.Integer, primary_key=True)
    nombre_persona = db.Column(db.String(50))
    apellidos = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    correo = db.Column(db.String(150))
    direccion = db.Column(db.String(255))
    
    # Relaciones
    usuarios = db.relationship('Usuario', backref='datos_personales', lazy=True)
    clientes = db.relationship('Cliente', backref='persona_cliente', lazy=True)
    empleados = db.relationship('Empleado', backref='persona_empleado', lazy=True)

class Rol(db.Model):
    __tablename__ = 'rol'
    id_rol = db.Column(db.Integer, primary_key=True)
    nombre_rol = db.Column(db.String(100))
    
    # Relación
    usuarios = db.relationship('Usuario', backref='rol_perfil', lazy=True)

class Categoria(db.Model):
    __tablename__ = 'categoria'
    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre_categoria = db.Column(db.String(100))
    servicios = db.relationship('Servicio', backref='categoria', lazy=True)

class Puesto(db.Model):
    __tablename__ = 'puesto'
    id_puesto = db.Column(db.Integer, primary_key=True)
    nombre_puesto = db.Column(db.String(100))
    empleados = db.relationship('Empleado', backref='puesto', lazy=True)

# 2. TABLAS DE USUARIO Y ACCESO (Tu Combo 1)
# ---------------------------------------------------------------------
class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(100), unique=True, nullable=False)
    contrasenia = db.Column(db.String(255), nullable=False)
    estatus = db.Column(db.Enum('ACTIVO', 'INACTIVO'), default='ACTIVO')
    ultimo_acceso = db.Column(db.DateTime)
    intentos_fallidos = db.Column(db.Integer, default=0)
    bloqueado = db.Column(db.Boolean, default=False)
    
    # Llaves Foráneas
    id_persona = db.Column(db.Integer, db.ForeignKey('persona.id_persona'))
    id_rol = db.Column(db.Integer, db.ForeignKey('rol.id_rol'))

    def get_id(self):
        return str(self.id_usuario)

# 3. TABLAS OPERATIVAS (Módulos de tus compañeros)
# ---------------------------------------------------------------------
class Cliente(db.Model):
    __tablename__ = 'cliente'
    id_cliente = db.Column(db.Integer, primary_key=True)
    estatus = db.Column(db.Enum('ACTIVO', 'INACTIVO'), default='ACTIVO')
    id_persona = db.Column(db.Integer, db.ForeignKey('persona.id_persona'))
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))

class Empleado(db.Model):
    __tablename__ = 'empleado'
    id_empleado = db.Column(db.Integer, primary_key=True)
    fecha_contratacion = db.Column(db.Date)
    estatus = db.Column(db.Enum('ACTIVO', 'INACTIVO'), default='ACTIVO')
    id_persona = db.Column(db.Integer, db.ForeignKey('persona.id_persona'))
    id_puesto = db.Column(db.Integer, db.ForeignKey('puesto.id_puesto'))
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))

class Servicio(db.Model):
    __tablename__ = 'servicio'
    id_servicio = db.Column(db.Integer, primary_key=True)
    nombre_servicio = db.Column(db.String(150))
    precio = db.Column(db.Numeric(10, 2))
    duracion_minutos = db.Column(db.Integer)
    estatus = db.Column(db.Enum('ACTIVO', 'INACTIVO'), default='ACTIVO')
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id_categoria'))

class Cita(db.Model):
    __tablename__ = 'cita'
    id_cita = db.Column(db.Integer, primary_key=True)
    fecha_hora = db.Column(db.DateTime)
    estatus = db.Column(db.Enum('PENDIENTE', 'CONFIRMADA', 'CANCELADA', 'FINALIZADA'), default='PENDIENTE')
    id_cliente = db.Column(db.Integer, db.ForeignKey('cliente.id_cliente'))
    id_empleado = db.Column(db.Integer, db.ForeignKey('empleado.id_empleado'))