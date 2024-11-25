import tkinter as tk
from tkinter import messagebox
from src.vista.registro import abrir_registro
from src.vista.app import abrir_aplicacion
from src.logica.gestion import usuarios
from src.logica.cifrado import descifrar_contraseña
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl

# Configuración de correo
USERNAME = "davidandreguevaramoscoso@gmail.com"
PASSWORD = "grdt bfrj zedj uxzg"  # Sustitauye esto por tu contraseña correcta
DESTINATARIO = "72508579@continental.edu.pe"


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

        if nombre_usuario in usuarios:
            clave = usuarios[nombre_usuario]["clave"]
            contraseña_almacenada = usuarios[nombre_usuario]["contraseña"]
            if descifrar_contraseña(contraseña_almacenada, clave) == contraseña:
                messagebox.showinfo("Éxito", f"Bienvenido, {nombre_usuario}!")
                ventana_login.destroy()  # Cierra la ventana de inicio de sesión
                abrir_aplicacion(nombre_usuario)  # Abre la aplicación principal
                return

        # Incrementa el contador de intentos fallidos
        intentos_fallidos[0] += 1
        messagebox.showerror("Error", f"Credenciales incorrectas. Intentos fallidos: {intentos_fallidos[0]}")

        if intentos_fallidos[0] == 5:
            enviar_alerta_intentos()  # Enviar correo de alerta
            messagebox.showwarning("Alerta", "Se han registrado 5 intentos fallidos. Se enviará una alerta.")
            intentos_fallidos[0] = 0  # Reinicia el contador tras enviar la alerta

    tk.Button(ventana_login, text="Iniciar Sesión", command=iniciar_sesion, bg="#4CAF50", fg="white").pack(pady=10)
    tk.Button(ventana_login, text="Registrarse", command=lambda: abrir_registro(ventana_login), bg="#FFA500", fg="white").pack(pady=10)

    ventana_login.mainloop()