from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import psycopg2

from config.conexion import conectar_bd
from gui.estilos import (
    BG_COLOR,
    CARD_BG,
    TEXT_MAIN,
    BTN_SUCCESS
)

VIAS_ADMINISTRACION = [
    "ORAL",
    "INTRAMUSCULAR",
    "INTRAVENOSA",
    "TOPICA",
    "OFTALMICA"
]

PRESENTACIONES_MED = [
    "TABLETA",
    "CAPSULA",
    "JARABE",
    "SOLUCION INYECTABLE",
    "UNGUENTO"
]


class RegistroMedicamento:

    def obtener_siguiente_id_medicamento(self):
        conexion = None
        cursor = None
        try:
            conexion = conectar_bd()
            if conexion is None:
                return 1
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT COALESCE(MAX(id_medicamento), 0) + 1 FROM public.medicamento;"
            )
            fila = cursor.fetchone()
            return int(fila[0]) if fila and fila[0] else 1
        except psycopg2.Error:
            return 1
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

    def _parsear_fecha_caducidad(self, texto_fecha):
        texto = texto_fecha.strip()
        for formato in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"):
            try:
                return datetime.strptime(texto, formato).strftime("%Y-%m-%d")
            except ValueError:
                continue
        raise ValueError("Formato de fecha inválido")

    def mostrar_formulario_medicamento(self):
        self.limpiar_contenedor()
        self.crear_barra_superior(self.main_container)

        content = tk.Frame(self.main_container, bg=BG_COLOR)
        content.pack(fill="both", expand=True, padx=60, pady=35)

        acciones = tk.Frame(content, bg=BG_COLOR)
        acciones.pack(anchor="w", pady=(0, 20))

        tk.Button(
            acciones,
            text="← Volver al Menú",
            font=("Segoe UI", 10, "bold"),
            bg="#e2e8f0",
            fg=TEXT_MAIN,
            relief="flat",
            cursor="hand2",
            command=self.mostrar_dashboard
        ).pack(side="left", padx=(0, 12))

        tk.Button(
            acciones,
            text="📋 Ver Medicamentos",
            font=("Segoe UI", 10, "bold"),
            bg="#0f766e",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.mostrar_consultas_medicamento
        ).pack(side="left")

        form_card = tk.Frame(content, bg=CARD_BG, relief="flat", bd=1)
        form_card.pack(anchor="w", ipadx=40, ipady=25)

        tk.Label(
            form_card,
            text="Registrar Medicamento",
            font=("Segoe UI", 18, "bold"),
            bg=CARD_BG,
            fg=TEXT_MAIN
        ).pack(anchor="w", pady=(10, 25))

        campos = [
            "Código Medicamento (ID):",
            "Nombre:",
            "Vía de Administración:",
            "Presentación:",
            "Fecha Caducidad (DD-MM-AAAA o AAAA-MM-DD):"
        ]

        self.entries_med = {}
        siguiente_id = self.obtener_siguiente_id_medicamento()

        grid = tk.Frame(form_card, bg=CARD_BG)
        grid.pack(anchor="w")

        for i, etiqueta in enumerate(campos):
            tk.Label(
                grid,
                text=etiqueta,
                font=("Segoe UI", 10, "bold"),
                bg=CARD_BG,
                fg=TEXT_MAIN,
                anchor="w"
            ).grid(row=i, column=0, sticky="w", pady=8, padx=8)

            if etiqueta == "Código Medicamento (ID):":
                widget = tk.Entry(
                    grid,
                    font=("Segoe UI", 11),
                    width=32,
                    relief="solid",
                    bd=1,
                    bg="#f1f5f9",
                    fg=TEXT_MAIN
                )
                widget.insert(0, str(siguiente_id))
                widget.config(state="readonly")
            elif etiqueta == "Vía de Administración:":
                widget = tk.Spinbox(
                    grid,
                    values=VIAS_ADMINISTRACION,
                    font=("Segoe UI", 11),
                    width=30,
                    relief="solid",
                    bd=1
                )
                widget.delete(0, tk.END)
                widget.insert(0, "ORAL")
            elif etiqueta == "Presentación:":
                widget = tk.Spinbox(
                    grid,
                    values=PRESENTACIONES_MED,
                    font=("Segoe UI", 11),
                    width=30,
                    relief="solid",
                    bd=1
                )
                widget.delete(0, tk.END)
                widget.insert(0, "TABLETA")
            else:
                widget = tk.Entry(
                    grid,
                    font=("Segoe UI", 11),
                    width=32,
                    relief="solid",
                    bd=1
                )

            widget.grid(row=i, column=1, pady=8, padx=8)
            self.entries_med[etiqueta] = widget

        tk.Button(
            form_card,
            text="Guardar Medicamento",
            font=("Segoe UI", 10, "bold"),
            bg=BTN_SUCCESS,
            fg="white",
            relief="flat",
            width=22,
            cursor="hand2",
            command=self.guardar_medicamento_db
        ).pack(anchor="w", pady=(25, 15), padx=8)

    def guardar_medicamento_db(self):
        conexion = None
        cursor = None
        try:
            nombre = self.entries_med["Nombre:"].get().strip().upper()
            via = self.entries_med["Vía de Administración:"].get().strip().upper()
            presentacion = self.entries_med["Presentación:"].get().strip().upper()
            fecha_raw = self.entries_med[
                "Fecha Caducidad (DD-MM-AAAA o AAAA-MM-DD):"
            ].get().strip()

            if not all([nombre, via, presentacion, fecha_raw]):
                messagebox.showwarning(
                    "Campos vacíos",
                    "Completa todos los datos del medicamento."
                )
                return

            fecha_sql = self._parsear_fecha_caducidad(fecha_raw)

            conexion = conectar_bd()
            if conexion is None:
                return

            cursor = conexion.cursor()
            cursor.execute(
                "SELECT COALESCE(MAX(id_medicamento), 0) + 1 FROM public.medicamento;"
            )
            fila_id = cursor.fetchone()
            id_med = int(fila_id[0]) if fila_id and fila_id[0] else 1

            cursor.execute(
                """
                INSERT INTO public.medicamento (
                    id_medicamento,
                    nombre,
                    via_administracion,
                    presentacion,
                    fecha_caducidad
                )
                VALUES (%s, %s, %s, %s, %s);
                """,
                (id_med, nombre, via, presentacion, fecha_sql)
            )
            conexion.commit()

            messagebox.showinfo(
                "Medicamento registrado",
                f"Se registró '{nombre}' con el ID {id_med}."
            )
            self.mostrar_formulario_medicamento()

        except ValueError:
            messagebox.showerror(
                "Fecha inválida",
                "Usa el formato DD-MM-AAAA o AAAA-MM-DD (ejemplo: 31-01-2027 o 2027-01-31)."
            )
        except psycopg2.Error as error:
            if conexion:
                conexion.rollback()
            messagebox.showerror(
                "Error de PostgreSQL",
                f"No se pudo guardar el medicamento:\n\n{error}"
            )
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()