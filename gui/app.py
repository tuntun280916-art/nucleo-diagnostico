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


from citas.registro import RegistroCita
from citas.consultas import ConsultasCita

class AppSistema(
    Login,
    Dashboard,
    RegistroEmpleado,
    ConsultasEmpleado,
    RegistroMedico,
    ConsultasMedico,
    RegistroPaciente,
    ConsultasPaciente,
    RegistroCita,
    ConsultasCita,
    tk.Tk
):

    def __init__(self):

        super().__init__()

        self.title("Núcleo de Diagnóstico - Sistema de Gestión")
        self.geometry("1050x450")
        self.config(bg=BG_COLOR)
        self.minsize(950, 400)
        self.resizable(True, True)

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


        self.unbind_all("<MouseWheel>")

        for widget in self.main_container.winfo_children():
            widget.destroy()

    def crear_area_desplazable(self, padx=60, pady=35):

        canvas = tk.Canvas(
            self.main_container,
            bg=BG_COLOR,
            highlightthickness=0
        )
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(
            self.main_container,
            orient="vertical",
            command=canvas.yview
        )
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        contenedor = tk.Frame(canvas, bg=BG_COLOR)

        ventana = canvas.create_window(
            (0, 0),
            window=contenedor,
            anchor="nw"
        )

        def actualizar_area(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        contenedor.bind("<Configure>", actualizar_area)

        def ajustar_ancho(event):
            canvas.itemconfigure(ventana, width=event.width)

        canvas.bind("<Configure>", ajustar_ancho)

        def mover_rueda(event):
            if canvas.winfo_exists() and event.delta:
                direccion = -1 if event.delta > 0 else 1
                canvas.yview_scroll(direccion * 3, "units")

        self.bind_all("<MouseWheel>", mover_rueda)

        content = tk.Frame(contenedor, bg=BG_COLOR)
        content.pack(
            fill="both",
            expand=True,
            padx=padx,
            pady=pady
        )

        return content

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