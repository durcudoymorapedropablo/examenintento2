import os

from flask import Flask
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "dev-secret-key-change-me"
)

bcrypt = Bcrypt(app)

from flask_app.controllers import usuarios
from flask_app.controllers import tareas
