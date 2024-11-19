import tkinter as tk
from tkinter import messagebox
from src.vista.registro import abrir_registro
from src.vista.app import abrir_aplicacion
from src.logica.gestion import usuarios


def abrir_login():
    """Abre la ventana de inicio de sesión."""
    ventana_login = tk.Tk()
    ventana_login.title("Inicio de Sesión")
    ventana_login.geometry("400x300")

    tk.Label(ventana_login, text="Usuario:").pack(pady=5)
    entry_usuario_login = tk.Entry(ventana_login)
    entry_usuario_login.pack()

    tk.Label(ventana_login, text="Contraseña:").pack(pady=5)
    entry_password_login = tk.Entry(ventana_login, show="*")
    entry_password_login.pack()

    def iniciar_sesion():
        nombre_usuario = entry_usuario_login.get()
        contraseña = entry_password_login.get()

        if nombre_usuario in usuarios and usuarios[nombre_usuario]["contraseña"] == contraseña:
            messagebox.showinfo("Éxito", f"Bienvenido, {nombre_usuario}!")
            ventana_login.destroy()
            abrir_aplicacion(nombre_usuario)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.")

    tk.Button(ventana_login, text="Iniciar Sesión", command=iniciar_sesion).pack(pady=10)
    tk.Button(ventana_login, text="Registrarse", command=lambda: abrir_registro(ventana_login)).pack(pady=10)

    ventana_login.mainloop()
