import tkinter as tk
from tkinter import messagebox
from src.logica.gestion import usuarios, validar_contraseña
from src.logica.cifrado import generar_clave


def abrir_registro(ventana_login):
    """Abre la ventana de registro de usuario."""
    ventana_registro = tk.Toplevel(ventana_login)
    ventana_registro.title("Registro de Usuario")
    ventana_registro.geometry("400x300")

    tk.Label(ventana_registro, text="Usuario:").pack(pady=5)
    entry_usuario_registro = tk.Entry(ventana_registro)
    entry_usuario_registro.pack()

    tk.Label(ventana_registro, text="Correo Electrónico:").pack(pady=5)
    entry_email_registro = tk.Entry(ventana_registro)
    entry_email_registro.pack()

    tk.Label(ventana_registro, text="Contraseña:").pack(pady=5)
    entry_password_registro = tk.Entry(ventana_registro, show="*")
    entry_password_registro.pack()

    def registrar_usuario():
        nombre_usuario = entry_usuario_registro.get()
        correo = entry_email_registro.get()
        contraseña = entry_password_registro.get()

        if not nombre_usuario or not correo or not contraseña:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if nombre_usuario in usuarios:
            messagebox.showerror("Error", "El usuario ya está registrado.")
            return

        if not validar_contraseña(contraseña):
            messagebox.showerror("Error", "La contraseña no cumple con los requisitos. Debe tener por lo menos 8 digitos, tambien mayuscolas y llevar caracteres especiales")  #cambio en mensaje
            return

        clave_usuario = generar_clave()
        usuarios[nombre_usuario] = {
            "contraseña": contraseña,
            "correo": correo,
            "clave": clave_usuario
        }
        ventana_registro.destroy()
        messagebox.showinfo("Éxito", "Usuario registrado exitosamente.")

    tk.Button(ventana_registro, text="Registrar", command=registrar_usuario).pack(pady=10)
