
import tkinter as tk
from tkinter import messagebox, ttk

from config.conexion import conectar_bd
from gui.estilos import (
    BG_COLOR,
    CARD_BG,
    TEXT_MAIN
)


class ConsultasMedico:

    def mostrar_consultas_medico(self):
        self.limpiar_contenedor()
        self.crear_barra_superior(self.main_container)

        content = tk.Frame(
            self.main_container,
            bg=BG_COLOR
        )
        content.pack(
            fill="both",
            expand=True,
            padx=60,
            pady=35
        )

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
            text="Listado General de Médicos",
            font=("Segoe UI", 20, "bold"),
            bg=BG_COLOR,
            fg=TEXT_MAIN
        ).pack(anchor="w", pady=(0, 20))

        table_frame = tk.Frame(
            content,
            bg=CARD_BG
        )
        table_frame.pack(
            fill="both",
            expand=True
        )

        # ESTILO DE LA TABLA
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

        # COLUMNAS
        columnas = (
            "ID",
            "Nombre Completo",
            "Dirección",
            "Teléfono",
            "Fecha de Nacimiento",
            "Sexo",
            "Especialidad",
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
            tree.column(
                col,
                width=130,
                anchor="center"
            )

        # AJUSTE DE ANCHOS
        tree.column(
            "Nombre Completo",
            width=180,
            anchor="w"
        )

        tree.column(
            "Dirección",
            width=150,
            anchor="w"
        )

        tree.column(
            "Teléfono",
            width=120,
            anchor="center"
        )

        # BARRAS DE DESPLAZAMIENTO
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

        tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar_y.pack(
            side="right",
            fill="y"
        )

        scrollbar_x.pack(
            side="bottom",
            fill="x"
        )

        # CONSULTA A POSTGRESQL
        conexion = None
        cursor = None
        filas = []

        try:
            conexion = conectar_bd()

            if conexion is None:
                messagebox.showerror(
                    "Error de conexión",
                    "No se pudo conectar con la base de datos."
                )
                return

            cursor = conexion.cursor()

            cursor.execute("""
                SELECT *
                FROM public.medico
                ORDER BY id_medico;
            """)

            filas = cursor.fetchall()

            # INSERTAR LOS REGISTROS EN EL TREEVIEW
            for fila in filas:
                valores = (
                    fila[0],
                    fila[1],
                    fila[2],
                    fila[3],
                    fila[4],
                    fila[5],
                    fila[6],
                    fila[7]
                )

                tree.insert(
                    "",
                    "end",
                    values=valores
                )

            if not filas:
                messagebox.showinfo(
                    "Información",
                    "No hay médicos registrados."
                )

        except Exception as err:
            messagebox.showerror(
                "Error al consultar médicos",
                f"No se pudieron cargar los médicos:\n\n{err}"
            )

        finally:
            if cursor:
                cursor.close()

            if conexion:
                conexion.close()

