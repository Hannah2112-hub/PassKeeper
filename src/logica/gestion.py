import re
from sqlalchemy.orm import Session
from src.DATABASE.DB import Usuario, Contrasena
from src.logica.cifrado import cifrar_contraseña, descifrar_contraseña

def validar_contraseña(contraseña):
    """
    Verifica que la contraseña cumpla con los requisitos de seguridad:
    - Al menos 8 caracteres.
    - Contiene al menos una letra mayúscula.
    - Contiene al menos una letra minúscula.
    - Contiene al menos un número.
    - Contiene al menos un carácter especial.
    - No contiene espacios.
    """
    if len(contraseña) < 8:
        return False
    if not re.search(r'[A-Z]', contraseña):
        return False
    if not re.search(r'[a-z]', contraseña):
        return False
    if not re.search(r'\d', contraseña):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', contraseña):
        return False
    if re.search(r'\s', contraseña):
        return False
    return True

def guardar_contraseña(session: Session, usuario_id, sitio, usuario_sitio, contraseña_sitio, categoria):
    """Guarda una nueva contraseña asociada a un usuario en la base de datos."""
    try:
        # Buscar al usuario en la base de datos
        usuario = session.query(Usuario).filter_by(id=usuario_id).first()
        if not usuario:
            raise ValueError(f"Usuario con ID {usuario_id} no encontrado.")

        # Cifrar la contraseña usando la clave del usuario
        contraseña_cifrada = cifrar_contraseña(contraseña_sitio, usuario.clave)

        # Crear una nueva instancia de contraseña
        nueva_contraseña = Contrasena(
            sitio_web=sitio,
            usuario_sitio=usuario_sitio,
            contrasena_encriptada=contraseña_cifrada,
            categoria=categoria,
            usuario_id=usuario.id
        )

        # Agregar y confirmar cambios
        session.add(nueva_contraseña)
        session.commit()
        return f"Contraseña para {sitio} guardada exitosamente."
    except Exception as e:
        session.rollback()
        raise ValueError(f"Error al guardar la contraseña: {e}")

def obtener_contraseñas_por_usuario(session: Session, usuario_id):
    """Obtiene todas las contraseñas asociadas a un usuario específico."""
    try:
        contraseñas = session.query(Contrasena).filter_by(usuario_id=usuario_id).all()
        return [
            {
                "sitio": c.sitio_web,
                "usuario": c.usuario_sitio,
                "contraseña": c.contrasena_encriptada,
                "categoria": c.categoria
            }
            for c in contraseñas
        ]
    except Exception as e:
        raise ValueError(f"Error al obtener contraseñas: {e}")

def descifrar_contraseña_usuario(session: Session, usuario_id, sitio):
    """Descifra la contraseña de un sitio específico para un usuario."""
    try:
        contraseña = session.query(Contrasena).filter_by(usuario_id=usuario_id, sitio_web=sitio).first()
        if not contraseña:
            raise ValueError(f"No se encontró una contraseña para el sitio {sitio}.")

        # Buscar la clave del usuario
        usuario = session.query(Usuario).filter_by(id=usuario_id).first()
        if not usuario:
            raise ValueError(f"Usuario con ID {usuario_id} no encontrado.")

        # Descifrar la contraseña
        return descifrar_contraseña(contraseña.contrasena_encriptada, usuario.clave)
    except Exception as e:
        raise ValueError(f"Error al descifrar la contraseña: {e}")
