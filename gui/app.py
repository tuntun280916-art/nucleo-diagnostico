import os
import tkinter as tk
from PIL import Image, ImageTk

from gui.estilos import BG_COLOR
from gui.login import Login
from gui.dashboard import Dashboard

from empleados.registro import RegistroEmpleado
from empleados.consultas import ConsultasEmpleado

from medicos.registro import RegistroMedico
from medicos.consultas import ConsultasMedico

from pacientes.registro import RegistroPaciente
from pacientes.consultas import ConsultasPaciente


class AppSistema(
    Login,
    Dashboard,
    RegistroEmpleado,
    ConsultasEmpleado,
    RegistroMedico,
    ConsultasMedico,
    RegistroPaciente,
    ConsultasPaciente,
    tk.Tk
):

    def __init__(self):

        super().__init__()

        self.title("Núcleo de Diagnóstico - Sistema de Gestión")
        self.geometry("1920x1080")
        self.config(bg=BG_COLOR)
        self.minsize(950, 650)

        self.rol_actual = None
        self.empleado_actual = None

        self.main_container = tk.Frame(
            self,
            bg=BG_COLOR
        )
        self.main_container.pack(
            fill="both",
            expand=True
        )

        self.mostrar_login()

    def limpiar_contenedor(self):

        for widget in self.main_container.winfo_children():
            widget.destroy()

    def cargar_imagen(self, ruta, ancho, alto):

        if os.path.exists(ruta):

            try:
                imagen = Image.open(ruta).resize(
                    (ancho, alto),
                    Image.Resampling.LANCZOS
                )

                return ImageTk.PhotoImage(imagen)

            except Exception:
                return None

        return None