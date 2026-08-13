from flask_app.configuration.mysqlconnection import connectToMySQL


class Usuario:

    @staticmethod
    def obtener_por_email(email):

        query = """
            SELECT id, nombre, apellido, email, password
            FROM usuarios
            WHERE email = %(email)s
        """

        resultado = connectToMySQL("organitask").query_db(
            query,
            {
                "email": email
            }
        )

        if resultado:
            return resultado[0]

        return None

    @staticmethod
    def crear(nombre, apellido, email, password_hash):

        query = """
            INSERT INTO usuarios
            (nombre, apellido, email, password)
            VALUES (
                %(nombre)s,
                %(apellido)s,
                %(email)s,
                %(password)s
            )
        """

        return connectToMySQL("organitask").query_db(
            query,
            {
                "nombre": nombre,
                "apellido": apellido,
                "email": email,
                "password": password_hash
            }
        )
