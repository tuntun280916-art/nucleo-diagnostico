import tkinter as tk

from gui.estilos import (
    BG_COLOR, CARD_BG, PRIMARY_COLOR, TEXT_MAIN, TEXT_MUTED,
    BORDER_COLOR
)


class Dashboard:

    def crear_barra_superior(self, contenedor):

        top_bar = tk.Frame(
            contenedor,
            bg="#e2e8f0",
            height=55
        )
        top_bar.pack(fill="x", side="top")

        # Identificar la sesión activa
        if self.rol_actual == "admin":
            texto_sesion = "👤 Sesión activa: Administrador"
        else:
            nombre = self.empleado_actual["nombre_comp"]
            texto_sesion = f"👤 Sesión activa: {nombre}"

        tk.Label(
            top_bar,
            text=texto_sesion,
            font=("Segoe UI", 11, "bold"),
            bg="#e2e8f0",
            fg=TEXT_MAIN
        ).pack(side="left", padx=25)

        self.img_logo_sup = self.cargar_imagen(
            "recursos/LogoND.png", 75, 38
        )

        if self.img_logo_sup:
            tk.Label(
                top_bar,
                image=self.img_logo_sup,
                bg="#e2e8f0"
            ).pack(side="right", padx=20, pady=6)
        else:
            tk.Label(
                top_bar,
                text="🏥 Núcleo de Diagnóstico",
                font=("Segoe UI", 11, "bold"),
                bg="#e2e8f0",
                fg=PRIMARY_COLOR
            ).pack(side="right", padx=20)

        tk.Button(
            top_bar,
            text="Cerrar Sesión",
            font=("Segoe UI", 10, "bold"),
            bg="#cbd5e1",
            fg=TEXT_MAIN,
            relief="flat",
            cursor="hand2",
            command=self.cerrar_sesion
        ).pack(side="right", padx=10, pady=10)

    def cerrar_sesion(self):

        self.rol_actual = None
        self.empleado_actual = None

        self.mostrar_login()

    def mostrar_dashboard(self):

        self.limpiar_contenedor()

        self.crear_barra_superior(self.main_container)

        # =====================================
        # ÁREA CON SCROLL VERTICAL
        # =====================================

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

        # Frame que contendrá todos los elementos
        contenedor_scroll = tk.Frame(canvas, bg=BG_COLOR)

        ventana_canvas = canvas.create_window(
            (0, 0),
            window=contenedor_scroll,
            anchor="nw"
        )

        # Actualizar el área desplazable
        def actualizar_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        contenedor_scroll.bind("<Configure>", actualizar_scroll)

        # Adaptar el contenido al ancho del Canvas
        def ajustar_ancho(event):
            canvas.itemconfigure(
                ventana_canvas,
                width=event.width
            )

        canvas.bind("<Configure>", ajustar_ancho)

        # Movimiento con la rueda del mouse
        # =====================================
        # DESPLAZAMIENTO CON RUEDA DEL MOUSE
        # =====================================

        def mover_rueda(event):
            if canvas.winfo_exists():
                desplazamiento = -1 if event.delta > 0 else 1
                canvas.yview_scroll(desplazamiento * 3, "units")

        # Habilitar desplazamiento en todo el dashboard
        canvas.bind_all("<MouseWheel>", mover_rueda)

        # =====================================
        # CONTENIDO ORIGINAL DEL DASHBOARD
        # =====================================

        content = tk.Frame(
            contenedor_scroll,
            bg=BG_COLOR
        )
        content.pack(
            fill="both",
            expand=True,
            padx=60,
            pady=45
        )

        self.img_logo_grande = self.cargar_imagen(
            "recursos/LogoND.png", 260, 110
        )

        if self.img_logo_grande:
            tk.Label(
                content,
                image=self.img_logo_grande,
                bg=BG_COLOR
            ).pack(anchor="center", pady=(0, 20))

        tk.Label(
            content,
            text="Panel de Control Principal",
            font=("Segoe UI", 26, "bold"),
            bg=BG_COLOR,
            fg=TEXT_MAIN
        ).pack(anchor="w", pady=(0, 8))

        if self.rol_actual == "admin":

            texto = (
                "Seleccione una opción de gestión para "
                "continuar en el sistema."
            )

        else:

            texto = (
                "Seleccione una opción para gestionar "
                "los registros de pacientes."
            )

        tk.Label(
            content,
            text=texto,
            font=("Segoe UI", 13),
            bg=BG_COLOR,
            fg=TEXT_MUTED
        ).pack(anchor="w", pady=(0, 40))

        grid_cards = tk.Frame(
            content,
            bg=BG_COLOR
        )
        grid_cards.pack(anchor="center", fill="x")

        # =====================================
        # PANEL DEL ADMINISTRADOR
        # =====================================

        if self.rol_actual == "admin":

            card_emp = tk.Frame(
                grid_cards,
                bg=CARD_BG,
                relief="flat",
                bd=1,
                highlightbackground=BORDER_COLOR,
                highlightthickness=1
            )
            card_emp.pack(
                side="left",
                padx=(0, 30),
                ipadx=30,
                ipady=25
            )

            tk.Label(
                card_emp,
                text="Módulo Empleados",
                font=("Segoe UI", 16, "bold"),
                bg=CARD_BG,
                fg=PRIMARY_COLOR
            ).pack(anchor="w", pady=(5, 15))

            tk.Button(
                card_emp,
                text="➕ Registrar Empleado",
                font=("Segoe UI", 11),
                bg=PRIMARY_COLOR,
                fg="white",
                relief="flat",
                width=24,
                cursor="hand2",
                command=lambda: self.mostrar_formulario_empleado()
            ).pack(pady=8)

            tk.Button(
                card_emp,
                text="📋 Consultar Empleados",
                font=("Segoe UI", 11),
                bg="#475569",
                fg="white",
                relief="flat",
                width=24,
                cursor="hand2",
                command=lambda: self.mostrar_consultas_empleado()
            ).pack(pady=8)

            # Tarjeta de médicos
            card_med = tk.Frame(
                grid_cards,
                bg=CARD_BG,
                relief="flat",
                bd=1,
                highlightbackground=BORDER_COLOR,
                highlightthickness=1
            )
            card_med.pack(
                side="left",
                padx=(0, 30),
                ipadx=30,
                ipady=25
            )

            tk.Label(
                card_med,
                text="Módulo Médicos",
                font=("Segoe UI", 16, "bold"),
                bg=CARD_BG,
                fg=PRIMARY_COLOR
            ).pack(anchor="w", pady=(5, 15))

            tk.Button(
                card_med,
                text="➕ Registrar Médico",
                font=("Segoe UI", 11),
                bg=PRIMARY_COLOR,
                fg="white",
                relief="flat",
                width=24,
                cursor="hand2",
                command=lambda: self.mostrar_formulario_medico()
            ).pack(pady=8)

            tk.Button(
                card_med,
                text="📋 Consultar Médicos",
                font=("Segoe UI", 11),
                bg="#475569",
                fg="white",
                relief="flat",
                width=24,
                cursor="hand2",
                command=lambda: self.mostrar_consultas_medico()
            ).pack(pady=8)

        # =====================================
        # PANEL DE EMPLEADOS
        # =====================================

        card_pac = tk.Frame(
            grid_cards,
            bg=CARD_BG,
            relief="flat",
            bd=1,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1
        )

        card_pac.pack(
            side="left",
            padx=(0, 30),
            ipadx=30,
            ipady=25
        )

        tk.Label(
            card_pac,
            text="Módulo Pacientes",
            font=("Segoe UI", 16, "bold"),
            bg=CARD_BG,
            fg=PRIMARY_COLOR
        ).pack(anchor="w", pady=(5, 15))

        tk.Button(
            card_pac,
            text="➕ Registrar Paciente",
            font=("Segoe UI", 11),
            bg=PRIMARY_COLOR,
            fg="white",
            relief="flat",
            width=24,
            cursor="hand2",
            command=lambda: self.mostrar_formulario_paciente()
        ).pack(pady=8)

        tk.Button(
            card_pac,
            text="📋 Consultar Pacientes",
            font=("Segoe UI", 11),
            bg="#475569",
            fg="white",
            relief="flat",
            width=24,
            cursor="hand2",
            command=lambda: self.mostrar_consultas_paciente()
        ).pack(pady=8)



        # =====================================
        # MÓDULO DE CITAS
        # =====================================

        card_citas = tk.Frame(
            content,
            bg=CARD_BG,
            relief="flat",
            bd=1,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1
        )

        card_citas.pack(
            anchor="w",
            padx=(0, 30),
            pady=(25, 0),
            ipadx=30,
            ipady=25
        )

        tk.Label(
            card_citas,
            text="Módulo Citas",
            font=("Segoe UI", 16, "bold"),
            bg=CARD_BG,
            fg=PRIMARY_COLOR
        ).pack(anchor="w", pady=(5, 15))

        tk.Button(
            card_citas,
            text="➕ Registrar Cita",
            font=("Segoe UI", 11),
            bg=PRIMARY_COLOR,
            fg="white",
            relief="flat",
            width=24,
            cursor="hand2",
            command=lambda: self.mostrar_formulario_cita()
        ).pack(pady=8)

        tk.Button(
            card_citas,
            text="📋 Consultar Citas",
            font=("Segoe UI", 11),
            bg="#475569",
            fg="white",
            relief="flat",
            width=24,
            cursor="hand2",
            command=lambda: self.mostrar_consultas_cita()
        ).pack(pady=8)
