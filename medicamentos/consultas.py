import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2

from config.conexion import conectar_bd
from gui.estilos import BG_COLOR, CARD_BG, TEXT_MAIN


class ConsultasMedicamento:

    def mostrar_consultas_medicamento(self):
        self.limpiar_contenedor()
        self.crear_barra_superior(self.main_container)

        content = tk.Frame(self.main_container, bg=BG_COLOR)
        content.pack(fill="both", expand=True, padx=60, pady=35)

        tk.Button(
            content,
            text="← Volver al Menú",
            font=("Segoe UI", 10, "bold"),
            bg="#e2e8f0",
            fg=TEXT_MAIN,
            relief="flat",
            cursor="hand2",
            command=self.mostrar_dashboard
        ).pack(anchor="w", pady=(0, 15))

        tk.Label(
            content,
            text="Listado General de Medicamentos",
            font=("Segoe UI", 20, "bold"),
            bg=BG_COLOR,
            fg=TEXT_MAIN
        ).pack(anchor="w", pady=(0, 15))

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
            "NOMBRE",
            "VIA_ADMINISTRACION",
            "PRESENTACION",
            "FECHA_CADUCIDAD"
        )

        tree = ttk.Treeview(
            table_frame,
            columns=columnas,
            show="headings",
            height=13
        )

        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=180, anchor="center")

        tree.column("ID", width=70, anchor="center")
        tree.column("NOMBRE", width=260, anchor="w")

        scrollbar_y = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=tree.yview
        )
        tree.configure(yscrollcommand=scrollbar_y.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

        conexion = None
        cursor = None
        try:
            conexion = conectar_bd()
            if conexion is None:
                messagebox.showerror(
                    "Error de conexión",
                    "No se pudo conectar con la base de datos."
                )
                return

            cursor = conexion.cursor()
            cursor.execute(
                """
                SELECT
                    id_medicamento,
                    nombre,
                    via_administracion,
                    presentacion,
                    fecha_caducidad
                FROM public.medicamento
                ORDER BY id_medicamento ASC;
                """
            )
            filas = cursor.fetchall()
            for fila in filas:
                tree.insert("", "end", values=fila)

            if not filas:
                messagebox.showinfo(
                    "Información",
                    "No hay medicamentos registrados."
                )

        except psycopg2.Error as error:
            messagebox.showerror(
                "Error de PostgreSQL",
                f"No se pudieron consultar los medicamentos:\n\n{error}"
            )
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()