from flask import Flask
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from . import mysql  # o según cómo lo importes
from config import Config  # Asegúrate de que config.py tenga la clase Config definida

login_manager = LoginManager()
login_manager.login_view = 'main.login'  # Ruta a la vista de login


def create_app():
    app = Flask(__name__)
    
    # Carga la configuración desde la clase Config
    app.config.from_object(Config)

    # Inicializa las extensiones
    mysql.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'main.login'  # Redirige a /login si no hay sesión

    # Importa y registra el Blueprint
    from .routes import main
    app.register_blueprint(main)

    return app


class Usuario(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Usuarios WHERE id = %s", (user_id,))
    user = cur.fetchone()
    if user:
        return Usuario(user[0], user[1], user[2])
    return None
