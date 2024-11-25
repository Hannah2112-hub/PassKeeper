import re

# Diccionarios globales para almacenar datos
usuarios = {}  # Almacena los datos de los usuarios
contraseñas = {}  # Almacena las contraseñas de sitios web asociadas a los usuarios


def validar_contraseña(contraseña):
    """Verifica que la contraseña cumpla con los requisitos de seguridad."""
    return (
        len(contraseña) >= 8 and
        re.search(r'[A-Z]', contraseña) and
        re.search(r'[a-z]', contraseña) and
        re.search(r'\d', contraseña) and
        re.search(r'[!@#$%^&*(),.?":{}|<>]', contraseña) and
        not re.search(r'\s', contraseña)  # Verifica que no haya espacios
    )


def obtener_contraseñas_ordenadas():
    """Devuelve las contraseñas ordenadas alfabéticamente por sitio web."""
    return dict(sorted(contraseñas.items()))


def agregar_contraseña_favorita(sitio, usuario, contraseña, favorita=False):
    """Agrega una contraseña y la marca como favorita si es necesario."""
    if sitio in contraseñas:
        # Si ya existe la contraseña para ese sitio, puedes actualizarla o mostrar un mensaje
        print(f"La contraseña para {sitio} ya existe. Actualizando...")
    contraseñas[sitio] = {
        "usuario": usuario,
        "contraseña": contraseña,
        "favorita": favorita  # Nuevo campo para marcar como favorita
    }

def agregar_contraseña_categoria(sitio, usuario, contraseña, categoria):
    """Agrega una contraseña y la categoriza."""
    contraseñas[sitio] = {
        "usuario": usuario,
        "contraseña": contraseña,
        "categoria": categoria  # Nuevo campo para la categoría
    }