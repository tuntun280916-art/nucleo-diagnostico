
import tkinter as tk
from tkinter import messagebox
from datetime import date, time
from tkcalendar import Calendar
import unicodedata

from config.conexion import conectar_bd
from citas.horarios import generar_horarios_para_fecha

from gui.estilos import (
    BG_COLOR,
    CARD_BG,
    PRIMARY_COLOR,
    TEXT_MAIN,
    TEXT_MUTED,
    BORDER_COLOR
)


class RegistroCita:

    # =============================================
    # NORMALIZAR TEXTO PARA LAS BÚSQUEDAS
    # =============================================

    def normalizar_busqueda_cita(self, texto):

        texto = unicodedata.normalize("NFD", str(texto))

        return "".join(
            letra for letra in texto
            if unicodedata.category(letra) != "Mn"
        ).casefold().strip()

    # =============================================
    # OBTENER PACIENTES Y MÉDICOS
    # =============================================

    def cargar_catalogos_cita(self):

        conexion = conectar_bd()

        if conexion is None:
            return None

        try:

            with conexion.cursor() as cursor:

                cursor.execute("""
                    SELECT id_paciente, nombre_comp
                    FROM public.paciente
                    ORDER BY nombre_comp;
                """)

                pacientes = cursor.fetchall()

                cursor.execute("""
                    SELECT id_medico, nombre_comp
                    FROM public.medico
                    ORDER BY nombre_comp;
                """)

                medicos = cursor.fetchall()

            return pacientes, medicos

        except Exception as error:

            messagebox.showerror(
                "Error",
                f"No se pudieron cargar los datos:\n{error}"
            )

            return None

        finally:

            conexion.close()

    # =============================================
    # HORARIOS DE ATENCIÓN
    # =============================================

    def horarios_validos_cita(self, fecha):

        return generar_horarios_para_fecha(fecha)

    # =============================================
    # BUSCADOR INTELIGENTE REUTILIZABLE
    # =============================================

    def crear_buscador_cita(
        self,
        contenedor,
        titulo,
        opciones,
        al_cambiar,
        al_seleccionar
    ):

        marco = tk.Frame(contenedor, bg=CARD_BG)
        marco.pack(fill="x", pady=(0, 20))

        tk.Label(
            marco,
            text=titulo,
            font=("Segoe UI", 12, "bold"),
            bg=CARD_BG,
            fg=TEXT_MAIN
        ).pack(anchor="w", pady=(0, 8))

        variable = tk.StringVar(master=marco)

        buscador = tk.Entry(
            marco,
            textvariable=variable,
            font=("Segoe UI", 12),
            width=32,
            relief="flat",
            highlightthickness=1,
            highlightbackground=BORDER_COLOR,
            highlightcolor=PRIMARY_COLOR
        )

        buscador.pack(fill="x", ipady=10)

        tk.Label(
            marco,
            text="Escribe un nombre o número de ID",
            font=("Segoe UI", 9),
            bg=CARD_BG,
            fg=TEXT_MUTED
        ).pack(anchor="w", pady=(5, 0))

        # Contenedor de sugerencias

        sugerencias = tk.Frame(
            marco,
            bg="white",
            highlightthickness=1,
            highlightbackground=BORDER_COLOR
        )

        lista = tk.Listbox(
            sugerencias,
            font=("Segoe UI", 11),
            height=5,
            bg="white",
            fg=TEXT_MAIN,
            selectbackground=PRIMARY_COLOR,
            selectforeground="white",
            relief="flat",
            activestyle="none",
            exportselection=False
        )

        lista.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = tk.Scrollbar(
            sugerencias,
            orient="vertical",
            command=lista.yview
        )

        scrollbar.pack(side="right", fill="y")

        lista.config(
            yscrollcommand=scrollbar.set
        )

        coincidencias = []
        seleccionando = False

        # =========================================
        # BUSCAR MIENTRAS SE ESCRIBE
        # =========================================

        def buscar(*args):

            nonlocal coincidencias

            if seleccionando:
                return

            al_cambiar()

            texto = self.normalizar_busqueda_cita(
                variable.get()
            )

            lista.delete(0, tk.END)
            coincidencias = []

            if texto.startswith("id "):
                texto = texto[3:].strip()

            if not texto:

                sugerencias.pack_forget()
                return

            for identificador, nombre in opciones:

                nombre_normalizado = (
                    self.normalizar_busqueda_cita(nombre)
                )

                if texto.isdigit():

                    coincide = texto in str(identificador)

                else:

                    coincide = all(
                        palabra in nombre_normalizado
                        for palabra in texto.split()
                    )

                if coincide:

                    coincidencias.append(
                        (identificador, nombre)
                    )

            if coincidencias:

                for identificador, nombre in coincidencias:

                    lista.insert(
                        tk.END,
                        f"{nombre} (ID {identificador})"
                    )

                lista.config(
                    height=min(len(coincidencias), 5)
                )

            else:

                lista.insert(
                    tk.END,
                    "No se encontraron coincidencias"
                )

                lista.config(height=1)

            sugerencias.pack(
                fill="x",
                pady=(3, 0)
            )

        # =========================================
        # SELECCIONAR UNA SUGERENCIA
        # =========================================

        def seleccionar(event=None):

            nonlocal seleccionando

            seleccion = lista.curselection()

            if not seleccion or not coincidencias:
                return

            indice = seleccion[0]

            if indice >= len(coincidencias):
                return

            identificador, nombre = coincidencias[indice]

            seleccionando = True

            variable.set(
                f"{nombre} (ID {identificador})"
            )

            seleccionando = False

            sugerencias.pack_forget()

            buscador.focus_set()
            buscador.icursor(tk.END)

            al_seleccionar(identificador)

        # Navegación mediante teclado

        def bajar(event):

            if coincidencias:

                sugerencias.pack(fill="x", pady=(3, 0))

                lista.focus_set()
                lista.selection_clear(0, tk.END)
                lista.selection_set(0)
                lista.activate(0)

            return "break"

        def aceptar_primero(event):

            if coincidencias:

                lista.selection_clear(0, tk.END)
                lista.selection_set(0)

                seleccionar()

            return "break"

        def cerrar_sugerencias(event):

            sugerencias.pack_forget()
            buscador.focus_set()

            return "break"

        def desplazar_lista(event):

            direccion = -1 if event.delta > 0 else 1

            lista.yview_scroll(
                direccion,
                "units"
            )

            return "break"

        variable.trace_add("write", buscar)

        buscador.bind("<Down>", bajar)
        buscador.bind("<Return>", aceptar_primero)
        buscador.bind("<Escape>", cerrar_sugerencias)

        lista.bind("<ButtonRelease-1>", seleccionar)
        lista.bind("<Return>", seleccionar)
        lista.bind("<Escape>", cerrar_sugerencias)
        lista.bind("<MouseWheel>", desplazar_lista)

        return buscador

    # =============================================
    # FORMULARIO PRINCIPAL
    # =============================================

    def mostrar_formulario_cita(self):

        catalogos = self.cargar_catalogos_cita()

        if catalogos is None:
            return

        pacientes, medicos = catalogos

        nombres_pacientes = dict(pacientes)
        nombres_medicos = dict(medicos)

        self.limpiar_contenedor()

        self.crear_barra_superior(
            self.main_container
        )

        content = self.crear_area_desplazable(
            padx=30,
            pady=25
        )

        estado: dict[str, int | date | str | None] = {
            "paciente": None,
            "medico": None,
            "fecha": None,
            "hora": None
        }
        botones_horarios = {}

        # =========================================
        # BOTÓN REGRESAR
        # =========================================

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
            text="Registrar nueva cita",
            font=("Segoe UI", 26, "bold"),
            bg=BG_COLOR,
            fg=TEXT_MAIN
        ).pack(anchor="w", pady=(0, 5))

        tk.Label(
            content,
            text="Selecciona al paciente, al médico y un horario disponible.",
            font=("Segoe UI", 12),
            bg=BG_COLOR,
            fg=TEXT_MUTED
        ).pack(anchor="w", pady=(0, 25))

        cuerpo = tk.Frame(
            content,
            bg=BG_COLOR
        )

        cuerpo.pack(
            fill="both",
            expand=True
        )

        # =========================================
        # PANEL IZQUIERDO
        # =========================================

        izquierda = tk.Frame(
            cuerpo,
            bg=CARD_BG,
            padx=22,
            pady=22,
            highlightthickness=1,
            highlightbackground=BORDER_COLOR
        )

        izquierda.pack(
            side="left",
            anchor="n",
            padx=(0, 20)
        )

        tk.Label(
            izquierda,
            text="Datos de la cita",
            font=("Segoe UI", 19, "bold"),
            bg=CARD_BG,
            fg=TEXT_MAIN
        ).pack(anchor="w", pady=(0, 25))

        # =========================================
        # PANEL DERECHO
        # =========================================

        derecha = tk.Frame(
            cuerpo,
            bg=CARD_BG,
            padx=24,
            pady=24,
            highlightthickness=1,
            highlightbackground=BORDER_COLOR
        )

        derecha.pack(
            side="left",
            anchor="n",
            fill="both",
            expand=True
        )

        tk.Label(
            derecha,
            text="Agenda del médico",
            font=("Segoe UI", 19, "bold"),
            bg=CARD_BG,
            fg=TEXT_MAIN
        ).pack(anchor="w", pady=(0, 8))

        tk.Label(
            derecha,
            text="Consulta la disponibilidad seleccionando una fecha.",
            font=("Segoe UI", 11),
            bg=CARD_BG,
            fg=TEXT_MUTED,
            wraplength=400,
            justify="left"
        ).pack(anchor="w", pady=(0, 20))

        # =========================================
        # CALENDARIO
        # =========================================

        calendario = Calendar(
            derecha,
            selectmode="day",
            locale="es_MX",
            date_pattern="yyyy-mm-dd",
            firstweekday="monday",
            showweeknumbers=False,
            font=("Segoe UI", 13),
            background="#ffffff",
            foreground="#0f172a",
            bordercolor="#e2e8f0",
            headersbackground="#ffffff",
            headersforeground="#64748b",
            selectbackground="#2563eb",
            selectforeground="#ffffff",
            normalbackground="#ffffff",
            normalforeground="#0f172a",
            weekendbackground="#f8fafc",
            weekendforeground="#475569",
            othermonthbackground="#ffffff",
            othermonthforeground="#cbd5e1",
            othermonthwebackground="#ffffff",
            othermonthweforeground="#cbd5e1"
        )

        calendario.pack(
            anchor="w",
            pady=(0, 20)
        )

        # =========================================
        # LEYENDA DE COLORES
        # =========================================

        leyenda = tk.Frame(
            derecha,
            bg=CARD_BG
        )

        leyenda.pack(
            anchor="w",
            pady=(0, 15)
        )

        colores = [
            ("Disponible", "#16a34a"),
            ("Ocupado", "#dc2626"),
            ("Seleccionado", "#2563eb")
        ]

        for texto, color in colores:

            tk.Label(
                leyenda,
                text="●",
                font=("Segoe UI", 15),
                bg=CARD_BG,
                fg=color
            ).pack(side="left", padx=(0, 4))

            tk.Label(
                leyenda,
                text=texto,
                font=("Segoe UI", 10),
                bg=CARD_BG,
                fg=TEXT_MAIN
            ).pack(side="left", padx=(0, 12))

        tk.Label(
            derecha,
            text="Horarios de atención",
            font=("Segoe UI", 14, "bold"),
            bg=CARD_BG,
            fg=TEXT_MAIN
        ).pack(anchor="w", pady=(0, 10))

        frame_horarios = tk.Frame(
            derecha,
            bg=CARD_BG
        )

        frame_horarios.pack(anchor="w")

        lbl_estado_agenda = tk.Label(
            derecha,
            text="",
            font=("Segoe UI", 10),
            bg=CARD_BG,
            fg=TEXT_MUTED,
            wraplength=400,
            justify="left"
        )

        lbl_estado_agenda.pack(
            anchor="w",
            pady=(15, 0)
        )

        # =========================================
        # ACTUALIZAR BOTÓN REGISTRAR
        # =========================================

        def actualizar_boton():

            completo = all(
                estado[campo] is not None
                for campo in (
                    "paciente",
                    "medico",
                    "fecha",
                    "hora"
                )
            )

            boton_registrar.config(
                state="normal" if completo else "disabled",
                bg="#10b981" if completo else "#94a3b8"
            )

        # =========================================
        # LIMPIAR AGENDA
        # =========================================

        def limpiar_agenda():

            estado["fecha"] = None
            estado["hora"] = None

            lbl_fecha.config(
                text="No seleccionada"
            )

            lbl_hora.config(
                text="No seleccionada"
            )

            lbl_estado_agenda.config(text="")

            for widget in frame_horarios.winfo_children():
                widget.destroy()

            botones_horarios.clear()

            actualizar_boton()

        # =========================================
        # CAMBIOS DE PACIENTE
        # =========================================

        def paciente_modificado():

            habia_paciente = estado["paciente"] is not None

            estado["paciente"] = None

            if habia_paciente and estado["medico"] is not None:

                actualizar_horarios()

            else:

                actualizar_boton()

        def paciente_seleccionado(identificador):

            estado["paciente"] = identificador

            if estado["medico"] is not None:

                actualizar_horarios()

            else:

                actualizar_boton()

        # =========================================
        # CAMBIOS DE MÉDICO
        # =========================================

        def medico_modificado():

            estado["medico"] = None

            limpiar_agenda()

            lbl_estado_agenda.config(
                text="Selecciona un médico para consultar su agenda."
            )

        def medico_seleccionado(identificador):

            estado["medico"] = identificador

            actualizar_horarios()

        # =========================================
        # SELECCIONAR HORA
        # =========================================

        def seleccionar_hora(hora):

            anterior = estado["hora"]

            if anterior in botones_horarios:

                botones_horarios[anterior].config(
                    bg="#dcfce7",
                    fg="#166534"
                )

            estado["hora"] = hora

            lbl_hora.config(
                text=hora
            )

            botones_horarios[hora].config(
                bg="#2563eb",
                fg="white"
            )

            actualizar_boton()

        # =========================================
        # CONSULTAR DISPONIBILIDAD
        # MÉDICO Y PACIENTE
        # =========================================

        def actualizar_horarios(event=None):

            limpiar_agenda()

            if estado["medico"] is None:

                lbl_estado_agenda.config(
                    text="Primero selecciona un médico.",
                    fg=TEXT_MUTED
                )

                return

            fecha = calendario.selection_get()

            horarios = self.horarios_validos_cita(fecha)

            if not horarios:

                lbl_estado_agenda.config(
                    text="Domingo: no hay atención médica.",
                    fg="#dc2626"
                )

                return

            conexion = conectar_bd()

            if conexion is None:

                lbl_estado_agenda.config(
                    text="No se pudo consultar la disponibilidad.",
                    fg="#dc2626"
                )

                return

            try:

                with conexion.cursor() as cursor:

                    cursor.execute("""
                        SELECT
                            hora,
                            id_medico,
                            id_paciente
                        FROM public.cita
                        WHERE fecha = %s
                          AND (
                              id_medico = %s
                              OR id_paciente = %s
                          );
                    """, (
                        fecha,
                        estado["medico"],
                        estado["paciente"]
                    ))

                    registros = cursor.fetchall()

            except Exception as error:

                messagebox.showerror(
                    "Error de agenda",
                    f"No se pudo consultar la agenda:\n{error}"
                )

                return

            finally:

                conexion.close()

            # Horarios ocupados del médico

            ocupadas_medico = {
                registro[0].strftime("%H:%M")
                for registro in registros
                if registro[1] == estado["medico"]
            }

            # Horarios ocupados del paciente

            ocupadas_paciente = {
                registro[0].strftime("%H:%M")
                for registro in registros
                if registro[2] == estado["paciente"]
            }

            # Unión de ambos conjuntos

            ocupadas = ocupadas_medico | ocupadas_paciente

            estado["fecha"] = fecha

            lbl_fecha.config(
                text=fecha.strftime("%d/%m/%Y")
            )

            # =====================================
            # CREAR BOTONES DE HORARIOS
            # =====================================

            for indice, hora in enumerate(horarios):

                disponible = hora not in ocupadas

                boton = tk.Button(
                    frame_horarios,
                    text=hora,
                    font=("Segoe UI", 12, "bold"),
                    width=7,
                    height=2,
                    relief="flat",
                    bd=0,
                    bg=(
                        "#dcfce7" if disponible
                        else "#fecaca"
                    ),
                    fg=(
                        "#166534" if disponible
                        else "#991b1b"
                    ),
                    disabledforeground="#991b1b",
                    activebackground="#2563eb",
                    activeforeground="white",
                    cursor=(
                        "hand2" if disponible
                        else "arrow"
                    ),
                    state=(
                        "normal" if disponible
                        else "disabled"
                    ),
                    command=lambda h=hora: seleccionar_hora(h)
                )

                boton.grid(
                    row=indice // 4,
                    column=indice % 4,
                    padx=5,
                    pady=5,
                    sticky="ew"
                )

                if disponible:

                    botones_horarios[hora] = boton

            # Mostrar información de disponibilidad

            mensajes = []

            if ocupadas_medico:

                mensajes.append(
                    "Horarios ocupados del médico: "
                    + ", ".join(sorted(ocupadas_medico))
                )

            if ocupadas_paciente:

                mensajes.append(
                    "El paciente ya tiene citas a las: "
                    + ", ".join(sorted(ocupadas_paciente))
                )

            if mensajes:

                lbl_estado_agenda.config(
                    text="\n\n".join(mensajes),
                    fg="#b91c1c"
                )

            else:

                lbl_estado_agenda.config(
                    text="Todos los horarios de atención están disponibles.",
                    fg="#166534"
                )

            actualizar_boton()

        # =========================================
        # REGISTRAR CITA EN POSTGRESQL
        # =========================================

        def registrar_cita():

            if any(
                estado[campo] is None
                for campo in (
                    "paciente",
                    "medico",
                    "fecha",
                    "hora"
                )
            ):

                messagebox.showwarning(
                    "Datos incompletos",
                    "Selecciona paciente, médico, fecha y hora."
                )

                return

            id_paciente = estado["paciente"]
            id_medico = estado["medico"]
            fecha = estado["fecha"]
            hora = estado["hora"]
            if not isinstance(fecha, date) or not isinstance(hora, str):

                messagebox.showwarning(
                    "Datos inválidos",
                    "Selecciona una fecha y hora válidas."
                )

                return

             #Validar horario de atencion

            if hora not in self.horarios_validos_cita(fecha):

                messagebox.showerror(
                    "Horario inválido",
                    "El horario está fuera del horario de atención."
                )

                return

            # =====================================
            # CONFIRMACIÓN DE LA CITA
            # =====================================

            confirmar = messagebox.askyesno(
                "Confirmar cita",
                f"¿Deseas registrar la siguiente cita?\n\n"
                f"Paciente: {nombres_pacientes[id_paciente]}\n\n"
                f"Médico: {nombres_medicos[id_medico]}\n\n"
                f"Fecha: {fecha.strftime('%d/%m/%Y')}\n"
                f"Hora: {hora}"
            )

            if not confirmar:
                return

            conexion = conectar_bd()

            if conexion is None:
                return

            motivo = None
            id_cita = None

            try:

                conexion.autocommit = False

                with conexion.cursor() as cursor:

                    # Bloquear escrituras simultáneas
                    # durante la validación y el registro.

                    cursor.execute("""
                        LOCK TABLE public.cita
                        IN SHARE ROW EXCLUSIVE MODE;
                    """)

                    # =================================
                    # VALIDAR DISPONIBILIDAD DEL MÉDICO
                    # Y DEL PACIENTE
                    # =================================

                    cursor.execute("""
                        SELECT id_medico, id_paciente
                        FROM public.cita
                        WHERE fecha = %s
                          AND hora = %s
                          AND (
                              id_medico = %s
                              OR id_paciente = %s
                          );
                    """, (
                        fecha,
                        time.fromisoformat(hora),
                        id_medico,
                        id_paciente
                    ))

                    conflictos = cursor.fetchall()

                    if conflictos:

                        paciente_ocupado = any(
                            fila[1] == id_paciente
                            for fila in conflictos
                        )

                        medico_ocupado = any(
                            fila[0] == id_medico
                            for fila in conflictos
                        )

                        if paciente_ocupado and medico_ocupado:

                            motivo = (
                                "El paciente y el médico "
                                "ya tienen una cita "
                                "en ese horario."
                            )

                        elif paciente_ocupado:

                            motivo = (
                                "El paciente ya tiene una cita "
                                "registrada en ese horario, "
                                "aunque sea con otro médico."
                            )

                        else:

                            motivo = (
                                "El médico ya tiene una cita "
                                "registrada en ese horario."
                            )

                    else:

                        # =============================
                        # INSERTAR NUEVA CITA
                        # =============================

                        cursor.execute("""
                            INSERT INTO public.cita (
                                id_paciente,
                                id_medico,
                                fecha,
                                hora
                            )
                            VALUES (%s, %s, %s, %s)
                            RETURNING id_cita;
                        """, (
                            id_paciente,
                            id_medico,
                            fecha,
                            time.fromisoformat(hora)
                        ))

                        id_cita = cursor.fetchone()[0]

                if motivo is not None:

                    conexion.rollback()

                else:

                    conexion.commit()

            except Exception as error:

                conexion.rollback()

                messagebox.showerror(
                    "Error al registrar",
                    f"No se pudo registrar la cita:\n{error}"
                )

                return

            finally:

                conexion.close()

            # =====================================
            # MOSTRAR CONFLICTO DE HORARIO
            # =====================================

            if motivo is not None:

                messagebox.showwarning(
                    "Horario ocupado",
                    motivo + "\n\nSelecciona otro horario."
                )

                actualizar_horarios()

                return

            # =====================================
            # REGISTRO EXITOSO
            # =====================================

            messagebox.showinfo(
                "Cita registrada",
                f"La cita se registró correctamente.\n\n"
                f"ID de cita: {id_cita}\n\n"
                f"Paciente: {nombres_pacientes[id_paciente]}\n\n"
                f"Médico: {nombres_medicos[id_medico]}\n\n"
                f"Fecha: {fecha.strftime('%d/%m/%Y')}\n"
                f"Hora: {hora}"
            )

            # Regresar únicamente después de guardar

            self.mostrar_dashboard()

        # =========================================
        # CONSTRUIR BUSCADORES
        # =========================================

        self.crear_buscador_cita(
            izquierda,
            "Buscar paciente",
            pacientes,
            al_cambiar=paciente_modificado,
            al_seleccionar=paciente_seleccionado
        )

        self.crear_buscador_cita(
            izquierda,
            "Buscar médico",
            medicos,
            al_cambiar=medico_modificado,
            al_seleccionar=medico_seleccionado
        )

        tk.Button(
            izquierda,
            text="Ver disponibilidad del doctor",
            font=("Segoe UI", 12, "bold"),
            bg=PRIMARY_COLOR,
            fg="white",
            relief="flat",
            cursor="hand2",
            pady=12,
            command=actualizar_horarios
        ).pack(fill="x", pady=(0, 25))

        # =========================================
        # RESUMEN DE LA CITA
        # =========================================

        tk.Frame(
            izquierda,
            bg=BORDER_COLOR,
            height=1
        ).pack(fill="x", pady=(0, 20))

        tk.Label(
            izquierda,
            text="Fecha seleccionada",
            font=("Segoe UI", 11),
            bg=CARD_BG,
            fg=TEXT_MUTED
        ).pack(anchor="w")

        lbl_fecha = tk.Label(
            izquierda,
            text="No seleccionada",
            font=("Segoe UI", 16, "bold"),
            bg=CARD_BG,
            fg=TEXT_MAIN
        )

        lbl_fecha.pack(
            anchor="w",
            pady=(5, 20)
        )

        tk.Label(
            izquierda,
            text="Hora seleccionada",
            font=("Segoe UI", 11),
            bg=CARD_BG,
            fg=TEXT_MUTED
        ).pack(anchor="w")

        lbl_hora = tk.Label(
            izquierda,
            text="No seleccionada",
            font=("Segoe UI", 16, "bold"),
            bg=CARD_BG,
            fg=TEXT_MAIN
        )

        lbl_hora.pack(
            anchor="w",
            pady=(5, 25)
        )

        # =========================================
        # BOTÓN REGISTRAR
        # =========================================

        boton_registrar = tk.Button(
            izquierda,
            text="Registrar cita",
            font=("Segoe UI", 13, "bold"),
            bg="#94a3b8",
            fg="white",
            disabledforeground="white",
            relief="flat",
            cursor="hand2",
            state="disabled",
            pady=14,
            command=registrar_cita
        )

        boton_registrar.pack(fill="x")

        # =========================================
        # EVENTOS DEL CALENDARIO
        # =========================================

        calendario.bind(
            "<<CalendarSelected>>",
            actualizar_horarios
        )

        # Estado inicial del formulario

        actualizar_horarios()
