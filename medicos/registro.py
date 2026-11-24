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


class RegistroMedico:

    def mostrar_formulario_medico(self):
        self.limpiar_contenedor()
        self.crear_barra_superior(self.main_container)

        content = self.crear_area_desplazable()

        tk.Button(
            content,
            text="← Volver al Menú",
            font=("Segoe UI", 10, "bold"),
            bg="#e2e8f0",
            fg=TEXT_MAIN,
            relief="flat",
            cursor="hand2",
            command=self.mostrar_dashboard
        ).pack(anchor="w", pady=(0, 20))

        form_card = tk.Frame(
            content,
            bg=CARD_BG,
            relief="flat",
            bd=1
        )
        form_card.pack(
            anchor="w",
            ipadx=40,
            ipady=25
        )

        tk.Label(
            form_card,
            text="Registrar Nuevo Medico",
            font=("Segoe UI", 18, "bold"),
            bg=CARD_BG,
            fg=TEXT_MAIN
        ).pack(anchor="w", pady=(10, 25))

        campos = [
            "Código (ID):",
            "Nombre Completo:",
            "Dirección:",
            "Teléfono:",
            "Fecha Nac. (AAAA-MM-DD):",
            "Sexo (F/M):",
            "Especialidad:",
            "Contraseña:",
        ]

        self.entries_emp = {}

        fields_grid = tk.Frame(
            form_card,
            bg=CARD_BG
        )
        fields_grid.pack(anchor="w")

        for i, label_text in enumerate(campos):

            tk.Label(
                fields_grid,
                text=label_text,
                font=("Segoe UI", 10, "bold"),
                bg=CARD_BG,
                fg=TEXT_MAIN,
                anchor="w"
            ).grid(
                row=i,
                column=0,
                sticky="w",
                pady=8,
                padx=8
            )

            entry = tk.Entry(
                fields_grid,
                font=("Segoe UI", 11),
                width=32,
                relief="solid",
                bd=1
            )

            entry.grid(
                row=i,
                column=1,
                pady=8,
                padx=8
            )

            self.entries_emp[label_text] = entry

        tk.Button(
            form_card,
            text="Guardar Registro",
            font=("Segoe UI", 11, "bold"),
            bg=BTN_SUCCESS,
            fg="white",
            relief="flat",
            width=28,
            cursor="hand2",
            command=self.guardar_medico_db
        ).pack(
            anchor="w",
            pady=(25, 15),
            padx=8
        )

    def guardar_medico_db(self):

        conexion = None
        cursor = None

        try:

            datos = {
                "id_medico": self.entries_emp["Código (ID):"].get().strip(),
                "nombre_comp": self.entries_emp["Nombre Completo:"].get().strip(),
                "direccion": self.entries_emp["Dirección:"].get().strip(), 
                "telefono": self.entries_emp["Teléfono:"].get().strip(),
                "fecha_nac": self.entries_emp["Fecha Nac. (AAAA-MM-DD):"].get().strip(),
                "sexo": self.entries_emp["Sexo (F/M):"].get().strip().upper(),
                "especialidad": self.entries_emp["Especialidad:"].get().strip().upper(),
                "contrasena": self.entries_emp["Contraseña:"].get().strip(),
            }

            # Validar campos vacíos
            if not all(datos.values()):
                messagebox.showwarning(
                    "Campos vacíos",
                    "Completa todos los campos del empleado."
                )
                return

            # Validar contraseña
            if len(datos["contrasena"]) > 8:
                messagebox.showwarning(
                    "Contraseña inválida",
                    "La contraseña debe tener máximo 8 caracteres."
                )
                return

            # Validar sexo
            if datos["sexo"] not in ("F", "M"):
                messagebox.showwarning(
                    "Sexo inválido",
                    "Ingresa F o M en el campo Sexo."
                )
                return

            # Convertir datos numéricos
            id_empleado = int(datos["id_medico"])

            # Conectar a PostgreSQL
            conexion = conectar_bd()

            if conexion is None:
                return

            cursor = conexion.cursor()

            # Insertar empleado
            cursor.execute("""
                           INSERT INTO medico (
                               id_medico,
                               nombre_comp,
                               direccion,
                               telefono,
                               fecha_nac,
                               sexo,
                               especialidad,
                               contrasena
                               )
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                               """, (
                                   id_empleado,
                                   datos["nombre_comp"],
                                   datos["direccion"],
                                   datos["telefono"],
                                   datos["fecha_nac"],
                                   datos["sexo"],
                                   datos["especialidad"],
                                   datos["contrasena"]
                                   ))
            # Guardar cambios
            conexion.commit()

            messagebox.showinfo(
                "Registro exitoso",
                "Médico registrado correctamente."
            )

            self.mostrar_dashboard()

        except ValueError:

            messagebox.showerror(
                "Datos inválidos",
                "Verifica que el ID sea un número entero "
                "y que el salario sea un número válido."
            )

        except psycopg2.Error as error:

            if conexion:
                conexion.rollback()

            messagebox.showerror(
                "Error de PostgreSQL",
                f"No se pudo registrar el médico:\n\n{error}"
            )

        except Exception as error:

            if conexion:
                conexion.rollback()

            messagebox.showerror(
                "Error al insertar",
                f"No se pudo completar el registro:\n\n{error}"
            )

        finally:

            if cursor:
                cursor.close()

            if conexion:
                conexion.close()
