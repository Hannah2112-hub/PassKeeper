import tkinter as tk
from tkinter import messagebox
from src.logica.gestion import usuarios, validar_contraseña
from src.logica.cifrado import generar_clave, cifrar_contraseña
import re


def validar_correo(correo):
    """Valida que el correo tenga un formato válido."""
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(patron, correo)


def abrir_registro(ventana_login):
    """Abre la ventana de registro de usuario."""
    ventana_registro = tk.Toplevel(ventana_login)
    ventana_registro.title("Registro de Usuario")
    ventana_registro.geometry("400x300")
    ventana_registro.configure(bg="#2E3B55")

    tk.Label(ventana_registro, text="Registro de Usuario", font=("Arial", 16), fg="white", bg="#2E3B55").pack(pady=10)

    tk.Label(ventana_registro, text="Usuario:", font=("Arial", 12), fg="white", bg="#2E3B55").pack(pady=5)
    entry_usuario_registro = tk.Entry(ventana_registro)
    entry_usuario_registro.pack()

    tk.Label(ventana_registro, text="Correo Electrónico:", font=("Arial", 12), fg="white", bg="#2E3B55").pack(pady=5)
    entry_email_registro = tk.Entry(ventana_registro)
    entry_email_registro.pack()

    tk.Label(ventana_registro, text="Contraseña:", font=("Arial", 12), fg="white", bg="#2E3B55").pack(pady=5)
    entry_password_registro = tk.Entry(ventana_registro, show="*")
    entry_password_registro.pack()

    def registrar_usuario():
        nombre_usuario = entry_usuario_registro.get().strip()
        correo = entry_email_registro.get().strip()
        contraseña = entry_password_registro.get().strip()

        if not nombre_usuario or not correo or not contraseña:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if not validar_correo(correo):
            messagebox.showerror("Error", "El correo electrónico no es válido.")
            return

        if nombre_usuario in usuarios:
            messagebox.showerror("Error", "El usuario ya está registrado.")
            return

        if not validar_contraseña(contraseña):
            messagebox.showerror("Error", "La contraseña debe tener al menos 8 caracteres, incluir mayúsculas, minúsculas, números y caracteres especiales.")
            return

        clave_usuario = generar_clave()
        usuarios[nombre_usuario] = {
            "contraseña": cifrar_contraseña(contraseña, clave_usuario),
            "correo": correo,
            "clave": clave_usuario
        }

        ventana_registro.destroy()
        messagebox.showinfo("Éxito", "Usuario registrado exitosamente.")

    tk.Button(ventana_registro, text="Registrar", command=registrar_usuario, bg="#4CAF50", fg="white").pack(pady=10)