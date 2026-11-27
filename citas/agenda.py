from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox, ttk

from config.conexion import conectar_bd
from citas.registro import HORARIOS_CITA, BLOQUES_COMIDA
from gui.estilos import (
    BG_COLOR,
    CARD_BG,
    PRIMARY_COLOR,
    TEXT_MAIN
)


class AgendaMedico:

    def _obtener_medicos_db(self):
        medicos = []
        conexion = None
        cursor = None
        try:
            conexion = conectar_bd()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute(
                    """
                    SELECT id_medico, nombre_comp
                    FROM public.medico
                    ORDER BY nombre_comp ASC;
                    """
                )
                medicos = cursor.fetchall()
        except Exception as err:
            messagebox.showerror("Error al cargar médicos", f"No se pudo obtener la lista de médicos:\n\n{err}")
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
        return medicos

    def _filtrar_medicos_combo(self, event=None):
        # Ignorar teclas de navegación del desplegable
        if event and event.keysym in ("Up", "Down", "Return", "Escape", "Tab"):
            return

        texto = self.combo_agenda_med.get().strip().lower()
        if not texto:
            self.combo_agenda_med["values"] = self._opciones_medicos
            return

        coincidencias = [
            op for op in self._opciones_medicos
            if texto in op.lower()
        ]
        self.combo_agenda_med["values"] = coincidencias if coincidencias else self._opciones_medicos

    def _resolver_medico_seleccionado(self):
        valor = self.combo_agenda_med.get().strip()
        if not valor:
            return None, "Selecciona o escribe el nombre de un médico."

        # Caso 1: Formato "Nombre Completo (ID: 3)"
        if "(ID:" in valor and valor.endswith(")"):
            try:
                id_str = valor.rsplit("(ID:", 1)[1][:-1].strip()
                id_med = int(id_str)
                for m_id, m_nom in self._lista_medicos:
                    if m_id == id_med:
                        return m_id, f"{m_nom} (ID: {m_id})"
            except ValueError:
                pass

        # Caso 2: El usuario escribió un ID directo
        if valor.isdigit():
            id_med = int(valor)
            for m_id, m_nom in self._lista_medicos:
                if m_id == id_med:
                    return m_id, f"{m_nom} (ID: {m_id})"

        # Caso 3: El usuario escribió el nombre (o parte del nombre) del médico
        valor_lower = valor.lower()
        coincidencias = [
            (m_id, m_nom) for m_id, m_nom in self._lista_medicos
            if valor_lower in m_nom.lower()
        ]

        if len(coincidencias) == 1:
            m_id, m_nom = coincidencias[0]
            return m_id, f"{m_nom} (ID: {m_id})"
        elif len(coincidencias) > 1:
            # Si hay coincidencia exacta, priorizarla
            for m_id, m_nom in coincidencias:
                if m_nom.lower() == valor_lower:
                    return m_id, f"{m_nom} (ID: {m_id})"
            nombres_sugeridos = ", ".join(m_nom for _, m_nom in coincidencias[:4])
            return None, f"Hay más de un médico que coincide con '{valor}': {nombres_sugeridos}. Selecciónalo del menú."

        return None, f"No se encontró ningún médico que coincida con '{valor}'."

    def mostrar_agenda_medico(self):
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
            text="Agenda Semanal del Médico",
            font=("Segoe UI", 20, "bold"),
            bg=BG_COLOR,
            fg=TEXT_MAIN
        ).pack(anchor="w", pady=(0, 12))

        self._lista_medicos = self._obtener_medicos_db()
        self._opciones_medicos = [f"{nom} (ID: {med_id})" for med_id, nom in self._lista_medicos]

        filtros = tk.Frame(content, bg=BG_COLOR)
        filtros.pack(anchor="w", pady=(0, 12))

        tk.Label(
            filtros,
            text="Médico (elegir o escribir nombre):",
            font=("Segoe UI", 10, "bold"),
            bg=BG_COLOR,
            fg=TEXT_MAIN
        ).pack(side="left", padx=(0, 6))

        self.combo_agenda_med = ttk.Combobox(
            filtros,
            values=self._opciones_medicos,
            font=("Segoe UI", 10),
            width=32,
            state="normal"
        )
        if self._opciones_medicos:
            self.combo_agenda_med.set(self._opciones_medicos[0])
        self.combo_agenda_med.pack(side="left", padx=(0, 14))
        self.combo_agenda_med.bind("<KeyRelease>", self._filtrar_medicos_combo)
        self.combo_agenda_med.bind("<<ComboboxSelected>>", lambda _e: self.renderizar_tabla_agenda())

        tk.Label(
            filtros,
            text="Lunes Semana (AAAA-MM-DD):",
            font=("Segoe UI", 10, "bold"),
            bg=BG_COLOR,
            fg=TEXT_MAIN
        ).pack(side="left", padx=(0, 6))

        self.entry_agenda_lunes = tk.Entry(
            filtros,
            font=("Segoe UI", 10),
            width=13,
            relief="solid",
            bd=1
        )
        self.entry_agenda_lunes.insert(0, "2026-11-23")
        self.entry_agenda_lunes.pack(side="left", padx=(0, 14))

        tk.Button(
            filtros,
            text="Consultar Agenda",
            font=("Segoe UI", 10, "bold"),
            bg=PRIMARY_COLOR,
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.renderizar_tabla_agenda
        ).pack(side="left")

        self.lbl_agenda_medico = tk.Label(
            content,
            text="",
            font=("Segoe UI", 12, "bold"),
            bg=BG_COLOR,
            fg=PRIMARY_COLOR
        )
        self.lbl_agenda_medico.pack(anchor="w", pady=(0, 10))

        self.frame_tabla_agenda = tk.Frame(content, bg=CARD_BG)
        self.frame_tabla_agenda.pack(fill="both", expand=True)

        self.renderizar_tabla_agenda()

    def renderizar_tabla_agenda(self):
        for widget in self.frame_tabla_agenda.winfo_children():
            widget.destroy()

        id_medico, etiqueta_medico = self._resolver_medico_seleccionado()
        if id_medico is None:
            messagebox.showwarning("Médico no válido", etiqueta_medico)
            return

        try:
            lunes_dt = datetime.strptime(self.entry_agenda_lunes.get().strip(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Datos inválidos", "Ingresa una fecha de lunes válida con formato AAAA-MM-DD.")
            return

        nombres_dias = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES"]
        dias_semana = []
        for idx in range(5):
            fecha_actual = lunes_dt + timedelta(days=idx)
            encabezado = f"{nombres_dias[idx]} {fecha_actual.strftime('%d/%b').upper()}"
            dias_semana.append((fecha_actual.strftime("%Y-%m-%d"), encabezado))

        nombre_doctor = etiqueta_medico
        citas_ocupadas = {}

        conexion = None
        cursor = None
        try:
            conexion = conectar_bd()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute("SELECT nombre_comp FROM public.medico WHERE id_medico = %s;", (id_medico,))
                med = cursor.fetchone()
                if med:
                    nombre_doctor = f"{med[0]} (ID: {id_medico})"

                fechas_sql = [d[0] for d in dias_semana]
                cursor.execute(
                    """
                    SELECT c.fecha_cita, c.hora_cita, COALESCE(p.nombre_comp, 'Paciente ' || c.id_paciente)
                    FROM public.cita c
                    LEFT JOIN public.paciente p ON c.id_paciente = p.id_paciente
                    WHERE c.id_medico = %s
                      AND c.fecha_cita = ANY(%s::date[]);
                    """,
                    (id_medico, fechas_sql)
                )
                for f_cita, h_cita, nom_pac in cursor.fetchall():
                    citas_ocupadas[(str(f_cita), h_cita)] = nom_pac
        except Exception as err:
            messagebox.showerror("Error al cargar agenda", f"No se pudo consultar la agenda:\n\n{err}")
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

        self.lbl_agenda_medico.config(text=f"Agenda Semanal — {nombre_doctor}")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#e2e8f0", foreground=TEXT_MAIN)
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=32, background="white", fieldbackground="white")

        columnas = ("HORARIO",) + tuple(d[1] for d in dias_semana)
        tree = ttk.Treeview(self.frame_tabla_agenda, columns=columnas, show="headings", height=12)

        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=165, anchor="center")

        tree.column("HORARIO", width=120, anchor="center")

        for hora in HORARIOS_CITA:
            fila = [hora]
            for fecha_iso, _ in dias_semana:
                if hora in BLOQUES_COMIDA:
                    fila.append("COMIDA")
                elif (fecha_iso, hora) in citas_ocupadas:
                    fila.append(citas_ocupadas[(fecha_iso, hora)])
                else:
                    fila.append("")
            tree.insert("", "end", values=tuple(fila))

        tree.pack(fill="both", expand=True)