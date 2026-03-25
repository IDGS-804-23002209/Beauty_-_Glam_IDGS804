import os

class Config:
    # --- MySQL (Estructura y Roles) ---
<<<<<<< HEAD
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/salon_belleza1'
=======
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://LAPLANTA:LAPLANTA@localhost/salon_belleza'
>>>>>>> 9bafb839699e372c260aa01d80570e00c2aa041b
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SECRET_KEY = os.urandom(24)
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECURITY_PASSWORD_SALT = 'beauty_glam_salt_123'
    
    # Tiempo de sesión (A08/A10: Máximo 10 minutos)
    PERMANENT_SESSION_LIFETIME = 600 
    SECURITY_TOKEN_MAX_AGE = 600
    
    # --- MongoDB (Bitácora Masiva) ---
    MONGO_URI = "mongodb://localhost:27017/salon_belleza_logs"
<<<<<<< HEAD

    # 1. Conexión a MongoDB (Definida antes que los Blueprints)
client = MongoClient("mongodb://localhost:27017/")
mongo_db = client['salon_audit']
bitacora_mongo = mongo_db['logs_seguridad']
=======
    
    # --- Flask (Configuración de la Aplicación) ---
    DEBUG = True
    TESTING = False
>>>>>>> 9bafb839699e372c260aa01d80570e00c2aa041b
