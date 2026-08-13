from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["SECRET_KEY"] = "cambia-esta-clave-en-produccion"

bcrypt = Bcrypt(app)

from flask_app.controllers import usuarios
from flask_app.controllers import tareas
