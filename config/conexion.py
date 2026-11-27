import psycopg2
from tkinter import messagebox


def conectar_bd():
    """Abre la conexión con PostgreSQL usando las credenciales existentes."""
    try:
        return psycopg2.connect(
            host="localhost",
            database="nucleo_diagnostico",
            user="postgres",
            password="1234",
            port="5432",
            client_encoding="WIN1252"
        )
    except psycopg2.Error as error:
        if getattr(error, "args", None) and len(error.args) > 1 and isinstance(error.args[1], bytes):
            detalle = error.args[1].decode("cp1252", errors="replace")
        else:
            detalle = repr(error)

        messagebox.showerror(
            "Error de conexión",
            f"No se pudo conectar a PostgreSQL:\n{detalle}"
        )
        return None