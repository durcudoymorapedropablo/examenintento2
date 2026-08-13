from flask_app.configuration.mysqlconnection import connectToMySQL


class Tarea:

    @staticmethod
    def obtener_por_usuario(usuario_id):

        query = """
            SELECT id,
                   usuario_id,
                   nombre,
                   fecha_entrega,
                   descripcion,
                   completada,
                   fecha_completada
            FROM tareas
            WHERE usuario_id = %(usuario_id)s
            ORDER BY fecha_entrega ASC, id DESC
        """

        resultado = connectToMySQL("organitask").query_db(
            query,
            {
                "usuario_id": usuario_id
            }
        )

        if resultado:
            return resultado

        return []

    @staticmethod
    def obtener_por_id_usuario(tarea_id, usuario_id):

        query = """
            SELECT id,
                   usuario_id,
                   nombre,
                   fecha_entrega,
                   descripcion,
                   completada,
                   fecha_completada
            FROM tareas
            WHERE id = %(tarea_id)s
            AND usuario_id = %(usuario_id)s
        """

        resultado = connectToMySQL("organitask").query_db(
            query,
            {
                "tarea_id": tarea_id,
                "usuario_id": usuario_id
            }
        )

        if resultado:
            return resultado[0]

        return None

    @staticmethod
    def crear(usuario_id, nombre, fecha_entrega, descripcion):

        query = """
            INSERT INTO tareas
            (
                usuario_id,
                nombre,
                fecha_entrega,
                descripcion
            )
            VALUES
            (
                %(usuario_id)s,
                %(nombre)s,
                %(fecha_entrega)s,
                %(descripcion)s
            )
        """

        return connectToMySQL("organitask").query_db(
            query,
            {
                "usuario_id": usuario_id,
                "nombre": nombre,
                "fecha_entrega": fecha_entrega,
                "descripcion": descripcion
            }
        )

    @staticmethod
    def actualizar(
        tarea_id,
        usuario_id,
        nombre,
        fecha_entrega,
        descripcion
    ):

        query = """
            UPDATE tareas
            SET nombre = %(nombre)s,
                fecha_entrega = %(fecha_entrega)s,
                descripcion = %(descripcion)s
            WHERE id = %(tarea_id)s
            AND usuario_id = %(usuario_id)s
        """

        return connectToMySQL("organitask").query_db(
            query,
            {
                "tarea_id": tarea_id,
                "usuario_id": usuario_id,
                "nombre": nombre,
                "fecha_entrega": fecha_entrega,
                "descripcion": descripcion
            }
        )

    @staticmethod
    def eliminar(tarea_id, usuario_id):

        query = """
            DELETE FROM tareas
            WHERE id = %(tarea_id)s
            AND usuario_id = %(usuario_id)s
        """

        return connectToMySQL("organitask").query_db(
            query,
            {
                "tarea_id": tarea_id,
                "usuario_id": usuario_id
            }
        )

    @staticmethod
    def completar(tarea_id, usuario_id):

        query = """
            UPDATE tareas
            SET completada = 1,
                fecha_completada = CURDATE()
            WHERE id = %(tarea_id)s
            AND usuario_id = %(usuario_id)s
            AND completada = 0
        """

        return connectToMySQL("organitask").query_db(
            query,
            {
                "tarea_id": tarea_id,
                "usuario_id": usuario_id
            }
        )

