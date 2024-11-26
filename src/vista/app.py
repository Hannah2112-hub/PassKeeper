import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from sqlalchemy.orm import sessionmaker
from src.DATABASE.DB import setup_database, Contrasena
from src.logica.gestion import guardar_contraseña, obtener_contraseñas_por_usuario, descifrar_contraseña_usuario
from src.logica.cifrado import cifrar_contraseña  # Necesario para cifrar la nueva contraseña

# Configuración de la base de datos
engine = setup_database()
Session = sessionmaker(bind=engine)
session = Session()

def abrir_aplicacion(usuario_actual):
    """Abre la ventana principal de la aplicación."""
    app = tk.Tk()
    app.title("Gestor de Contraseñas")
    app.geometry("800x600")
    app.configure(bg="#2E3B55")

    tk.Label(app, text=f"Bienvenido, {usuario_actual.nombre}", font=("Arial", 20), fg="#FFD700", bg="#2E3B55").pack(pady=20)

    # Configurar la tabla de contraseñas
    frame_tabla = tk.Frame(app, bg="#2E3B55")
    frame_tabla.pack(pady=10, fill=tk.BOTH, expand=True)

    columnas = ("sitio", "usuario", "contraseña", "categoria")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)
    tabla.heading("sitio", text="Sitio Web")
    tabla.heading("usuario", text="Usuario")
    tabla.heading("contraseña", text="Contraseña")
    tabla.heading("categoria", text="Categoría")
    tabla.column("sitio", width=250, anchor="center")
    tabla.column("usuario", width=200, anchor="center")
    tabla.column("contraseña", width=200, anchor="center")
    tabla.column("categoria", width=150, anchor="center")
    tabla.pack(fill=tk.BOTH, expand=True)

    # Funciones principales
    def actualizar_tabla():
        """Carga las contraseñas desde la base de datos y actualiza la tabla."""
        tabla.delete(*tabla.get_children())
        contraseñas = obtener_contraseñas_por_usuario(session, usuario_actual.id)
        if not contraseñas:
            tabla.insert("", "end", values=("No hay contraseñas", "", "", ""))
        else:
            for c in contraseñas:
                tabla.insert("", "end", values=(c["sitio"], c["usuario"], "*******", c["categoria"]))

    def guardar_contraseña_evento():
        """Guarda una nueva contraseña en la base de datos."""
        sitio = entry_sitio.get().strip()
        usuario_sitio = entry_usuario_sitio.get().strip()
        contraseña_sitio = entry_contraseña_sitio.get().strip()
        categoria = categoria_combobox.get().strip()

        if not sitio or not usuario_sitio or not contraseña_sitio or not categoria:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            mensaje = guardar_contraseña(session, usuario_actual.id, sitio, usuario_sitio, contraseña_sitio, categoria)
            messagebox.showinfo("Éxito", mensaje)
            actualizar_tabla()
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar la contraseña: {e}")

    def ver_contraseña_evento():
        """Descifra y muestra la contraseña del sitio seleccionado."""
        seleccionado = tabla.focus()
        if seleccionado:
            sitio = tabla.item(seleccionado)["values"][0]
            try:
                contraseña_descifrada = descifrar_contraseña_usuario(session, usuario_actual.id, sitio)
                messagebox.showinfo("Contraseña", f"Contraseña para {sitio}: {contraseña_descifrada}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al descifrar la contraseña: {e}")

    def editar_contraseña_evento():
        """Permite editar la contraseña de un sitio seleccionado."""
        seleccionado = tabla.focus()  # Obtener el elemento seleccionado en la tabla
        if not seleccionado:
            messagebox.showerror("Error", "Por favor, selecciona una contraseña para editar.")
            return

        sitio = tabla.item(seleccionado)["values"][0]  # Obtenemos el sitio web de la fila seleccionada

        # Cuadro de diálogo para ingresar la nueva contraseña
        nueva_contraseña = simpledialog.askstring(
            "Editar Contraseña",
            f"Ingrese la nueva contraseña para el sitio: {sitio}",
            show="*"
        )

        if not nueva_contraseña:
            messagebox.showerror("Error", "La contraseña no puede estar vacía.")
            return

        try:
            # Buscar la contraseña en la base de datos
            contrasena_obj = session.query(Contrasena).filter_by(usuario_id=usuario_actual.id, sitio_web=sitio).first()
            if not contrasena_obj:
                messagebox.showerror("Error", "No se encontró la contraseña en la base de datos.")
                return

            # Cifrar la nueva contraseña y actualizarla en la base de datos
            contrasena_obj.contrasena_encriptada = cifrar_contraseña(nueva_contraseña, usuario_actual.clave)
            session.commit()

            messagebox.showinfo("Éxito", f"La contraseña para {sitio} ha sido actualizada.")
            actualizar_tabla()  # Refrescar la tabla
        except Exception as e:
            session.rollback()
            messagebox.showerror("Error", f"Error al actualizar la contraseña: {e}")

    def eliminar_contraseña_evento():
        """Permite eliminar una contraseña seleccionada."""
        seleccionado = tabla.focus()  # Obtener el elemento seleccionado en la tabla
        if not seleccionado:
            messagebox.showerror("Error", "Por favor, selecciona una contraseña para eliminar.")
            return

        sitio = tabla.item(seleccionado)["values"][0]  # Obtenemos el sitio web de la fila seleccionada

        # Confirmar eliminación
        confirmacion = messagebox.askyesno(
            "Eliminar Contraseña",
            f"¿Estás seguro de que deseas eliminar la contraseña para el sitio: {sitio}?"
        )

        if not confirmacion:
            return

        try:
            # Buscar y eliminar la contraseña en la base de datos
            contrasena_obj = session.query(Contrasena).filter_by(usuario_id=usuario_actual.id, sitio_web=sitio).first()
            if not contrasena_obj:
                messagebox.showerror("Error", "No se encontró la contraseña en la base de datos.")
                return

            session.delete(contrasena_obj)
            session.commit()

            messagebox.showinfo("Éxito", f"La contraseña para {sitio} ha sido eliminada.")
            actualizar_tabla()  # Refrescar la tabla
        except Exception as e:
            session.rollback()
            messagebox.showerror("Error", f"Error al eliminar la contraseña: {e}")

    # Entradas y botones
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

    tk.Label(frame_entradas, text="Categoría:", bg="#2E3B55", fg="white").grid(row=1, column=2, padx=5)
    categorias = ["Trabajo", "Personal", "Redes Sociales", "Bancos", "Otros"]
    categoria_combobox = ttk.Combobox(frame_entradas, values=categorias, state="readonly")
    categoria_combobox.grid(row=1, column=3, padx=5)
    categoria_combobox.set("Otros")

    frame_botones = tk.Frame(app, bg="#2E3B55")
    frame_botones.pack(pady=10)

    tk.Button(frame_botones, text="Guardar Contraseña", command=guardar_contraseña_evento, bg="#4CAF50", fg="white", width=20).grid(row=0, column=0, padx=10)
    tk.Button(frame_botones, text="Ver Contraseña", command=ver_contraseña_evento, bg="#FFA500", fg="white", width=20).grid(row=0, column=1, padx=10)
    tk.Button(frame_botones, text="Editar Contraseña", command=editar_contraseña_evento, bg="#FFA500", fg="white", width=20).grid(row=0, column=2, padx=10)
    tk.Button(
        frame_botones,
        text="Eliminar Contraseña",
        command=eliminar_contraseña_evento,
        bg="#FF4500",
        fg="white",
        width=20
    ).grid(row=0, column=3, padx=10)

    # Inicializar tabla
    actualizar_tabla()
    app.mainloop()
