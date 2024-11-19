import string
import random
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from src.logica.cifrado import cifrar_contraseña, descifrar_contraseña, generar_clave
from src.logica.gestion import contraseñas, usuarios, obtener_contraseñas_ordenadas


def abrir_aplicacion(usuario_actual):
    """Abre la aplicación principal."""
    app = tk.Tk()
    app.title("Gestor de Contraseñas")
    app.geometry("800x600")
    app.configure(bg="#2E3B55")

    # Función auxiliar para obtener el sitio seleccionado
    def obtener_sitio_seleccionado():
        """Obtiene el sitio seleccionado de la tabla."""
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showerror("Error", "Seleccione una contraseña.")
            return None
        item = tabla.item(seleccion)
        sitio = item["values"][0]
        if sitio == "No hay contraseñas":
            messagebox.showerror("Error", "No hay contraseñas seleccionadas.")
            return None
        return sitio

    # Confirmar salida
    def cierre_automatico():
        app.destroy()

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

    # Botones
    frame_botones = tk.Frame(app, bg="#2E3B55")
    frame_botones.pack(pady=10)

    tk.Button(frame_botones, text="Guardar", command=lambda: guardar_contraseña(), bg="#4CAF50", fg="white", width=15).grid(row=0, column=0, padx=5)
    tk.Button(frame_botones, text="Ver Contraseña", command=lambda: ver_contraseña(), bg="#FFA500", fg="white", width=15).grid(row=0, column=1, padx=5)
    tk.Button(frame_botones, text="Editar", command=lambda: editar_contraseña(), bg="#FFA500", fg="white", width=15).grid(row=0, column=2, padx=5)
    tk.Button(frame_botones, text="Eliminar", command=lambda: eliminar_contraseña(), bg="#FF4500", fg="white", width=15).grid(row=0, column=3, padx=5)
    tk.Button(frame_botones, text="Cambiar Clave", command=lambda: cambiar_clave(), bg="#4CAF50", fg="white", width=15).grid(row=0, column=4, padx=5)
    tk.Button(frame_botones, text="Cerrar", command=lambda: confirmar_salida(), bg="#FF4500", fg="white", width=15).grid(row=0, column=5, padx=5)
    tk.Button(frame_botones, text="Generar contraseñas", command=lambda: generar_contraseña(), bg="#4CAF50", fg="white", width=15).grid(row=1, column=0, padx=5)

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

    def ver_contraseña():
        sitio = obtener_sitio_seleccionado()
        if sitio:
            clave_usuario = usuarios[usuario_actual]["clave"]
            contraseña_descifrada = descifrar_contraseña(contraseñas[sitio]["contraseña"], clave_usuario)
            messagebox.showinfo("Contraseña", f"La contraseña para {sitio} es: {contraseña_descifrada}")

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

    def cambiar_clave():
        if messagebox.askyesno("Confirmar Cambio", "¿Cambiar clave de encriptación?"):
            nueva_clave = generar_clave()
            clave_antigua = usuarios[usuario_actual]["clave"]
            usuarios[usuario_actual]["clave"] = nueva_clave
            for sitio, datos in contraseñas.items():
                contraseña_descifrada = descifrar_contraseña(datos["contraseña"], clave_antigua)
                datos["contraseña"] = cifrar_contraseña(contraseña_descifrada, nueva_clave)
            actualizar_tabla()

    def generar_contraseña(longitud=12):
        if messagebox.askyesno("Generacion de contraseña", "¿Generar contraseña?"):
            if longitud < 4:
                raise ValueError(
                    "La longitud de la contraseña debe ser al menos 4 caracteres para cumplir todos los requisitos.")
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

            # Crear una nueva ventana para mostrar y copiar la contraseña
            password_window = tk.Toplevel()
            password_window.title("Contraseña Generada")

            label = tk.Label(password_window, text=f"Contraseña generada: {generated_password}", font=("Arial", 14))
            label.pack(padx=20, pady=20)

            def copiar_al_portapapeles():
                password_window.clipboard_clear()
                password_window.clipboard_append(generated_password)
                messagebox.showinfo("Información", "Contraseña copiada al portapapeles")

            boton_copiar = tk.Button(password_window, text="Copiar contraseña", command=copiar_al_portapapeles)
            boton_copiar.pack(pady=10)

            return generated_password

    # Ejemplo de cómo se llamaría la función dentro de otro entorno
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    generar_contraseña()

    # Inicializar tabla
    actualizar_tabla()

    # Cerrar la aplicación después de 1 minuto
    app.after(60000, cierre_automatico)

    app.mainloop()
