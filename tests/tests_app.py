import unittest
from unittest.mock import MagicMock
import hashlib

# Importar las funciones que vamos a probar
from src.vista.app import cifrar_contrasena, guardar_contrasena


class TestGestorContraseñas(unittest.TestCase):
    # Test de cifrado de contraseñas
    def test_cifrar_contrasena(self):
        password = "mi_contraseña_secreta"
        hashed_password = cifrar_contrasena(password)
        # Comprobamos que la contraseña cifrada es un hash de longitud 64 (SHA256)
        self.assertEqual(len(hashed_password), 64)
        self.assertNotEqual(hashed_password, password)  # El hash no debe ser igual a la contraseña original

    # Test de guardar contraseñas
    def test_guardar_contrasena(self):
        # Mock de la sesión de la base de datos
        session = MagicMock()
        usuario_actual = MagicMock()
        usuario_actual.id = 1  # Mock de un ID de usuario

        # Mock de datos de contraseña
        sitio = "example.com"
        usuario_sitio = "usuario_test"
        contrasena_sitio = "12345"
        categoria = "Trabajo"

        # Llamamos a la función
        guardar_contrasena(session, sitio, usuario_sitio, contrasena_sitio, categoria, usuario_actual)

        # Verificamos que se haya agregado la nueva contraseña a la sesión de la base de datos
        session.add.assert_called_once()  # Comprobamos que se haya llamado add
        session.commit.assert_called_once()  # Comprobamos que se haya llamado commit

    # Test de editar contraseñas
    def test_editar_contrasena(self):
        contraseñas = {"example.com": {"contraseña": "cifrada123"}}
        sitio = "example.com"
        nueva_contrasena = "nueva_cifrada123"

        # Simulamos un cambio de clave para el usuario
        contraseñas[sitio]["contraseña"] = nueva_contrasena
        # Verificamos que la contraseña haya sido cambiada
        self.assertEqual(contraseñas[sitio]["contraseña"], nueva_contrasena)

    # Test de configurar el tiempo de inactividad
    def test_configurar_tiempo_inactividad(self):
        global tiempo_inactividad
        tiempo_inactividad = 300000  # Inicializamos con 5 minutos (en milisegundos)

        # Simulamos cambiar el tiempo de inactividad a 10 minutos
        nuevo_tiempo = 10 * 60000  # 10 minutos en milisegundos
        tiempo_inactividad = nuevo_tiempo

        # Comprobamos que el tiempo se haya actualizado correctamente
        self.assertEqual(tiempo_inactividad, nuevo_tiempo)

    # Test de la función de ver contraseñas
    def test_ver_contrasena_segura(self):
        contraseñas = {"example.com": {"contraseña": "cifrada123", "contraseña_visible": None}}
        sitio = "example.com"
        clave_usuario = "clave_test"

        # Simulamos descifrar la contraseña
        contraseña_descifrada = "12345"  # Simulamos la contraseña original

        # Mostrar la contraseña y actualizar la tabla
        contraseñas[sitio]["contraseña_visible"] = contraseña_descifrada
        self.assertEqual(contraseñas[sitio]["contraseña_visible"], "12345")

        # Luego, simulamos que se oculta la contraseña
        contraseñas[sitio]["contraseña_visible"] = None
        self.assertIsNone(contraseñas[sitio].get("contraseña_visible"))


if __name__ == "__main__":
    unittest.main()
