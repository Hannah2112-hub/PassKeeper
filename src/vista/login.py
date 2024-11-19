import tkinter as tk
from tkinter import messagebox
from src.vista.registro import abrir_registro
from src.vista.app import abrir_aplicacion
from src.logica.gestion import usuarios
from src.logica.cifrado import descifrar_contraseña


def abrir_login():
    """Abre la ventana de inicio de sesión."""
    ventana_login = tk.Tk()
    ventana_login.title("Inicio de Sesión")
    ventana_login.geometry("400x300")
    ventana_login.configure(bg="#2E3B55")

    tk.Label(ventana_login, text="Inicio de Sesión", font=("Arial", 16), fg="white", bg="#2E3B55").pack(pady=10)

    tk.Label(ventana_login, text="Usuario:", font=("Arial", 12), fg="white", bg="#2E3B55").pack(pady=5)
    entry_usuario_login = tk.Entry(ventana_login)
    entry_usuario_login.pack()

    tk.Label(ventana_login, text="Contraseña:", font=("Arial", 12), fg="white", bg="#2E3B55").pack(pady=5)
    entry_password_login = tk.Entry(ventana_login, show="*")
    entry_password_login.pack()

    def iniciar_sesion():
        nombre_usuario = entry_usuario_login.get().strip()
        contraseña = entry_password_login.get().strip()

        if not nombre_usuario or not contraseña:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if nombre_usuario in usuarios:
            clave = usuarios[nombre_usuario]["clave"]
            contraseña_almacenada = usuarios[nombre_usuario]["contraseña"]
            if descifrar_contraseña(contraseña_almacenada, clave) == contraseña:
                messagebox.showinfo("Éxito", f"Bienvenido, {nombre_usuario}!")
                ventana_login.destroy()  # Cierra la ventana de inicio de sesión
                abrir_aplicacion(nombre_usuario)  # Abre la aplicación principal
                return

        messagebox.showerror("Error", "Credenciales incorrectas.")

    tk.Button(ventana_login, text="Iniciar Sesión", command=iniciar_sesion, bg="#4CAF50", fg="white").pack(pady=10)
    tk.Button(ventana_login, text="Registrarse", command=lambda: abrir_registro(ventana_login), bg="#FFA500", fg="white").pack(pady=10)

    ventana_login.mainloop()
