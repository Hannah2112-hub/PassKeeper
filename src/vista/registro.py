import tkinter as tk
from tkinter import messagebox
from sqlalchemy.orm import sessionmaker
from src.DATABASE.DB import setup_database, Usuario
from src.logica.cifrado import generar_clave, cifrar_contraseña
from src.logica.gestion import validar_contraseña
import re

# Configurar conexión a la base de datos
engine = setup_database()
Session = sessionmaker(bind=engine)
session = Session()

def validar_correo(correo):
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'
    if ".." in correo:
        return False
    return bool(re.match(patron, correo))

def abrir_registro(ventana_login):
    """Abre la ventana de registro de usuario."""
    ventana_registro = tk.Toplevel(ventana_login)
    ventana_registro.title("Registro de Usuario")
    ventana_registro.geometry("450x350")
    ventana_registro.configure(bg="#19222b")

    # Etiquetas y campos de entrada
    tk.Label(ventana_registro, text="Registro de Usuario", font=("constantia", 32, "bold"), fg="white", bg="#19222b").pack(pady=5)

    tk.Label(ventana_registro, text="Usuario:", font=("Constantia", 24), fg="#ddd6cc", bg="#19222b").pack(pady=5)
    entry_usuario_registro = tk.Entry(ventana_registro)
    entry_usuario_registro.pack()

    tk.Label(ventana_registro, text="Correo Electrónico:", font=("Constantia", 24), fg="#ddd6cc", bg="#19222b").pack(pady=5)
    entry_email_registro = tk.Entry(ventana_registro)
    entry_email_registro.pack()

    tk.Label(ventana_registro, text="Contraseña:", font=("Constantia", 24), fg="#ddd6cc", bg="#19222b").pack(pady=5)
    entry_password_registro = tk.Entry(ventana_registro, show="*")
    entry_password_registro.pack()

    def registrar_usuario():
        """Valida y registra un nuevo usuario en la base de datos."""
        nombre_usuario = entry_usuario_registro.get().strip()
        correo = entry_email_registro.get().strip()
        contraseña = entry_password_registro.get().strip()

        # Validaciones básicas
        if not nombre_usuario or not correo or not contraseña:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if not validar_correo(correo):
            messagebox.showerror("Error", "El correo electrónico no es válido.")
            return

        try:
            # Verificar si el usuario o correo ya existe en la base de datos
            usuario_existente = session.query(Usuario).filter(
                (Usuario.nombre == nombre_usuario) | (Usuario.email == correo)
            ).first()

            if usuario_existente:
                messagebox.showerror("Error", "El usuario o correo ya está registrado.")
                return

            # Validar la fortaleza de la contraseña
            if not validar_contraseña(contraseña):
                messagebox.showerror(
                    "Error",
                    "La contraseña debe tener al menos 8 caracteres, incluir mayúsculas, minúsculas, números y caracteres especiales."
                )
                return

            # Generar una clave única y cifrar la contraseña
            clave_usuario = generar_clave()  # Esta clave debe ser almacenada en la base de datos
            contraseña_cifrada = cifrar_contraseña(contraseña, clave_usuario)

            # Crear un nuevo usuario
            nuevo_usuario = Usuario(
                nombre=nombre_usuario,
                email=correo,
                contrasena_maestra=contraseña_cifrada,
                clave=clave_usuario  # Asegúrate de agregar este campo en el modelo Usuario
            )

            # Guardar el usuario en la base de datos
            session.add(nuevo_usuario)
            session.commit()  # Es importante realizar el commit para guardar los cambios

            # Cerrar la ventana de registro y mostrar un mensaje de éxito
            ventana_registro.destroy()
            messagebox.showinfo("Éxito", "Usuario registrado exitosamente.")

        except Exception as e:
            session.rollback()  # Deshacer cualquier cambio en caso de error
            print(f"Error al registrar el usuario: {e}")
            messagebox.showerror("Error", "Ocurrió un error al registrar el usuario. Inténtalo nuevamente.")

    # Botón para registrar al usuario
    tk.Button(ventana_registro, text="Registrar", command=registrar_usuario, font=("Constantia", 12), bg="#b84356", fg="white").pack(pady=15)