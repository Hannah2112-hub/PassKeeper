import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from sqlalchemy.orm import sessionmaker
from src.DATABASE.DB import setup_database, Contrasena
from src.logica.gestion import guardar_contraseña, obtener_contraseñas_por_usuario, descifrar_contraseña_usuario
from src.logica.cifrado import cifrar_contraseña  # Necesario para cifrar la nueva contraseña
from tkinter import simpledialog, messagebox

# Configuración de la base de datos
engine = setup_database()
Session = sessionmaker(bind=engine)
session = Session()

# Variable global para el tiempo de inactividad
tiempo_inactividad = 60000  # 5 minutos en milisegundos (valor inicial)



def cargar_login():
    from src.vista.login import abrir_login
    return abrir_login


def abrir_aplicacion(usuario_actual):
    """Abre la ventana principal de la aplicación."""
    # Configuración de la ventana principal
    app = tk.Tk()
    app.title("Gestor de Contraseñas")
    app.geometry("800x600")
    app.configure(bg="#19222b")

    # Título de bienvenida
    tk.Label(app, text=f"Bienvenido, {usuario_actual.nombre}",
             font=("Constantia", 32), fg="#FFD700", bg="#19222b").pack(pady=20)

    # ======================
    # Funciones principales
    # ======================

    # Función para configurar el tiempo de inactividad
    def configurar_tiempo_inactividad():
        global tiempo_inactividad
        tiempo = simpledialog.askinteger("Tiempo de Inactividad", "Ingrese el tiempo de inactividad (en minutos):",
                                         minvalue=1, maxvalue=60)
        if tiempo:
            tiempo_inactividad = tiempo * 60000  # Convertir minutos a milisegundos
            messagebox.showinfo("Configuración Actualizada",
                                f"El tiempo de inactividad se ha configurado a {tiempo} minutos.")
            reiniciar_temporizador()  # Reiniciar el temporizador con el nuevo valor

    # Función para reiniciar el temporizador (acepta el argumento del evento)
    def reiniciar_temporizador(event=None):
        """Reinicia el temporizador con el nuevo valor de tiempo de inactividad."""
        if hasattr(app, 'after_id'):  # Si ya existe un temporizador anterior, cancelarlo
            app.after_cancel(app.after_id)
        app.after_id = app.after(tiempo_inactividad, cierre_automatico)  # Establecer el nuevo temporizador

    # Función para iniciar el temporizador cuando la aplicación se abre
    def iniciar_temporizador():
        """Inicia el temporizador cuando la aplicación se abre."""
        reiniciar_temporizador()
        # Agregar la detección de actividad
        detectar_actividad()

    # Función para cerrar la aplicación automáticamente por inactividad
    def cierre_automatico():
        messagebox.showinfo("Cierre Automático", "La aplicación se cerrará por inactividad.")
        app.destroy()
        abrir_login = cargar_login()
        abrir_login()

    # Función para detectar actividad (clic, movimiento del ratón, o tecla presionada)
    def detectar_actividad():
        """Detecta actividad del usuario y reinicia el temporizador cuando ocurre actividad."""
        app.bind("<Button>", reiniciar_temporizador)  # Detecta clics en la ventana
        app.bind("<Motion>", reiniciar_temporizador)  # Detecta movimiento del ratón
        app.bind("<Key>", reiniciar_temporizador)  # Detecta teclas presionadas

    def confirmar_cerrar_sesion():
        """Confirma el cierre de la aplicación y regresa al login."""
        if messagebox.askyesno("Confirmar Cierre",
                               "¿Estás seguro de que deseas cerrar la aplicación y regresar al login?"):
            app.destroy()  # Cierra la ventana de la aplicación actual
            abrir_login = cargar_login()  # Carga la función abrir_login
            abrir_login()  # Regresa al login

    def confirmar_salida():
        if messagebox.askyesno("Confirmar Cierre",
                               "¿Estás seguro de que deseas cerrar la aplicación?"):
            app.destroy()

    # Diccionario global para almacenar los favoritos
    favoritos = {}

    def actualizar_tabla():
        """Carga las contraseñas desde la base de datos y actualiza la tabla."""
        tabla.delete(*tabla.get_children())  # Limpia la tabla
        contraseñas = obtener_contraseñas_por_usuario(session, usuario_actual.id)

        # Depuración: Verifica que las contraseñas se obtienen correctamente
        print(f"Contraseñas obtenidas: {contraseñas}")

        if not contraseñas:
            tabla.insert("", "end", values=("No hay contraseñas", "", "", "", ""))
        else:
            for c in contraseñas:
                # Verifica si la contraseña está en el diccionario de favoritos
                favorita = "★" if favoritos.get(c["sitio"], False) else ""

                print(f"Contraseña: {c['sitio']}, Favorita: {favorita}")

                # Muestra la estrella si es favorita
                tabla.insert("", "end", values=(c["sitio"], c["usuario"], "*******", c["categoria"], favorita))

    def obtener_sitio_seleccionado():
        """Obtiene el sitio web seleccionado en la tabla."""
        seleccionado = tabla.focus()
        if seleccionado:
            return tabla.item(seleccionado)["values"][0]
        else:
            messagebox.showerror("Error", "Por favor, selecciona un elemento de la tabla.")
            return None

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
        sitio = obtener_sitio_seleccionado()
        if sitio:
            try:
                contraseña_descifrada = descifrar_contraseña_usuario(session, usuario_actual.id, sitio)
                messagebox.showinfo("Contraseña", f"Contraseña para {sitio}: {contraseña_descifrada}")
            except Exception as e:
                messagebox.showerror("Error", f"Error al descifrar la contraseña: {e}")

    def editar_contraseña_evento():
        """Permite editar la contraseña de un sitio seleccionado."""
        sitio = obtener_sitio_seleccionado()
        if not sitio:
            return

        nueva_contraseña = simpledialog.askstring(
            "Editar Contraseña",
            f"Ingrese la nueva contraseña para el sitio: {sitio}",
            show="*"
        )

        if not nueva_contraseña:
            messagebox.showerror("Error", "La contraseña no puede estar vacía.")
            return

        try:
            contrasena_obj = session.query(Contrasena).filter_by(usuario_id=usuario_actual.id, sitio_web=sitio).first()
            if not contrasena_obj:
                messagebox.showerror("Error", "No se encontró la contraseña en la base de datos.")
                return

            contrasena_obj.contrasena_encriptada = cifrar_contraseña(nueva_contraseña, usuario_actual.clave)
            session.commit()

            messagebox.showinfo("Éxito", f"La contraseña para {sitio} ha sido actualizada.")
            actualizar_tabla()
        except Exception as e:
            session.rollback()
            messagebox.showerror("Error", f"Error al actualizar la contraseña: {e}")

    def eliminar_contraseña_evento():
        """Permite eliminar una contraseña seleccionada."""
        sitio = obtener_sitio_seleccionado()
        if not sitio:
            return

        confirmacion = messagebox.askyesno(
            "Eliminar Contraseña",
            f"¿Estás seguro de que deseas eliminar la contraseña para el sitio: {sitio}?"
        )

        if not confirmacion:
            return

        try:
            contrasena_obj = session.query(Contrasena).filter_by(usuario_id=usuario_actual.id, sitio_web=sitio).first()
            if not contrasena_obj:
                messagebox.showerror("Error", "No se encontró la contraseña en la base de datos.")
                return

            session.delete(contrasena_obj)
            session.commit()

            messagebox.showinfo("Éxito", f"La contraseña para {sitio} ha sido eliminada.")
            actualizar_tabla()
        except Exception as e:
            session.rollback()
            messagebox.showerror("Error", f"Error al eliminar la contraseña: {e}")

    def marcar_como_favorita():
        """Marca o desmarca una contraseña como favorita."""
        sitio = obtener_sitio_seleccionado()  # Obtiene el sitio seleccionado en la tabla
        if not sitio:
            return

        try:
            # Verifica si el sitio está en el diccionario de favoritos
            if favoritos.get(sitio, False):
                # Desmarcar como favorito
                favoritos[sitio] = False
                estado = "desmarcado como favorito"
            else:
                # Marcar como favorito
                favoritos[sitio] = True
                estado = "marcado como favorito"

            messagebox.showinfo("Éxito", f"El sitio {sitio} ha sido {estado}.")

            # Después de actualizar, refresca la tabla
            actualizar_tabla()

        except Exception as e:
            messagebox.showerror("Error", f"Error al marcar como favorito: {e}")

    # ======================
    # Entradas y botones
    # ======================
    frame_entradas = tk.Frame(app, bg="#19222b")
    frame_entradas.pack(pady=5)

    tk.Label(frame_entradas, text="Usuario:",font=("Constantia", 15), fg="#ddd6cc", bg="#19222b").grid(row=0, column=0, padx=5)
    entry_usuario_sitio = tk.Entry(frame_entradas)
    entry_usuario_sitio.grid(row=0, column=1, padx=5)

    tk.Label(frame_entradas, text="Contraseña:",font=("Constantia",15), fg="#ddd6cc", bg="#19222b").grid(row=0, column=2, padx=5)
    entry_contraseña_sitio = tk.Entry(frame_entradas, show="*")
    entry_contraseña_sitio.grid(row=0, column=3, padx=5)

    tk.Label(frame_entradas, text="Sitio Web:",font=("Constantia", 15), fg="#ddd6cc", bg="#19222b").grid(row=1, column=0, padx=5)
    entry_sitio = tk.Entry(frame_entradas)
    entry_sitio.grid(row=1, column=1, padx=5)

    tk.Label(frame_entradas, text="Categoría:",  font=("Constantia", 15), bg="#19222b", fg="#ddd6cc").grid(row=1, column=2, padx=5, pady=5)
    categorias = ["Trabajo", "Personal", "Redes Sociales", "Bancos", "Otros"]
    categoria_combobox = ttk.Combobox(frame_entradas, values=categorias, state="readonly")
    categoria_combobox.grid(row=1, column=3, padx=5)
    categoria_combobox.set("Otros")

    # Botones principales
    frame_botones = tk.Frame(app, bg="#19222b")
    frame_botones.pack(pady=10)

    tk.Button(frame_botones, text="Guardar Contraseña", command=guardar_contraseña_evento,font=("Constantia", 11), fg="white", bg="#4CAF50", width= 18, height=1).grid(row=0, column=0, padx=10,pady=10)
    tk.Button(frame_botones, text="Ver Contraseña", command=ver_contraseña_evento, font=("Constantia", 11), fg="white", bg="#00BFFF", width= 18, height=1).grid(row=0, column=1, padx=10,pady=10)
    tk.Button(frame_botones, text="Editar Contraseña", command=editar_contraseña_evento, font=("Constantia", 11), fg="black", bg="#FFD700", width= 18, height=1).grid(row=0, column=2, padx=10, pady=10)
    tk.Button(frame_botones, text="Eliminar Contraseña", command=eliminar_contraseña_evento,font=("Constantia", 11), fg="white", bg="#FF4500", width= 18, height=1).grid(row=0, column=3, padx=10, pady=10)
    # Botones adicionales
    frame_adicionales = tk.LabelFrame(app, text="Opciones Adicionales", font=("Constantia", 14, "bold"), fg="white",bg="#19222b")
    frame_adicionales.pack(pady=10)

    # Botones dentro de Opciones Adicionales
    tk.Button(frame_adicionales, text="Marcar como Favorito", command=marcar_como_favorita,font=("Constantia", 11), bg="#4CAF50", fg="white",width=20).grid(row=0, column=0, padx=10, pady=5)
    tk.Button(frame_adicionales, text="Configurar Inactividad",command=configurar_tiempo_inactividad, font=("Constantia", 11), bg="#4CAF50",fg="white", width=20).grid(row=0, column=1, padx=10, pady=5)
    tk.Button(frame_adicionales, text="Cerrar Sesión", command=confirmar_cerrar_sesion, font=("Constantia", 11), bg="#FF4500", fg="white", width=20).grid(row=0, column=2,padx=10, pady=5)

    # Filtrar por categoría dentro de Opciones Adicionales
    tk.Label(frame_adicionales, text="Filtrar por Categoría:", font=("Constantia", 12), bg="#19222b", fg="white").grid(row=1, column=0, padx=5,pady=5)
    filtro_categoria_combobox = ttk.Combobox(frame_adicionales, values=["Todas"] + categorias, font=("Constantia", 12), state="readonly", width=18)
    filtro_categoria_combobox.grid(row=1, column=1, padx=5, pady=5)
    filtro_categoria_combobox.set("Todas")

    tk.Button(frame_adicionales, text="Aplicar Filtro", font=("Constantia", 12), bg="white", fg="black", width=20).grid(row=1, column=2, padx=10, pady=5)

    # ======================
    # Tabla de contraseñas
    # ======================
    # Estilo para la tabla
    style = ttk.Style()
    style.configure("Treeview", font=("Constantia", 12))  # Fuente y tamaño para las filas
    style.configure("Treeview.Heading", font=("Constantia", 12))  # Fuente y tamaño para los encabezados

    # Crear el marco de la tabla
    frame_tabla = tk.Frame(app, bg="#2E3B55")
    frame_tabla.pack(pady=10, fill=tk.BOTH, expand=True)

    # Definición de columnas y tabla
    columnas = ("sitio", "usuario", "contraseña", "categoria", "favorita")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=15)

    # Configuración de encabezados y columnas
    for col, text, width in zip(columnas,
                                ["Sitio Web", "Usuario", "Contraseña", "Categoría", "Favorita"],
                                [200, 150, 100, 150, 100]):
        tabla.heading(col, text=text)
        tabla.column(col, width=width, anchor="center")
    app.protocol("WM_DELETE_WINDOW", confirmar_salida)

    # Añadir tabla al marco
    tabla.pack(fill=tk.BOTH, expand=True)
    actualizar_tabla()
    iniciar_temporizador()
    app.mainloop()
