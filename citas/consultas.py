
import tkinter as tk
from tkinter import ttk, messagebox

from config.conexion import conectar_bd

from gui.estilos import (
    BG_COLOR,
    CARD_BG,
    PRIMARY_COLOR,
    TEXT_MAIN,
    TEXT_MUTED,
    BORDER_COLOR
)


class ConsultasCita:

    def mostrar_consultas_cita(self):

        # =====================================
        # CONSULTAR CITAS EN POSTGRESQL
        # =====================================

        conexion = conectar_bd()

        if conexion is None:
            return

        try:

            with conexion.cursor() as cursor:

                cursor.execute("""
                    SELECT
                        c.id_cita,
                        p.id_paciente,
                        p.nombre_comp,
                        m.id_medico,
                        m.nombre_comp,
                        c.fecha,
                        c.hora
                    FROM public.cita AS c

                    INNER JOIN public.paciente AS p
                        ON c.id_paciente = p.id_paciente

                    INNER JOIN public.medico AS m
                        ON c.id_medico = m.id_medico

                    ORDER BY c.fecha DESC, c.hora ASC;
                """)

                citas = cursor.fetchall()

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"No se pudieron consultar las citas:\n{error}"
            )

            return

        finally:

            conexion.close()

        # =====================================
        # CONSTRUIR INTERFAZ
        # =====================================

        self.limpiar_contenedor()

        self.crear_barra_superior(
            self.main_container
        )

        content = self.crear_area_desplazable(
            padx=30,
            pady=25
        )

        tk.Button(
            content,
            text="← Volver al menú principal",
            font=("Segoe UI", 11, "bold"),
            bg="#e2e8f0",
            fg=TEXT_MAIN,
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=10,
            command=self.mostrar_dashboard
        ).pack(anchor="w", pady=(0, 20))

        tk.Label(
            content,
            text="Consultar citas registradas",
            font=("Segoe UI", 26, "bold"),
            bg=BG_COLOR,
            fg=TEXT_MAIN
        ).pack(anchor="w", pady=(0, 5))

        tk.Label(
            content,
            text="Consulta y busca las citas del núcleo de diagnóstico.",
            font=("Segoe UI", 12),
            bg=BG_COLOR,
            fg=TEXT_MUTED
        ).pack(anchor="w", pady=(0, 25))

        # =====================================
        # PANEL PRINCIPAL
        # =====================================

        panel = tk.Frame(
            content,
            bg=CARD_BG,
            padx=22,
            pady=22,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1
        )

        panel.pack(fill="both", expand=True)

        # =====================================
        # BARRA DE BÚSQUEDA
        # =====================================

        tk.Label(
            panel,
            text="Buscar cita",
            font=("Segoe UI", 13, "bold"),
            bg=CARD_BG,
            fg=TEXT_MAIN
        ).pack(anchor="w", pady=(0, 8))

        variable_busqueda = tk.StringVar(master=panel)

        buscador = tk.Entry(
            panel,
            textvariable=variable_busqueda,
            font=("Segoe UI", 12),
            width=45,
            relief="flat",
            highlightthickness=1,
            highlightbackground=BORDER_COLOR,
            highlightcolor=PRIMARY_COLOR
        )

        buscador.pack(
            anchor="w",
            ipady=10,
            pady=(0, 5)
        )

        tk.Label(
            panel,
            text="Busca por paciente, médico, ID, fecha u hora.",
            font=("Segoe UI", 10),
            bg=CARD_BG,
            fg=TEXT_MUTED
        ).pack(anchor="w", pady=(0, 20))

        # =====================================
        # CONTADOR Y ACTUALIZACIÓN
        # =====================================

        encabezado = tk.Frame(panel, bg=CARD_BG)
        encabezado.pack(fill="x", pady=(0, 15))

        contador = tk.Label(
            encabezado,
            text="",
            font=("Segoe UI", 12, "bold"),
            bg=CARD_BG,
            fg=TEXT_MAIN
        )

        contador.pack(side="left")

        tk.Button(
            encabezado,
            text="↻ Actualizar",
            font=("Segoe UI", 11, "bold"),
            bg=PRIMARY_COLOR,
            fg="white",
            relief="flat",
            padx=14,
            pady=8,
            cursor="hand2",
            command=self.mostrar_consultas_cita
        ).pack(side="right")

        # =====================================
        # ESTILO DE LA TABLA
        # =====================================

        estilo = ttk.Style(self)

        estilo.configure(
            "Citas.Treeview",
            font=("Segoe UI", 11),
            rowheight=40,
            background="white",
            fieldbackground="white",
            foreground=TEXT_MAIN
        )

        estilo.configure(
            "Citas.Treeview.Heading",
            font=("Segoe UI", 11, "bold"),
            padding=10
        )

        # =====================================
        # TABLA DE CITAS
        # =====================================

        marco_tabla = tk.Frame(
            panel,
            bg=CARD_BG
        )

        marco_tabla.pack(
            fill="both",
            expand=True
        )

        columnas = (
            "id_cita",
            "paciente",
            "medico",
            "fecha",
            "hora"
        )

        tabla = ttk.Treeview(
            marco_tabla,
            columns=columnas,
            show="headings",
            style="Citas.Treeview",
            height=12
        )

        tabla.heading("id_cita", text="ID de cita")
        tabla.heading("paciente", text="Paciente")
        tabla.heading("medico", text="Médico")
        tabla.heading("fecha", text="Fecha")
        tabla.heading("hora", text="Hora")

        tabla.column(
            "id_cita",
            width=135,
            minwidth=110,
            anchor="center"
        )

        tabla.column(
            "paciente",
            width=320,
            minwidth=220,
            anchor="w"
        )

        tabla.column(
            "medico",
            width=320,
            minwidth=220,
            anchor="w"
        )

        tabla.column(
            "fecha",
            width=130,
            minwidth=110,
            anchor="center"
        )

        tabla.column(
            "hora",
            width=100,
            minwidth=80,
            anchor="center"
        )

        scrollbar_vertical = ttk.Scrollbar(
            marco_tabla,
            orient="vertical",
            command=tabla.yview
        )

        scrollbar_horizontal = ttk.Scrollbar(
            marco_tabla,
            orient="horizontal",
            command=tabla.xview
        )

        tabla.configure(
            yscrollcommand=scrollbar_vertical.set,
            xscrollcommand=scrollbar_horizontal.set
        )

        tabla.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        scrollbar_vertical.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        scrollbar_horizontal.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        marco_tabla.grid_columnconfigure(
            0,
            weight=1
        )

        marco_tabla.grid_rowconfigure(
            0,
            weight=1
        )

        tabla.tag_configure(
            "par",
            background="#ffffff"
        )

        tabla.tag_configure(
            "impar",
            background="#f1f5f9"
        )

        # =====================================
        # DESPLAZAMIENTO DE LA TABLA
        # =====================================

        def mover_tabla(event):

            direccion = -1 if event.delta > 0 else 1

            tabla.yview_scroll(
                direccion * 3,
                "units"
            )

            return "break"

        tabla.bind("<MouseWheel>", mover_tabla)

        # =====================================
        # BÚSQUEDA AUTOMÁTICA
        # =====================================

        def cargar_tabla(*args):

            for elemento in tabla.get_children():
                tabla.delete(elemento)

            texto = self.normalizar_busqueda_cita(
                variable_busqueda.get()
            )

            cantidad = 0

            for cita in citas:

                (
                    id_cita,
                    id_paciente,
                    nombre_paciente,
                    id_medico,
                    nombre_medico,
                    fecha,
                    hora
                ) = cita

                fecha_formato = fecha.strftime(
                    "%d/%m/%Y"
                )

                hora_formato = hora.strftime(
                    "%H:%M"
                )

                paciente = (
                    f"{nombre_paciente} "
                    f"(ID {id_paciente})"
                )

                medico = (
                    f"{nombre_medico} "
                    f"(ID {id_medico})"
                )

                contenido = self.normalizar_busqueda_cita(
                    f"{id_cita} "
                    f"{paciente} "
                    f"{medico} "
                    f"{fecha_formato} "
                    f"{fecha.isoformat()} "
                    f"{hora_formato}"
                )

                if not all(
                    palabra in contenido
                    for palabra in texto.split()
                ):
                    continue

                etiqueta = (
                    "par" if cantidad % 2 == 0
                    else "impar"
                )

                tabla.insert(
                    "",
                    tk.END,
                    values=(
                        id_cita,
                        paciente,
                        medico,
                        fecha_formato,
                        hora_formato
                    ),
                    tags=(etiqueta,)
                )

                cantidad += 1

            contador.config(
                text=f"Mostrando {cantidad} de {len(citas)} citas"
            )

        variable_busqueda.trace_add(
            "write",
            cargar_tabla
        )

        cargar_tabla()
