import os

class Config:
    # --- MySQL (Estructura y Roles) ---
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://LAPLANTA:root@localhost/salon_belleza'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SECRET_KEY = os.urandom(24)
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECURITY_PASSWORD_SALT = 'beauty_glam_salt_123'
    
    # Tiempo de sesión (A08/A10: Máximo 10 minutos)
    PERMANENT_SESSION_LIFETIME = 600 
    SECURITY_TOKEN_MAX_AGE = 600
    
    # --- MongoDB (Bitácora Masiva) ---
    MONGO_URI = "mongodb://localhost:27017/salon_belleza_logs"
    
    # --- Flask (Configuración de la Aplicación) ---
    DEBUG = True
    TESTING = False