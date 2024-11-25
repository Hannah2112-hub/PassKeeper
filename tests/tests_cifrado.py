import unittest
from cryptography.fernet import Fernet

# Funciones proporcionadas
def generar_clave():
    """Genera una nueva clave de encriptación."""
    return Fernet.generate_key()

def cifrar_contraseña(contraseña, clave_usuario):
    """Cifra una contraseña utilizando la clave proporcionada."""
    if not contraseña or not clave_usuario:
        raise ValueError("La contraseña o la clave no pueden estar vacías.")
    cifrador = Fernet(clave_usuario)
    return cifrador.encrypt(contraseña.encode())

def descifrar_contraseña(contrasena_cifrada, clave_usuario):
    """Descifra una contraseña cifrada utilizando la clave proporcionada."""
    if not contrasena_cifrada or not clave_usuario:
        raise ValueError("La contraseña cifrada o la clave no pueden estar vacías.")
    cifrador = Fernet(clave_usuario)
    return cifrador.decrypt(contrasena_cifrada).decode()

# Clase de pruebas usando unittest
class TestEncriptacion(unittest.TestCase):

    def test_generar_clave(self):
        """Test para verificar que se genera una clave de 32 bytes."""
        clave = generar_clave()
        self.assertEqual(len(clave), 44)  # La clave codificada en base64 tiene 44 caracteres

    def test_cifrar_contraseña(self):
        """Test para verificar que la contraseña se cifra correctamente."""
        clave = generar_clave()
        contraseña = "mi_contraseña_segura"
        contrasena_cifrada = cifrar_contraseña(contraseña, clave)
        self.assertIsInstance(contrasena_cifrada, bytes)  # La salida debe ser un objeto de tipo bytes

    def test_descifrar_contraseña(self):
        """Test para verificar que la contraseña se descifra correctamente."""
        clave = generar_clave()
        contraseña = "mi_contraseña_segura"
        contrasena_cifrada = cifrar_contraseña(contraseña, clave)
        contrasena_descifrada = descifrar_contraseña(contrasena_cifrada, clave)
        self.assertEqual(contraseña, contrasena_descifrada)  # Deben coincidir la original y la descifrada

    def test_error_sin_clave_o_contraseña(self):
        """Test para verificar que se lanza un error si se intenta cifrar o descifrar sin clave o contraseña."""
        with self.assertRaises(ValueError):
            cifrar_contraseña("", None)  # Debe lanzar un ValueError
        with self.assertRaises(ValueError):
            descifrar_contraseña(None, "")  # Debe lanzar un ValueError

# Ejecutar las pruebas
if __name__ == "__main__":
    unittest.main()
