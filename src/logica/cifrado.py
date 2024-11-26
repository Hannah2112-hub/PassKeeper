from cryptography.fernet import Fernet


def generar_clave():
    """Genera una nueva clave de encriptación."""
    # Genera una clave válida de 32 bytes codificada en base64 URL-safe
    return Fernet.generate_key()


def cifrar_contraseña(contraseña, clave_usuario):
    """Cifra una contraseña utilizando la clave proporcionada."""
    if not contraseña or not clave_usuario:
        raise ValueError("La contraseña o la clave no pueden estar vacías.")

    # Crea un objeto Fernet con la clave proporcionada
    cifrador = Fernet(clave_usuario)

    # Cifra la contraseña y la devuelve como bytes
    return cifrador.encrypt(contraseña.encode())  # La contraseña debe estar en bytes


def descifrar_contraseña(contrasena_cifrada, clave_usuario):
    """Descifra una contraseña cifrada utilizando la clave proporcionada."""
    if not contrasena_cifrada or not clave_usuario:
        raise ValueError("La contraseña cifrada o la clave no pueden estar vacías.")

    # Crea un objeto Fernet con la clave proporcionada
    cifrador = Fernet(clave_usuario)

    # Descifra la contraseña y la devuelve como cadena (utf-8)
    return cifrador.decrypt(contrasena_cifrada).decode()  # Devuelve la contraseña descifrada en texto
