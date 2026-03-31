from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect
from config import Config
from flask_migrate import Migrate
from models import db
# from pedidos.routes import pedidos
# from ventas.routes import ventas
from flask_security import login_required, current_user
from flask_login import LoginManager
from modulos.acceso.routes import acceso_bp
from models import Usuario

app = Flask(__name__)
app.config.from_object(Config)
login_manager = LoginManager()
login_manager.init_app(app)

# app.register_blueprint(pedidos)
# app.register_blueprint(ventas)
app.register_blueprint(acceso_bp) 

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

db.init_app(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route("/", methods=['GET'])
@app.route("/inicio")
# @login_required
def inicio():
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)