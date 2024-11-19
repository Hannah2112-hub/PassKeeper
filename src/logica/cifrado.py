from cryptography.fernet import Fernet


def generar_clave():
    """Genera una nueva clave de encriptación."""
    return Fernet.generate_key()


def cifrar_contraseña(contraseña, clave_usuario):
    """Cifra una contraseña utilizando la clave proporcionada."""
    if not contraseña or not clave_usuario:
        raise ValueError("La contraseña o la clave no pueden estar vacías.")
    cifrador = Fernet(clave_usuario)
    return cifrador.encrypt(contraseña.encode())


def descifrar_contraseña(contraseña_cifrada, clave_usuario):
    """Descifra una contraseña cifrada utilizando la clave proporcionada."""
    try:
        if not contraseña_cifrada or not clave_usuario:
            raise ValueError("La contraseña cifrada o la clave no pueden estar vacías.")
        cifrador = Fernet(clave_usuario)
        return cifrador.decrypt(contraseña_cifrada).decode()
    except Exception as e:
        print(f"Error al descifrar: {e}")
        return "Error al descifrar la contraseña."