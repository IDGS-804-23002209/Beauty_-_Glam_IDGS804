import os
from flask import Flask, render_template
from flask_login import LoginManager
from pymongo import MongoClient
from models import db, Usuario

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/salon_belleza'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 1. Conexión a MongoDB (Definida antes que los Blueprints)
client = MongoClient("mongodb://localhost:27017/")
mongo_db = client['salon_audit']
bitacora_mongo = mongo_db['logs_seguridad']

# 2. Inicializar Extensiones
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'acceso.login'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# 3. Registro de Blueprints (AL FINAL para evitar errores circulares)
from modulos.acceso.routes import acceso_bp
app.register_blueprint(acceso_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)