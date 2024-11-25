import tkinter as tk
from tkinter import messagebox
from src.vista.registro import abrir_registro
from src.vista.app import abrir_aplicacion
from src.logica.cifrado import descifrar_contraseña
from src.DATABASE.DB import Usuario
from sqlalchemy.orm import sessionmaker
from src.DATABASE.DB import setup_database
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl

# Configuración de correo
USERNAME = "davidandreguevaramoscoso@gmail.com"
PASSWORD = "grdt bfrj zedj uxzg"  # Sustitúyelo por tu contraseña correcta
DESTINATARIO = "72508579@continental.edu.pe"

# Configurar conexión a la base de datos
engine = setup_database()
Session = sessionmaker(bind=engine)
session = Session()

def enviar_alerta_intentos():
    """Envía un correo de alerta por múltiples intentos fallidos."""
    asunto = "Alerta de Intentos Fallidos"
    mensaje = MIMEMultipart("alternative")
    mensaje["Subject"] = asunto
    mensaje["From"] = USERNAME
    mensaje["To"] = DESTINATARIO

    html = """
    <html>
    <body>
        Hola,<br>
        Se han registrado 5 intentos fallidos de inicio de sesión en el sistema.
    </body>
    </html>
    """
    mensaje.attach(MIMEText(html, "html"))

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(USERNAME, PASSWORD)
            server.sendmail(USERNAME, DESTINATARIO, mensaje.as_string())
            print("Correo de alerta enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

def abrir_login():
    """Abre la ventana de inicio de sesión."""
    ventana_login = tk.Tk()
    ventana_login.title("Inicio de Sesión")
    ventana_login.geometry("400x300")
    ventana_login.configure(bg="#2E3B55")

    intentos_fallidos = [0]  # Contador de intentos fallidos

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

        try:
            # Buscar el usuario en la base de datos
            usuario = session.query(Usuario).filter_by(nombre=nombre_usuario).first()

            if not usuario:
                messagebox.showerror("Error", "Usuario no encontrado.")
                return

            # Imprimir para depuración
            print(f"Contraseña ingresada: {contraseña}")
            print(f"Contraseña almacenada (cifrada): {usuario.contrasena_maestra}")

            # Aquí necesitamos la clave de cifrado que usaste al registrar al usuario
            clave_usuario = usuario.clave  # Esto asume que tienes un campo 'clave' en el modelo Usuario
            # Descifrar la contraseña almacenada
            contrasena_descifrada = descifrar_contraseña(usuario.contrasena_maestra, clave_usuario)
            print(f"Contraseña descifrada: {contrasena_descifrada}")

            # Comparar las contraseñas
            if contrasena_descifrada == contraseña:
                messagebox.showinfo("Éxito", f"Bienvenido, {nombre_usuario}!")
                ventana_login.destroy()  # Cierra la ventana de inicio de sesión
                abrir_aplicacion(nombre_usuario)  # Abre la aplicación principal
            else:
                messagebox.showerror("Error", "Contraseña incorrecta.")
                intentos_fallidos[0] += 1

        except Exception as e:
            print(f"Error al intentar iniciar sesión: {e}")
            messagebox.showerror("Error", "Ocurrió un error al intentar iniciar sesión.")

        # Si hay 5 intentos fallidos, enviar alerta
        if intentos_fallidos[0] == 5:
            enviar_alerta_intentos()  # Enviar correo de alerta
            messagebox.showwarning("Alerta", "Se han registrado 5 intentos fallidos. Se enviará una alerta.")
            intentos_fallidos[0] = 0  # Reinicia el contador tras enviar la alerta

    tk.Button(ventana_login, text="Iniciar Sesión", command=iniciar_sesion, bg="#4CAF50", fg="white").pack(pady=10)
    tk.Button(ventana_login, text="Registrarse", command=lambda: abrir_registro(ventana_login), bg="#FFA500", fg="white").pack(pady=10)

    ventana_login.mainloop()