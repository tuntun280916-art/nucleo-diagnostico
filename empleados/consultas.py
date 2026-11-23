import tkinter as tk
from tkinter import messagebox, ttk

from config.conexion import conectar_bd
from gui.estilos import (
    BG_COLOR,
    CARD_BG,
    TEXT_MAIN
)


class ConsultasEmpleado:

    def mostrar_consultas_empleado(self):
        self.limpiar_contenedor()
        self.crear_barra_superior(self.main_container)

        content = tk.Frame(self.main_container, bg=BG_COLOR)
        content.pack(fill="both", expand=True, padx=60, pady=35)

        btn_volver = tk.Button(
            content,
            text="← Volver al Menú",
            font=("Segoe UI", 10, "bold"),
            bg="#e2e8f0",
            fg=TEXT_MAIN,
            relief="flat",
            cursor="hand2",
            command=self.mostrar_dashboard
        )
        btn_volver.pack(anchor="w", pady=(0, 20))

        tk.Label(
            content,
            text="Listado General de Empleados",
            font=("Segoe UI", 20, "bold"),
            bg=BG_COLOR,
            fg=TEXT_MAIN
        ).pack(anchor="w", pady=(0, 20))

        table_frame = tk.Frame(content, bg=CARD_BG)
        table_frame.pack(fill="both", expand=True)

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 11, "bold"),
            background="#e2e8f0",
            foreground=TEXT_MAIN
        )

        style.configure(
            "Treeview",
            font=("Segoe UI", 10),
            rowheight=32,
            background="white",
            fieldbackground="white"
        )

        columnas = (
            "ID",
            "Nombre",
            "Sexo",
            "Dirección",
            "Teléfono",
            "Fecha de Nacimiento",
            "Turno",
            "Salario",
            "Contraseña"
        )

        tree = ttk.Treeview(
            table_frame,
            columns=columnas,
            show="headings",
            height=14
        )

        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=110, anchor="center")

        tree.column("Nombre", width=180, anchor="w")
        tree.column("Dirección", width=150, anchor="w")
        tree.column("Teléfono", width=120, anchor="center")

        scrollbar_y = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=tree.yview
        )

        scrollbar_x = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=tree.xview
        )

        tree.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")

        conexion = None
        cursor = None

        try:
            conexion = conectar_bd()

            if conexion is None:
                return

            cursor = conexion.cursor()

            cursor.execute("""
                SELECT *
                FROM empleado   
                ORDER BY id_empleado;
            """)

            filas = cursor.fetchall()
            for fila in filas:
                valores = (
                    fila[0],
                    fila[1],
                    fila[2],
                    fila[3],
                    fila[4],
                    fila[5],
                    fila[6],
                    fila[7],
                    fila[8]
                    )
                tree.insert("", "end", values=valores)

        except Exception as err:
            messagebox.showerror(
                "Error al consultar empleados",
                f"No se pudieron cargar los empleados:\n\n{err}"
            )
            if not filas:
                messagebox.showinfo(
                    "Información",
                    "No hay empleados registrados."
                    )


        finally:
            if cursor:
                cursor.close()

            if conexion:
                conexion.close()
