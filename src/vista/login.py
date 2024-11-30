import tkinter as tk
from tkinter import messagebox
from src.DATABASE.DB import setup_database, Usuario
from src.vista.app import abrir_aplicacion
from src.vista.registro import abrir_registro  # Importar la función de registro
from src.logica.cifrado import descifrar_contraseña
from sqlalchemy.orm import sessionmaker

# Configuración de la base de datos
engine = setup_database()
Session = sessionmaker(bind=engine)
session = Session()

def abrir_login():
    """Abre la ventana de inicio de sesión."""
    ventana_login = tk.Tk()
    ventana_login.title("Inicio de Sesión")
    ventana_login.geometry("450x380")
    ventana_login.configure(bg="#19222b")

    tk.Label(ventana_login, text="Inicio de Sesión", font=("Constantia", 32, "bold"), fg="white", bg="#19222b").pack(pady=10)

    tk.Label(ventana_login, text="Usuario:", font=("Constantia", 24), fg="#ddd6cc", bg="#19222b").pack(pady=5)
    entry_usuario = tk.Entry(ventana_login)
    entry_usuario.pack()

    tk.Label(ventana_login, text="Contraseña:", font=("Constantia", 24 ), fg="#ddd6cc", bg="#19222b").pack(pady=5)
    entry_password = tk.Entry(ventana_login, show="*")
    entry_password.pack()

    def iniciar_sesion():
        """Valida el inicio de sesión del usuario."""
        nombre_usuario = entry_usuario.get().strip()
        contraseña = entry_password.get().strip()

        if not nombre_usuario or not contraseña:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            # Buscar usuario en la base de datos
            usuario = session.query(Usuario).filter_by(nombre=nombre_usuario).first()
            if not usuario:
                messagebox.showerror("Error", "Usuario no encontrado.")
                return

            # Descifrar la contraseña maestra del usuario
            contrasena_descifrada = descifrar_contraseña(usuario.contrasena_maestra, usuario.clave)

            if contrasena_descifrada == contraseña:
                messagebox.showinfo("Éxito", f"Bienvenido, {nombre_usuario}!")
                ventana_login.destroy()
                abrir_aplicacion(usuario)  # Abre la ventana principal
            else:
                messagebox.showerror("Error", "Contraseña incorrecta.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar sesión: {e}")

    def registrar_usuario():
        """Abre la ventana de registro de usuario."""
        abrir_registro(None)  # Llama a la función de registro

    tk.Button(ventana_login, text="Iniciar Sesión", command=iniciar_sesion, font=("Constantia", 12), bg="#bd9341", fg="white").pack(pady=15)
    tk.Button(ventana_login, text="Registrarse", command=registrar_usuario, font=("Constantia", 12), bg="#b84356", fg="white").pack(pady=0) # Botón para registro

    ventana_login.mainloop()