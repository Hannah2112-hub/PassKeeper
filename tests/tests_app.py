import unittest
import string
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.DATABASE.DB import Base, Usuario, Contrasena
from src.logica.cifrado import cifrar_contraseña, descifrar_contraseña
from cryptography.fernet import Fernet  # Para generar claves válidas

class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configura una base de datos en memoria para las pruebas."""
        cls.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()

        # Generar una clave válida para Fernet
        cls.clave_valida = Fernet.generate_key()

        # Crear un usuario de prueba
        cls.usuario = Usuario(
            nombre="testuser",
            email="testuser@example.com",
            contrasena_maestra=cifrar_contraseña("password123", cls.clave_valida),
            clave=cls.clave_valida
        )
        cls.session.add(cls.usuario)
        cls.session.commit()

    @classmethod
    def tearDownClass(cls):
        """Elimina la base de datos en memoria después de las pruebas."""
        cls.session.close()
        cls.engine.dispose()

    def test_guardar_contraseña(self):
        """Prueba guardar una contraseña en la base de datos."""
        nueva_contraseña = Contrasena(
            sitio_web="example.com",
            usuario_sitio="user@example.com",
            contrasena_encriptada=cifrar_contraseña("mypassword", self.usuario.clave),
            categoria="Trabajo",
            usuario_id=self.usuario.id
        )
        self.session.add(nueva_contraseña)
        self.session.commit()

        # Verificar que la contraseña se haya guardado correctamente
        contrasena_guardada = self.session.query(Contrasena).filter_by(sitio_web="example.com").first()
        self.assertIsNotNone(contrasena_guardada)
        self.assertEqual(contrasena_guardada.usuario_sitio, "user@example.com")

    def test_ver_contraseña(self):
        """Prueba descifrar una contraseña almacenada."""
        contrasena_obj = Contrasena(
            sitio_web="example2.com",
            usuario_sitio="user2@example.com",
            contrasena_encriptada=cifrar_contraseña("mypassword2", self.usuario.clave),
            categoria="Personal",
            usuario_id=self.usuario.id
        )
        self.session.add(contrasena_obj)
        self.session.commit()

        # Descifrar contraseña
        contrasena_descifrada = descifrar_contraseña(contrasena_obj.contrasena_encriptada, self.usuario.clave)
        self.assertEqual(contrasena_descifrada, "mypassword2")

    def test_editar_contraseña(self):
        """Prueba actualizar una contraseña existente."""
        # Crear una contraseña de prueba
        contrasena_obj = Contrasena(
            sitio_web="example3.com",
            usuario_sitio="user3@example.com",
            contrasena_encriptada=cifrar_contraseña("oldpassword", self.usuario.clave),
            categoria="Redes Sociales",
            usuario_id=self.usuario.id
        )
        self.session.add(contrasena_obj)
        self.session.commit()

        # Editar la contraseña
        contrasena_obj.contrasena_encriptada = cifrar_contraseña("newpassword", self.usuario.clave)
        self.session.commit()

        # Verificar el cambio
        contrasena_descifrada = descifrar_contraseña(contrasena_obj.contrasena_encriptada, self.usuario.clave)
        self.assertEqual(contrasena_descifrada, "newpassword")

    def test_eliminar_contraseña(self):
        """Prueba eliminar una contraseña existente."""
        # Crear una contraseña de prueba
        contrasena_obj = Contrasena(
            sitio_web="example4.com",
            usuario_sitio="user4@example.com",
            contrasena_encriptada=cifrar_contraseña("todeletepassword", self.usuario.clave),
            categoria="Otros",
            usuario_id=self.usuario.id
        )
        self.session.add(contrasena_obj)
        self.session.commit()

        # Eliminar la contraseña
        self.session.delete(contrasena_obj)
        self.session.commit()

        # Verificar que se haya eliminado
        contrasena_eliminada = self.session.query(Contrasena).filter_by(sitio_web="example4.com").first()
        self.assertIsNone(contrasena_eliminada)

def generar_contraseña():
    longitud = 12
    caracteres = (
            string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation
    )
    contraseña_segura = ''.join(random.choice(caracteres) for _ in range(longitud))
    return contraseña_segura

# Clase para pruebas unitarias
class TestGeneradorContraseña(unittest.TestCase):
    def test_longitud_contraseña(self):
        """Verifica que la contraseña generada tenga la longitud esperada."""
        contraseña = generar_contraseña()
        self.assertEqual(len(contraseña), 12, "La contraseña no tiene la longitud correcta.")

    def test_caracteres_validos(self):
        """Verifica que la contraseña generada contenga solo caracteres válidos."""
        caracteres_validos = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation
        contraseña = generar_contraseña()
        for char in contraseña:
            self.assertIn(char, caracteres_validos, f"El carácter '{char}' no es válido en la contraseña.")

    def test_variedad_en_contraseñas(self):
        """Verifica que las contraseñas generadas no sean iguales (aleatoriedad)."""
        contraseñas = {generar_contraseña() for _ in range(10)}
        self.assertGreater(len(contraseñas), 1, "La función genera contraseñas idénticas.")

if __name__ == "__main__":
    unittest.main()
