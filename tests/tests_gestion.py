import unittest
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


# Pruebas
class TestContraseñas(unittest.TestCase):

    def test_validar_contraseña_valida(self):
        """Test para validar una contraseña correcta."""
        self.assertTrue(validar_contraseña("MiContraseña123!"))

    def test_validar_contraseña_invalida_sin_mayusculas(self):
        """Test para validar una contraseña sin mayúsculas."""
        self.assertFalse(validar_contraseña("micontaseña123!"))

    def test_validar_contraseña_invalida_sin_minusculas(self):
        """Test para validar una contraseña sin minúsculas."""
        self.assertFalse(validar_contraseña("MICONTRASEÑA123!"))

    def test_validar_contraseña_invalida_sin_numero(self):
        """Test para validar una contraseña sin números."""
        self.assertFalse(validar_contraseña("MiContraseña!"))

    def test_validar_contraseña_invalida_sin_caracteres_especiales(self):
        """Test para validar una contraseña sin caracteres especiales."""
        self.assertFalse(validar_contraseña("MiContraseña123"))

    def test_validar_contraseña_invalida_con_espacios(self):
        """Test para validar una contraseña con espacios."""
        self.assertFalse(validar_contraseña("Mi Contraseña 123!"))

    def test_obtener_contraseñas_ordenadas(self):
        """Test para verificar que las contraseñas se ordenen alfabéticamente."""
        contraseñas.clear()  # Limpiar para pruebas
        agregar_contraseña_favorita("google.com", "usuario1", "MiContraseña123!", favorita=True)
        agregar_contraseña_favorita("facebook.com", "usuario2", "OtraContraseña123!", favorita=False)
        contraseñas_ordenadas = obtener_contraseñas_ordenadas()
        self.assertEqual(list(contraseñas_ordenadas.keys()), ['facebook.com', 'google.com'])

    def test_agregar_contraseña_favorita(self):
        """Test para verificar que se agregue una contraseña y se marque como favorita."""
        contraseñas.clear()  # Limpiar para pruebas
        agregar_contraseña_favorita("google.com", "usuario1", "MiContraseña123!", favorita=True)
        self.assertTrue("google.com" in contraseñas)
        self.assertEqual(contraseñas["google.com"]["favorita"], True)

    def test_agregar_contraseña_categoria(self):
        """Test para verificar que se agregue una contraseña con una categoría."""
        contraseñas.clear()  # Limpiar para pruebas
        agregar_contraseña_categoria("google.com", "usuario1", "MiContraseña123!", "Trabajo")
        self.assertTrue("google.com" in contraseñas)
        self.assertEqual(contraseñas["google.com"]["categoria"], "Trabajo")

    def test_agregar_contraseña_existente(self):
        """Test para verificar que al agregar una contraseña ya existente se actualice."""
        contraseñas.clear()  # Limpiar para pruebas
        agregar_contraseña_favorita("google.com", "usuario1", "MiContraseña123!", favorita=True)
        agregar_contraseña_favorita("google.com", "usuario1", "NuevaContraseña456!", favorita=False)
        self.assertEqual(contraseñas["google.com"]["contraseña"], "NuevaContraseña456!")
        self.assertEqual(contraseñas["google.com"]["favorita"], False)


# Ejecutar las pruebas
if __name__ == "__main__":
    unittest.main()
