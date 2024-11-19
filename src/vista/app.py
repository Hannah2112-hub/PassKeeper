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

    # Título principal
    tk.Label(app, text="Gestor de Contraseñas", font=("Arial", 20), fg="#FFD700", bg="#2E3B55").pack(pady=20)

    # Configurar el cierre automático basado en el tiempo de inactividad
    def configurar_tiempo_inactividad():
        global tiempo_inactividad
        tiempo = simpledialog.askinteger("Tiempo de Inactividad", "Ingrese el tiempo de inactividad (en minutos):",
                                         minvalue=1, maxvalue=60)
        if tiempo:
            tiempo_inactividad = tiempo * 60000  # Convertir minutos a milisegundos
            messagebox.showinfo("Configuración Actualizada",
                                f"El tiempo de inactividad se ha configurado a {tiempo} minutos.")

    def reiniciar_temporizador():
        app.after_cancel(app.after_id)
        iniciar_temporizador()

    def iniciar_temporizador():
        app.after_id = app.after(tiempo_inactividad, cierre_automatico)

    def cierre_automatico():
        messagebox.showinfo("Cierre Automático", "La aplicación se cerrará por inactividad.")
        app.destroy()

    # Confirmar salida manual
    def confirmar_salida():
        if messagebox.askyesno("Confirmar Cierre", "¿Estás seguro de que deseas cerrar la aplicación?"):
            app.destroy()

    app.protocol("WM_DELETE_WINDOW", confirmar_salida)

    # Función para actualizar la tabla
    def actualizar_tabla():
        tabla.delete(*tabla.get_children())
        contraseñas_ordenadas = obtener_contraseñas_ordenadas()
        if not contraseñas_ordenadas:
            tabla.insert("", "end", values=("No hay contraseñas", "", ""))
        else:
            for sitio, datos in contraseñas_ordenadas.items():
                tabla.insert("", "end", values=(sitio, datos["usuario"], "********"))

    # Obtener el sitio seleccionado en la tabla
    def obtener_sitio_seleccionado():
        seleccionado = tabla.focus()
        if seleccionado:
            return tabla.item(seleccionado)["values"][0]
        return None

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
            # Solicitar la contraseña maestra
            clave_ingresada = simpledialog.askstring("Ver Contraseña", "Ingrese su contraseña maestra:", show="*")
            clave_usuario = usuarios[usuario_actual]["clave"]

            if clave_ingresada and clave_ingresada == clave_usuario.decode():
                # Si la contraseña es correcta, mostrar la contraseña descifrada
                contraseña_descifrada = descifrar_contraseña(contraseñas[sitio]["contraseña"], clave_usuario)
                messagebox.showinfo("Contraseña", f"La contraseña para {sitio} es: {contraseña_descifrada}")
            else:
                messagebox.showerror("Error", "Contraseña maestra incorrecta.")

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
        if sitio and messagebox.askyesno("Confirmar Eliminación", f"¿Eliminar contraseña para {sitio}?"):
            del contraseñas[sitio]
            actualizar_tabla()

    # Cambiar clave de usuario
    def cambiar_clave_usuario():
        clave_antigua = simpledialog.askstring("Cambiar Clave", "Ingrese su clave actual:", show="*")
        clave_actual = usuarios[usuario_actual]["clave"]
        if clave_antigua and clave_antigua == clave_actual.decode():
            nueva_clave = simpledialog.askstring("Nueva Clave", "Ingrese su nueva clave:", show="*")
            confirmar_clave = simpledialog.askstring("Confirme Clave", "Confirme la nueva clave:", show="*")
            if nueva_clave and nueva_clave == confirmar_clave:
                nueva_clave_generada = generar_clave()
                usuarios[usuario_actual]["clave"] = nueva_clave_generada
                for sitio, datos in contraseñas.items():
                    contraseña_descifrada = descifrar_contraseña(datos["contraseña"], clave_actual)
                    datos["contraseña"] = cifrar_contraseña(contraseña_descifrada, nueva_clave_generada)
                messagebox.showinfo("Clave Actualizada", "La clave se actualizó exitosamente.")
            else:
                messagebox.showerror("Error", "Las claves no coinciden.")
        else:
            messagebox.showerror("Error", "Clave actual incorrecta.")

    # Generar contraseña segura
    def generar_contraseña(longitud=12):
        """Genera una contraseña segura con una longitud dada."""
        if longitud < 4:
            raise ValueError("La longitud mínima debe ser 4.")
        caracteres = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choices(caracteres, k=longitud))
        messagebox.showinfo("Contraseña Generada", f"Tu nueva contraseña es: {password}")

    # Entradas de datos
    frame_entradas = tk.Frame(app, bg="#2E3B55")
    frame_entradas.pack(pady=5)
    tk.Label(frame_entradas, text="Sitio Web:", bg="#2E3B55", fg="white").grid(row=0, column=0, padx=5)
    entry_sitio = tk.Entry(frame_entradas)
    entry_sitio.grid(row=0, column=1, padx=5)
    tk.Label(frame_entradas, text="Usuario:", bg="#2E3B55", fg="white").grid(row=0, column=2, padx=5)
    entry_usuario_sitio = tk.Entry(frame_entradas)
    entry_usuario_sitio.grid(row=0, column=3, padx=5)
    tk.Label(frame_entradas, text="Contraseña:", bg="#2E3B55", fg="white").grid(row=1, column=0, padx=5)
    entry_contraseña_sitio = tk.Entry(frame_entradas, show="*")
    entry_contraseña_sitio.grid(row=1, column=1, padx=5)

    # Botones de gestión de contraseñas
    frame_contraseñas = tk.LabelFrame(app, text="Gestión de Contraseñas", bg="#2E3B55", fg="white")
    frame_contraseñas.pack(pady=10)

    tk.Button(frame_contraseñas, text="Guardar", command=guardar_contraseña, bg="#4CAF50", fg="white", width=15).grid(
        row=0, column=0, padx=10, pady=5)
    tk.Button(frame_contraseñas, text="Ver Contraseña", command=ver_contraseña_segura, bg="#FFA500", fg="white",
              width=15).grid(row=0, column=1, padx=10, pady=5)
    tk.Button(frame_contraseñas, text="Editar", command=editar_contraseña, bg="#FFA500", fg="white", width=15).grid(
        row=0, column=2, padx=10, pady=5)
    tk.Button(frame_contraseñas, text="Eliminar", command=eliminar_contraseña, bg="#FF4500", fg="white", width=15).grid(
        row=0, column=3, padx=10, pady=5)

    # Botones adicionales
    frame_adicionales = tk.LabelFrame(app, text="Opciones Adicionales", bg="#2E3B55", fg="white")
    frame_adicionales.pack(pady=10)

    tk.Button(frame_adicionales, text="Generar Contraseña", command=generar_contraseña, bg="#4CAF50", fg="white",
              width=20).grid(row=0, column=0, padx=10, pady=5)
    tk.Button(frame_adicionales, text="Cambiar Clave Usuario", command=cambiar_clave_usuario, bg="#FFA500", fg="white",
              width=20).grid(row=0, column=1, padx=10, pady=5)
    tk.Button(frame_adicionales, text="Configurar Inactividad", command=configurar_tiempo_inactividad, bg="#4CAF50",
              fg="white", width=20).grid(row=0, column=2, padx=10, pady=5)
    tk.Button(frame_adicionales, text="Cerrar", command=confirmar_salida, bg="#FF4500", fg="white", width=20).grid(
        row=0, column=3, padx=10, pady=5)

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

    # Inicialización
    actualizar_tabla()
    iniciar_temporizador()
    app.mainloop()
