import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST", "")
USER = os.getenv("DB_USER", "")
PASSWORD = os.getenv("PASSWORD", "")
DATABASE = os.getenv("DATABASE", "")
PORT = os.getenv("PORT", "")


def connect_db():

    """Asigna los parámetros de conexión a la base de datos

    Returns:
        CMySQLConnection: Objeto conector a la base de datos.
    """

    db_connector = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE,
        port=PORT
    )

    return db_connector
