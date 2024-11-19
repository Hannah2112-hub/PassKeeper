# src/logica/gestion.py

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
        re.search(r'[!@#$%^&*(),.?":{}|<>]', contraseña)
    )


def obtener_contraseñas_ordenadas():
    """Devuelve las contraseñas ordenadas alfabéticamente por sitio web."""
    return dict(sorted(contraseñas.items()))
