from flask import (
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for
)

from flask_app import app, bcrypt
from flask_app.models.usuario import Usuario


@app.route("/", methods=["GET", "POST"])
def index():

    if "usuario_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        accion = request.form.get("accion")

        # ==========================
        # REGISTRO
        # ==========================

        if accion == "registro":

            nombre = request.form.get("nombre", "").strip()
            apellido = request.form.get("apellido", "").strip()
            email = request.form.get("email", "").strip().lower()
            password = request.form.get("password", "")
            confirmacion = request.form.get(
                "confirm_password",
                ""
            )

            errores = []

            if len(nombre) < 2:
                errores.append(
                    "El nombre debe tener al menos 2 caracteres."
                )

            if len(apellido) < 2:
                errores.append(
                    "El apellido debe tener al menos 2 caracteres."
                )

            if (
                not email
                or "@" not in email
                or "." not in email.rsplit("@", 1)[-1]
            ):
                errores.append(
                    "El e-mail debe tener un formato válido."
                )

            if not password:
                errores.append(
                    "La contraseña es obligatoria."
                )

            if password != confirmacion:
                errores.append(
                    "Contraseña y confirmación deben ser iguales."
                )

            if not errores and Usuario.obtener_por_email(email):

                errores.append(
                    "El e-mail no puede repetirse en la BD."
                )

            if errores:

                for error in errores:
                    flash(error, "error")

                return render_template("index.html")

            # BCRYPT
            password_hash = bcrypt.generate_password_hash(
                password
            ).decode("utf-8")

            Usuario.crear(
                nombre,
                apellido,
                email,
                password_hash
            )

            flash(
                "Registro realizado correctamente.",
                "success"
            )

            return redirect(url_for("index"))

        # ==========================
        # LOGIN
        # ==========================

        if accion == "login":

            email = request.form.get(
                "login_email",
                ""
            ).strip().lower()

            password = request.form.get(
                "login_password",
                ""
            )

            if not email or not password:

                flash(
                    "El e-mail y la contraseña son obligatorios.",
                    "error"
                )

                return render_template("index.html")

            usuario = Usuario.obtener_por_email(email)

            if (
                usuario
                and bcrypt.check_password_hash(
                    usuario["password"],
                    password
                )
            ):

                session.clear()

                session["usuario_id"] = usuario["id"]
                session["nombre"] = usuario["nombre"]
                session["apellido"] = usuario["apellido"]

                return redirect(url_for("dashboard"))

            flash(
                "El e-mail debe estar registrado y "
                "la contraseña debe corresponder a la BD.",
                "error"
            )

    return render_template("index.html")


# ==========================
# CERRAR SESIÓN
# ==========================

@app.route("/logout")
def logout():

    session.clear()

    flash(
        "Sesión cerrada correctamente.",
        "success"
    )

    return redirect(url_for("index"))
