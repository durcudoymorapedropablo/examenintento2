from datetime import date
from functools import wraps

from flask import (
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for
)

from flask_app import app
from flask_app.models.tarea import Tarea


# ==========================
# PROTEGER RUTAS
# ==========================

def login_required(view):

    @wraps(view)
    def wrapped(*args, **kwargs):

        if "usuario_id" not in session:

            flash(
                "Debes haber iniciado sesión para acceder a esta página.",
                "error"
            )

            return redirect(
                url_for("index")
            )

        return view(*args, **kwargs)

    return wrapped


# ==========================
# VALIDAR TAREA
# ==========================

def validar_tarea(
    nombre,
    fecha_entrega,
    descripcion
):

    errores = []

    if not nombre.strip():

        errores.append(
            "El nombre de la tarea no puede estar vacío."
        )

    if not fecha_entrega:

        errores.append(
            "La fecha de entrega es obligatoria."
        )

    else:

        try:

            if date.fromisoformat(
                fecha_entrega
            ) < date.today():

                errores.append(
                    "No puedes ingresar una fecha en el pasado."
                )

        except ValueError:

            errores.append(
                "La fecha de entrega no es válida."
            )

    if not descripcion.strip():

        errores.append(
            "La descripción no puede estar vacía."
        )

    return errores


# ==========================
# PÁGINA PRINCIPAL
# ==========================

@app.route("/dashboard")
@login_required
def dashboard():

    tareas = Tarea.obtener_por_usuario(
        session["usuario_id"]
    )

    return render_template(
        "dashboard.html",
        tareas=tareas,
        tareas_pendientes=[
            t for t in tareas
            if not t["completada"]
        ],
        tareas_completadas=[
            t for t in tareas
            if t["completada"]
        ]
    )


# ==========================
# CREAR TAREA
# ==========================

@app.route(
    "/nueva",
    methods=["GET", "POST"]
)
@login_required
def nueva_tarea():

    if request.method == "POST":

        nombre = request.form.get(
            "nombre",
            ""
        )

        fecha_entrega = request.form.get(
            "fecha_entrega",
            ""
        )

        descripcion = request.form.get(
            "descripcion",
            ""
        )

        errores = validar_tarea(
            nombre,
            fecha_entrega,
            descripcion
        )

        if errores:

            for error in errores:
                flash(error, "error")

            return render_template(
                "nueva.html",
                form=request.form,
                today=date.today().isoformat()
            )

        Tarea.crear(
            session["usuario_id"],
            nombre.strip(),
            fecha_entrega,
            descripcion.strip()
        )

        flash(
            "Tarea creada correctamente.",
            "success"
        )

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "nueva.html",
        form={},
        today=date.today().isoformat()
    )


# ==========================
# EDITAR TAREA
# ==========================

@app.route(
    "/editar/<int:tarea_id>",
    methods=["GET", "POST"]
)
@login_required
def editar_tarea(tarea_id):

    usuario_id = session["usuario_id"]

    tarea = Tarea.obtener_por_id_usuario(
        tarea_id,
        usuario_id
    )

    if not tarea:

        flash(
            "No puedes editar tareas de otro usuario, "
            "aunque cambies manualmente la URL.",
            "error"
        )

        return redirect(
            url_for("dashboard")
        )

    if request.method == "POST":

        nombre = request.form.get(
            "nombre",
            ""
        )

        fecha_entrega = request.form.get(
            "fecha_entrega",
            ""
        )

        descripcion = request.form.get(
            "descripcion",
            ""
        )

        errores = validar_tarea(
            nombre,
            fecha_entrega,
            descripcion
        )

        if errores:

            for error in errores:
                flash(error, "error")

            return render_template(
                "editar.html",
                form=request.form,
                tarea=tarea,
                today=date.today().isoformat()
            )

        Tarea.actualizar(
            tarea_id,
            usuario_id,
            nombre.strip(),
            fecha_entrega,
            descripcion.strip()
        )

        flash(
            "Tarea actualizada correctamente.",
            "success"
        )

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "editar.html",
        form=tarea,
        tarea=tarea,
        today=date.today().isoformat()
    )


# ==========================
# BORRAR TAREA
# ==========================

@app.route(
    "/borrar/<int:tarea_id>",
    methods=["POST"]
)
@login_required
def borrar_tarea(tarea_id):

    resultado = Tarea.eliminar(
        tarea_id,
        session["usuario_id"]
    )

    if resultado == 1:

        flash(
            "Tarea eliminada correctamente.",
            "success"
        )

    else:

        flash(
            "No puedes eliminar una tarea de otro usuario.",
            "error"
        )

    return redirect(
        url_for("dashboard")
    )


# ==========================
# COMPLETAR TAREA
# ==========================

@app.route(
    "/completar/<int:tarea_id>",
    methods=["POST"]
)
@login_required
def completar_tarea(tarea_id):

    resultado = Tarea.completar(
        tarea_id,
        session["usuario_id"]
    )

    if resultado == 1:

        flash(
            "Tarea marcada como completada.",
            "success"
        )

    else:

        flash(
            "No puedes completar una tarea de otro usuario.",
            "error"
        )

    return redirect(
        url_for("dashboard")
    )


# ==========================
# VER TAREA
# ==========================

@app.route(
    "/ver/<int:tarea_id>"
)
@login_required
def ver_tarea(tarea_id):

    tarea = Tarea.obtener_por_id_usuario(
        tarea_id,
        session["usuario_id"]
    )

    if not tarea:

        flash(
            "No tienes permiso para ver esta tarea.",
            "error"
        )

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "ver.html",
        tarea=tarea
    )