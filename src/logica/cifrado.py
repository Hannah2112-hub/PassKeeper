from cryptography.fernet import Fernet


def generar_clave():
    """Genera una nueva clave de encriptación."""
    return Fernet.generate_key()


def cifrar_contraseña(contraseña, clave_usuario):
    """Cifra una contraseña utilizando la clave proporcionada."""
    cifrador = Fernet(clave_usuario)
    return cifrador.encrypt(contraseña.encode())


def descifrar_contraseña(contraseña_cifrada, clave_usuario):
    """Descifra una contraseña cifrada utilizando la clave proporcionada."""
    try:
        cifrador = Fernet(clave_usuario)
        return cifrador.decrypt(contraseña_cifrada).decode()
    except Exception:
        return None
