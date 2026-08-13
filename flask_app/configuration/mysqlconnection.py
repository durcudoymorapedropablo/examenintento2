import os

import pymysql.cursors
from dotenv import load_dotenv


load_dotenv()


class MySQLConnection:
    def __init__(self, db):
        self.connection = pymysql.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            port=int(os.environ.get("DB_PORT", 3306)),
            user=os.environ.get("DB_USER", "root"),
            password=os.environ.get("DB_PASSWORD", ""),
            database=db,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )

    def query_db(self, query, data=None):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, data or {})

                operation = query.lstrip().split(None, 1)[0].lower()

                if operation == "insert":
                    return cursor.lastrowid

                if operation == "select":
                    return cursor.fetchall()

                return cursor.rowcount

        except Exception as e:
            print("Something went wrong:", e)
            return False

        finally:
            self.connection.close()


def connectToMySQL(db):
    return MySQLConnection(db)
