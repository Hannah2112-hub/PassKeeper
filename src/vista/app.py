import string
import random
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from src.logica.cifrado import cifrar_contraseña, descifrar_contraseña, generar_clave
from src.logica.gestion import contraseñas, usuarios, obtener_contraseñas_ordenadas

# Variable para el tiempo de inactividad en milisegundos
tiempo_inactividad = 300000  # 5 minutos por defecto

def abrir_aplicacion(usuario_actual):
    """Abre la aplicación principal."""
    app = tk.Tk()
    app.title("Gestor de Contraseñas")
    app.geometry("800x600")
    app.configure(bg="#2E3B55")

    # Configurar el cierre automático basado en el tiempo de inactividad
    def configurar_tiempo_inactividad():
        global tiempo_inactividad
        tiempo = simpledialog.askinteger("Tiempo de Inactividad", "Ingrese el tiempo de inactividad (en minutos):", minvalue=1, maxvalue=60)
        if tiempo:
            tiempo_inactividad = tiempo * 60000  # Convertir minutos a milisegundos
            messagebox.showinfo("Configuración Actualizada", f"El tiempo de inactividad se ha configurado a {tiempo} minutos.")

    # Reiniciar el temporizador de inactividad
    def reiniciar_temporizador():
        app.after_cancel(app.after_id)
        iniciar_temporizador()

    # Iniciar el temporizador de inactividad
    def iniciar_temporizador():
        app.after_id = app.after(tiempo_inactividad, cierre_automatico)

    # Función para cerrar la aplicación automáticamente después del tiempo de inactividad
    def cierre_automatico():
        messagebox.showinfo("Cierre Automático", "La aplicación se cerrará debido a inactividad.")
        app.destroy()

    # Confirmar salida
    def confirmar_salida():
        if messagebox.askyesno("Confirmar Cierre", "¿Estás seguro de que deseas cerrar la aplicación?"):
            app.destroy()

    app.protocol("WM_DELETE_WINDOW", confirmar_salida)

    # Bienvenida
    tk.Label(app, text=f"Bienvenido, {usuario_actual}", font=("Arial", 18), fg="#FFD700", bg="#2E3B55").pack(pady=10)

    # Entradas y etiquetas
    frame_entradas = tk.Frame(app, bg="#2E3B55")
    frame_entradas.pack(pady=5)

    tk.Label(frame_entradas, text="Sitio Web:", font=("Arial", 12), fg="white", bg="#2E3B55").grid(row=0, column=0, padx=5, pady=5)
    entry_sitio = tk.Entry(frame_entradas, width=30)
    entry_sitio.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_entradas, text="Usuario:", font=("Arial", 12), fg="white", bg="#2E3B55").grid(row=0, column=2, padx=5, pady=5)
    entry_usuario_sitio = tk.Entry(frame_entradas, width=30)
    entry_usuario_sitio.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(frame_entradas, text="Contraseña:", font=("Arial", 12), fg="white", bg="#2E3B55").grid(row=1, column=0, padx=5, pady=5)
    entry_contraseña_sitio = tk.Entry(frame_entradas, width=30, show="*")
    entry_contraseña_sitio.grid(row=1, column=1, padx=5, pady=5)

    # Botones agrupados por funcionalidad
    frame_botones = tk.Frame(app, bg="#2E3B55")
    frame_botones.pack(pady=10)

    # Botones de contraseñas
    frame_contraseñas = tk.LabelFrame(frame_botones, text="Gestión de Contraseñas", bg="#2E3B55", fg="white")
    frame_contraseñas.pack(side=tk.LEFT, padx=10, pady=5)

    tk.Button(frame_contraseñas, text="Guardar", command=lambda: [guardar_contraseña(), reiniciar_temporizador()], bg="#4CAF50", fg="white", width=15).pack(pady=5)
    tk.Button(frame_contraseñas, text="Ver Contraseña", command=lambda: [ver_contraseña_segura(), reiniciar_temporizador()], bg="#FFA500", fg="white", width=15).pack(pady=5)
    tk.Button(frame_contraseñas, text="Editar", command=lambda: [editar_contraseña(), reiniciar_temporizador()], bg="#FFA500", fg="white", width=15).pack(pady=5)
    tk.Button(frame_contraseñas, text="Eliminar", command=lambda: [eliminar_contraseña(), reiniciar_temporizador()], bg="#FF4500", fg="white", width=15).pack(pady=5)

    # Botones adicionales
    frame_adicionales = tk.LabelFrame(frame_botones, text="Opciones Adicionales", bg="#2E3B55", fg="white")
    frame_adicionales.pack(side=tk.RIGHT, padx=10, pady=5)

    tk.Button(frame_adicionales, text="Generar Contraseña", command=lambda: [generar_contraseña(), reiniciar_temporizador()], bg="#4CAF50", fg="white", width=20).pack(pady=5)
    tk.Button(frame_adicionales, text="Cambiar Clave Usuario", command=lambda: [cambiar_clave_usuario(), reiniciar_temporizador()], bg="#FFA500", fg="white", width=20).pack(pady=5)
    tk.Button(frame_adicionales, text="Configurar Inactividad", command=lambda: [configurar_tiempo_inactividad(), reiniciar_temporizador()], bg="#4CAF50", fg="white", width=20).pack(pady=5)
    tk.Button(frame_adicionales, text="Cerrar", command=lambda: confirmar_salida(), bg="#FF4500", fg="white", width=20).pack(pady=5)

    # Tabla de contraseñas
    frame_tabla = tk.Frame(app, bg="#2E3B55")
    frame_tabla.pack(pady=10, fill=tk.BOTH, expand=True)

    columnas = ("sitio", "usuario", "contraseña")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)
    tabla.heading("sitio", text="Sitio Web")
    tabla.heading("usuario", text="Usuario")
    tabla.heading("contraseña", text="Contraseña")
    tabla.column("sitio", width=250, anchor="center")
    tabla.column("usuario", width=200, anchor="center")
    tabla.column("contraseña", width=200, anchor="center")
    tabla.pack(fill=tk.BOTH, expand=True)

    estilo = ttk.Style()
    estilo.configure("Treeview", background="#1E2A38", foreground="white", rowheight=25, fieldbackground="#1E2A38")
    estilo.map("Treeview", background=[("selected", "#FFD700")])

    def actualizar_tabla():
        """Actualiza la tabla con las contraseñas."""
        for item in tabla.get_children():
            tabla.delete(item)
        contraseñas_ordenadas = obtener_contraseñas_ordenadas()
        if not contraseñas_ordenadas:
            tabla.insert("", "end", values=("No hay contraseñas", "", ""))
        else:
            for sitio, datos in contraseñas_ordenadas.items():
                tabla.insert("", "end", values=(sitio, datos["usuario"], "********"))

    # Funciones CRUD
    def guardar_contraseña():
        sitio = entry_sitio.get().strip()
        usuario_sitio = entry_usuario_sitio.get().strip()
        contraseña_sitio = entry_contraseña_sitio.get().strip()
        if not sitio or not usuario_sitio or not contraseña_sitio:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        clave_usuario = usuarios[usuario_actual]["clave"]
        contraseñas[sitio] = {
            "usuario": usuario_sitio,
            "contraseña": cifrar_contraseña(contraseña_sitio, clave_usuario),
        }
        actualizar_tabla()

    def ver_contraseña_segura():
        sitio = obtener_sitio_seleccionado()
        if sitio:
            clave_ingresada = simpledialog.askstring("Ver Contraseña", "Ingrese su clave principal:", show="*")
            clave_usuario = usuarios[usuario_actual]["clave"]
            if clave_ingresada and clave_ingresada == clave_usuario.decode():
                contraseña_descifrada = descifrar_contraseña(contraseñas[sitio]["contraseña"], clave_usuario)
                messagebox.showinfo("Contraseña", f"La contraseña para {sitio} es: {contraseña_descifrada}")

                # Volver a ocultar la contraseña después de 5 segundos
                app.after(5000, lambda: messagebox.showinfo("Contraseña", "La contraseña se ocultó nuevamente por seguridad"))
            else:
                messagebox.showerror("Error", "Clave principal incorrecta.")

    def editar_contraseña():
        sitio = obtener_sitio_seleccionado()
        if sitio:
            nueva_contraseña = simpledialog.askstring("Editar Contraseña", f"Ingrese nueva contraseña para {sitio}:")
            if nueva_contraseña:
                clave_usuario = usuarios[usuario_actual]["clave"]
                contraseñas[sitio]["contraseña"] = cifrar_contraseña(nueva_contraseña, clave_usuario)
                actualizar_tabla()

    def eliminar_contraseña():
        sitio = obtener_sitio_seleccionado()
        if sitio:
            if messagebox.askyesno("Confirmar Eliminación", f"¿Eliminar contraseña para {sitio}?"):
                del contraseñas[sitio]
                actualizar_tabla()

    def cambiar_clave_usuario():
        """Cambia la clave del usuario actual."""
        clave_antigua_ingresada = simpledialog.askstring("Cambiar Clave", "Ingrese su clave actual:", show="*")
        clave_usuario_actual = usuarios[usuario_actual]["clave"]

        if clave_antigua_ingresada and clave_antigua_ingresada == clave_usuario_actual.decode():
            nueva_clave = simpledialog.askstring("Cambiar Clave", "Ingrese la nueva clave de encriptación:", show="*")
            confirmar_clave = simpledialog.askstring("Cambiar Clave", "Confirme la nueva clave de encriptación:", show="*")

            if nueva_clave and nueva_clave == confirmar_clave:
                nueva_clave_generada = generar_clave()
                usuarios[usuario_actual]["clave"] = nueva_clave_generada

                # Actualizar todas las contraseñas con la nueva clave
                for sitio, datos in contraseñas.items():
                    contraseña_descifrada = descifrar_contraseña(datos["contraseña"], clave_usuario_actual)
                    datos["contraseña"] = cifrar_contraseña(contraseña_descifrada, nueva_clave_generada)

                messagebox.showinfo("Clave Actualizada", "La clave del usuario ha sido actualizada exitosamente.")
            else:
                messagebox.showerror("Error", "Las claves nuevas no coinciden. Intente nuevamente.")
        else:
            messagebox.showerror("Error", "Clave actual incorrecta.")

    def generar_contraseña(longitud=12):
        """Genera una contraseña segura con una longitud dada."""
        if longitud < 4:
            raise ValueError("La longitud mínima debe ser 4.")
        caracteres = string.ascii_letters + string.digits + string.punctuation

        password = [
            random.choice(string.ascii_uppercase),
            random.choice(string.ascii_lowercase),
            random.choice(string.digits),
            random.choice(string.punctuation)
        ]

        password += random.choices(caracteres, k=longitud - 4)
        random.shuffle(password)
        generated_password = ''.join(password)

        password_window = tk.Toplevel()
        password_window.title("Contraseña Generada")
        label = tk.Label(password_window, text=f"Contraseña generada: {generated_password}", font=("Arial", 14))
        label.pack(padx=20, pady=20)

        def copiar_al_portapapeles():
            password_window.clipboard_clear()
            password_window.clipboard_append(generated_password)
            messagebox.showinfo("Información", "Contraseña copiada al portapapeles")

        tk.Button(password_window, text="Copiar contraseña", command=copiar_al_portapapeles).pack(pady=10)

    # Inicializa la tabla con las contraseñas actuales
    actualizar_tabla()

    # Iniciar el temporizador de inactividad al abrir la aplicación
    iniciar_temporizador()
    app.mainloop()
