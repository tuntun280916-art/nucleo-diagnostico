import psycopg2
from tkinter import messagebox


def conectar_bd():
    """Abre la conexión con PostgreSQL usando las credenciales existentes."""
    try:
        return psycopg2.connect(
            host="localhost",
            database="nucleo_diagnostico",
            user="postgres",
            password="3601360159028Sa",
            port="5432"
        )
    except psycopg2.Error as error:
        messagebox.showerror(
            "Error de conexión",
            f"No se pudo conectar a PostgreSQL:\n{error}"
        )
        return None
