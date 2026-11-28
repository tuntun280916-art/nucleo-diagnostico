from datetime import datetime, time
import tkinter as tk
from tkinter import ttk, messagebox

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
            text="Consulta, busca o modifica las citas del núcleo de diagnóstico.",
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
        # CONTADOR Y ACCIONES
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

        botones_accion = tk.Frame(
            encabezado,
            bg=CARD_BG
        )

        botones_accion.pack(side="right")

        tk.Button(
            botones_accion,
            text="✎ Modificar cita",
            font=("Segoe UI", 11, "bold"),
            bg="#f59e0b",
            fg="white",
            relief="flat",
            padx=14,
            pady=8,
            cursor="hand2",
            command=lambda: abrir_modal_modificar()
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            botones_accion,
            text="↻ Actualizar",
            font=("Segoe UI", 11, "bold"),
            bg=PRIMARY_COLOR,
            fg="white",
            relief="flat",
            padx=14,
            pady=8,
            cursor="hand2",
            command=self.mostrar_consultas_cita
        ).pack(side="left")

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
        # MAPA DE CITAS
        # =====================================

        mapa_citas = {
            cita[0]: cita for cita in citas
        }

        # =====================================
        # MODAL PARA MODIFICAR CITA
        # =====================================

        def abrir_modal_modificar(event=None):

            seleccion = tabla.selection()

            if not seleccion:

                messagebox.showwarning(
                    "Sin selección",
                    "Selecciona una cita de la tabla para modificarla."
                )

                return

            valores = tabla.item(
                seleccion[0],
                "values"
            )

            id_cita_sel = int(valores[0])

            cita_actual = mapa_citas.get(id_cita_sel)

            if not cita_actual:
                return

            (
                _,
                id_pac_act,
                _,
                id_med_act,
                _,
                fecha_act,
                hora_act
            ) = cita_actual

            # =====================================
            # CONSULTAR PACIENTES Y MÉDICOS
            # =====================================

            conn_cat = conectar_bd()

            if conn_cat is None:
                return

            try:

                with conn_cat.cursor() as cur:

                    cur.execute("""
                        SELECT id_paciente, nombre_comp
                        FROM public.paciente
                        ORDER BY nombre_comp;
                    """)

                    pacientes_db = cur.fetchall()

                    cur.execute("""
                        SELECT id_medico, nombre_comp
                        FROM public.medico
                        ORDER BY nombre_comp;
                    """)

                    medicos_db = cur.fetchall()

            except Exception as error:

                messagebox.showerror(
                    "Error",
                    f"No se pudieron consultar pacientes y médicos:\n{error}"
                )

                return

            finally:

                conn_cat.close()

            if not pacientes_db or not medicos_db:

                messagebox.showwarning(
                    "Datos insuficientes",
                    "No existen pacientes o médicos registrados."
                )

                return

            # =====================================
            # CONSTRUIR VENTANA MODAL
            # =====================================

            modal = tk.Toplevel(self)

            modal.title(
                f"Modificar Cita #{id_cita_sel}"
            )

            modal.geometry("440x360")
            modal.configure(bg=CARD_BG)
            modal.transient(self)
            modal.grab_set()

            tk.Label(
                modal,
                text=f"Modificar Cita #{id_cita_sel}",
                font=("Segoe UI", 16, "bold"),
                bg=CARD_BG,
                fg=TEXT_MAIN
            ).pack(
                anchor="w",
                padx=24,
                pady=(20, 14)
            )

            # =====================================
            # PACIENTE
            # =====================================

            opciones_pac = [
                f"{nom} (ID {pid})"
                for pid, nom in pacientes_db
            ]

            tk.Label(
                modal,
                text="Paciente:",
                font=("Segoe UI", 10, "bold"),
                bg=CARD_BG,
                fg=TEXT_MAIN
            ).pack(
                anchor="w",
                padx=24
            )

            combo_pac = ttk.Combobox(
                modal,
                values=opciones_pac,
                font=("Segoe UI", 10),
                width=42,
                state="readonly"
            )

            for idx, (pid, _) in enumerate(pacientes_db):

                if pid == id_pac_act:

                    combo_pac.current(idx)
                    break

            combo_pac.pack(
                anchor="w",
                padx=24,
                pady=(4, 12)
            )

            # =====================================
            # MÉDICO
            # =====================================

            opciones_med = [
                f"{nom} (ID {mid})"
                for mid, nom in medicos_db
            ]

            tk.Label(
                modal,
                text="Médico:",
                font=("Segoe UI", 10, "bold"),
                bg=CARD_BG,
                fg=TEXT_MAIN
            ).pack(
                anchor="w",
                padx=24
            )

            combo_med = ttk.Combobox(
                modal,
                values=opciones_med,
                font=("Segoe UI", 10),
                width=42,
                state="readonly"
            )

            for idx, (mid, _) in enumerate(medicos_db):

                if mid == id_med_act:

                    combo_med.current(idx)
                    break

            combo_med.pack(
                anchor="w",
                padx=24,
                pady=(4, 12)
            )

            # =====================================
            # FECHA Y HORA
            # =====================================

            fila_fh = tk.Frame(
                modal,
                bg=CARD_BG
            )

            fila_fh.pack(
                anchor="w",
                padx=24,
                pady=(0, 18)
            )

            tk.Label(
                fila_fh,
                text="Fecha (AAAA-MM-DD):",
                font=("Segoe UI", 10, "bold"),
                bg=CARD_BG,
                fg=TEXT_MAIN
            ).grid(
                row=0,
                column=0,
                sticky="w",
                padx=(0, 12)
            )

            entry_fecha = tk.Entry(
                fila_fh,
                font=("Segoe UI", 11),
                width=15
            )

            entry_fecha.insert(
                0,
                fecha_act.strftime("%Y-%m-%d")
            )

            entry_fecha.grid(
                row=1,
                column=0,
                sticky="w",
                padx=(0, 12),
                pady=(4, 0)
            )

            tk.Label(
                fila_fh,
                text="Hora (HH:MM):",
                font=("Segoe UI", 10, "bold"),
                bg=CARD_BG,
                fg=TEXT_MAIN
            ).grid(
                row=0,
                column=1,
                sticky="w"
            )

            hora_actual_str = hora_act.strftime("%H:%M")

            horarios_disp = generar_horarios_para_fecha(
                fecha_act
            )

            if hora_actual_str not in horarios_disp:

                horarios_disp = sorted(
                    set(horarios_disp + [hora_actual_str])
                )

            combo_hora = ttk.Combobox(
                fila_fh,
                values=horarios_disp,
                font=("Segoe UI", 11),
                width=10,
                state="readonly"
            )

            combo_hora.set(hora_actual_str)

            combo_hora.grid(
                row=1,
                column=1,
                sticky="w",
                pady=(4, 0)
            )

            # =====================================
            # GUARDAR CAMBIOS
            # =====================================

            def guardar_cambios():

                # Validar fecha

                try:

                    nueva_fecha = datetime.strptime(
                        entry_fecha.get().strip(),
                        "%Y-%m-%d"
                    ).date()

                except ValueError:

                    messagebox.showerror(
                        "Fecha inválida",
                        "Usa el formato AAAA-MM-DD.",
                        parent=modal
                    )

                    return

                # Validar hora

                nueva_hora_str = combo_hora.get().strip()

                try:

                    nueva_hora = time.fromisoformat(
                        nueva_hora_str
                    )

                except ValueError:

                    messagebox.showerror(
                        "Hora inválida",
                        "Selecciona una hora válida.",
                        parent=modal
                    )

                    return

                # Validar paciente y médico

                if combo_pac.current() < 0 or combo_med.current() < 0:

                    messagebox.showwarning(
                        "Datos incompletos",
                        "Selecciona un paciente y un médico.",
                        parent=modal
                    )

                    return

                nuevo_id_pac = pacientes_db[
                    combo_pac.current()
                ][0]

                nuevo_id_med = medicos_db[
                    combo_med.current()
                ][0]

                # =====================================
                # CONEXIÓN PARA ACTUALIZAR
                # =====================================

                conn_upd = conectar_bd()

                if conn_upd is None:
                    return

                try:

                    conn_upd.autocommit = False

                    with conn_upd.cursor() as cur:

                        # Bloquear tabla para evitar
                        # modificaciones simultáneas

                        cur.execute("""
                            LOCK TABLE public.cita
                            IN SHARE ROW EXCLUSIVE MODE;
                        """)

                        # =====================================
                        # VALIDAR DISPONIBILIDAD
                        # =====================================

                        cur.execute("""
                            SELECT id_cita
                            FROM public.cita
                            WHERE id_cita <> %s
                              AND fecha = %s
                              AND hora = %s
                              AND (
                                  id_medico = %s
                                  OR id_paciente = %s
                              );
                        """, (
                            id_cita_sel,
                            nueva_fecha,
                            nueva_hora,
                            nuevo_id_med,
                            nuevo_id_pac
                        ))

                        if cur.fetchone():

                            conn_upd.rollback()

                            messagebox.showwarning(
                                "Horario ocupado",
                                "Ya existe otra cita en esa fecha y hora "
                                "para ese médico o paciente.",
                                parent=modal
                            )

                            return

                        # =====================================
                        # EJECUTAR UPDATE
                        # =====================================

                        cur.execute("""
                            UPDATE public.cita
                            SET
                                id_paciente = %s,
                                id_medico = %s,
                                fecha = %s,
                                hora = %s
                            WHERE id_cita = %s;
                        """, (
                            nuevo_id_pac,
                            nuevo_id_med,
                            nueva_fecha,
                            nueva_hora,
                            id_cita_sel
                        ))

                        if cur.rowcount == 0:

                            conn_upd.rollback()

                            messagebox.showwarning(
                                "Cita no encontrada",
                                "La cita ya no existe en la base de datos.",
                                parent=modal
                            )

                            return

                    # =====================================
                    # CONFIRMAR TRANSACCIÓN
                    # =====================================

                    conn_upd.commit()

                    messagebox.showinfo(
                        "Cita actualizada",
                        f"La cita #{id_cita_sel} se actualizó correctamente.",
                        parent=modal
                    )

                    modal.destroy()

                    # Actualizar automáticamente la tabla

                    self.mostrar_consultas_cita()

                except Exception as error:

                    conn_upd.rollback()

                    messagebox.showerror(
                        "Error al actualizar",
                        f"No se pudo modificar la cita:\n{error}",
                        parent=modal
                    )

                finally:

                    conn_upd.close()

            # =====================================
            # BOTONES DEL MODAL
            # =====================================

            btns = tk.Frame(
                modal,
                bg=CARD_BG
            )

            btns.pack(
                anchor="e",
                padx=24,
                pady=(8, 16)
            )

            tk.Button(
                btns,
                text="Cancelar",
                font=("Segoe UI", 10, "bold"),
                bg="#e2e8f0",
                fg=TEXT_MAIN,
                relief="flat",
                padx=14,
                pady=8,
                cursor="hand2",
                command=modal.destroy
            ).pack(
                side="left",
                padx=(0, 10)
            )

            tk.Button(
                btns,
                text="Guardar cambios",
                font=("Segoe UI", 10, "bold"),
                bg="#10b981",
                fg="white",
                relief="flat",
                padx=14,
                pady=8,
                cursor="hand2",
                command=guardar_cambios
            ).pack(side="left")

        # =====================================
        # DOBLE CLIC PARA MODIFICAR
        # =====================================

        tabla.bind(
            "<Double-1>",
            abrir_modal_modificar
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

        tabla.bind(
            "<MouseWheel>",
            mover_tabla
        )

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
