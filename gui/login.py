import tkinter as tk
from tkinter import messagebox

from config.conexion import conectar_bd
from gui.estilos import (
    BG_COLOR, CARD_BG, PRIMARY_COLOR, TEXT_MAIN, BTN_DANGER
)


class Login:

    def mostrar_login(self):
        self.limpiar_contenedor()

        card = tk.Frame(
            self.main_container,
            bg=CARD_BG,
            relief="flat",
            bd=1
        )
        card.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            width=460,
            height=420
        )

        self.img_logo_login = self.cargar_imagen(
            "recursos/LogoND.png", 160, 70
        )

        if self.img_logo_login:
            tk.Label(
                card,
                image=self.img_logo_login,
                bg=CARD_BG
            ).pack(pady=(35, 15))

        tk.Label(
            card,
            text="Iniciar Sesión",
            font=("Segoe UI", 18, "bold"),
            bg=CARD_BG,
            fg=TEXT_MAIN
        ).pack(pady=(0, 20))

        form_frame = tk.Frame(card, bg=CARD_BG)
        form_frame.pack(pady=5)

        tk.Label(
            form_frame,
            text="Usuario (ID):",
            font=("Segoe UI", 11, "bold"),
            bg=CARD_BG,
            fg=TEXT_MAIN,
            anchor="w"
        ).grid(row=0, column=0, sticky="w", pady=10)

        self.entry_usuario = tk.Entry(
            form_frame,
            font=("Segoe UI", 11),
            width=22,
            relief="solid",
            bd=1
        )
        self.entry_usuario.grid(
            row=0, column=1, pady=10, padx=12
        )

        tk.Label(
            form_frame,
            text="Contraseña:",
            font=("Segoe UI", 11, "bold"),
            bg=CARD_BG,
            fg=TEXT_MAIN,
            anchor="w"
        ).grid(row=1, column=0, sticky="w", pady=10)

        self.entry_pass = tk.Entry(
            form_frame,
            font=("Segoe UI", 11),
            width=22,
            show="*",
            relief="solid",
            bd=1
        )
        self.entry_pass.grid(
            row=1, column=1, pady=10, padx=12
        )

        btn_frame = tk.Frame(card, bg=CARD_BG)
        btn_frame.pack(pady=25)

        tk.Button(
            btn_frame,
            text="Ingresar",
            font=("Segoe UI", 10, "bold"),
            bg=PRIMARY_COLOR,
            fg="white",
            relief="flat",
            width=12,
            cursor="hand2",
            command=self.validar_login
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            btn_frame,
            text="Salir",
            font=("Segoe UI", 10, "bold"),
            bg=BTN_DANGER,
            fg="white",
            relief="flat",
            width=12,
            cursor="hand2",
            command=self.destroy
        ).grid(row=0, column=1, padx=10)

        self.entry_usuario.focus_set()

    def validar_login(self):

        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_pass.get().strip()

        if not usuario or not contrasena:
            messagebox.showwarning(
                "Campos vacíos",
                "Por favor, ingresa el usuario y la contraseña."
            )
            return

        # Acceso de administrador
        if usuario == "admin" and contrasena == "1234":

            self.rol_actual = "admin"
            self.empleado_actual = None

            self.mostrar_dashboard()
            return

        # Acceso de empleados
        try:
            id_empleado = int(usuario)
        except ValueError:
            messagebox.showerror(
                "Acceso denegado",
                "El usuario debe ser un ID de empleado válido."
            )
            return

        conexion = None
        cursor = None

        try:
            conexion = conectar_bd()

            if conexion is None:
                return

            cursor = conexion.cursor()

            cursor.execute("""
                SELECT id_empleado, nombre_comp
                FROM public.empleado
                WHERE id_empleado = %s
                AND contrasena = %s;
            """, (id_empleado, contrasena))

            empleado = cursor.fetchone()

            if empleado:

                self.rol_actual = "empleado"

                self.empleado_actual = {
                    "id_empleado": empleado[0],
                    "nombre_comp": empleado[1]
                }

                self.mostrar_dashboard()

            else:
                messagebox.showerror(
                    "Acceso denegado",
                    "Usuario o contraseña incorrectos."
                )

        except Exception as error:
            messagebox.showerror(
                "Error de conexión",
                f"No se pudo validar el acceso:\n\n{error}"
            )

        finally:
            if cursor:
                cursor.close()

            if conexion:
                conexion.close()