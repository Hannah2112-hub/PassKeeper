import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.DATABASE.DB import Base, Usuario, Contrasena
from src.logica.gestion import (
    validar_contraseña,
    guardar_contraseña,
    obtener_contraseñas_por_usuario,
    descifrar_contraseña_usuario
)
from src.logica.cifrado import generar_clave, cifrar_contraseña


class TestGestion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configura una base de datos en memoria para las pruebas."""
        cls.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()

        # Crear un usuario de prueba con una clave válida
        cls.clave_usuario = generar_clave()
        cls.usuario = Usuario(
            nombre="testuser",
            email="testuser@example.com",
            contrasena_maestra=cifrar_contraseña("password123", cls.clave_usuario),
            clave=cls.clave_usuario
        )
        cls.session.add(cls.usuario)
        cls.session.commit()

    @classmethod
    def tearDownClass(cls):
        """Elimina la base de datos en memoria después de las pruebas."""
        cls.session.close()
        cls.engine.dispose()

    def test_validar_contraseña(self):
        """Prueba para verificar que la validación de contraseñas funciona correctamente."""
        self.assertTrue(validar_contraseña("Password1!"))  # Contraseña válida
        self.assertFalse(validar_contraseña("short"))  # Demasiado corta
        self.assertFalse(validar_contraseña("nouppercase1!"))  # Sin mayúsculas
        self.assertFalse(validar_contraseña("NOLOWERCASE1!"))  # Sin minúsculas
        self.assertFalse(validar_contraseña("NoNumbers!"))  # Sin números
        self.assertFalse(validar_contraseña("NoSpecialChar1"))  # Sin caracteres especiales
        self.assertFalse(validar_contraseña("Spaces not allowed1!"))  # Contiene espacios

    def test_guardar_contraseña(self):
        """Prueba para verificar que una contraseña se guarda correctamente en la base de datos."""
        mensaje = guardar_contraseña(
            self.session,
            self.usuario.id,
            "example.com",
            "user@example.com",
            "mypassword",
            "Trabajo"
        )
        self.assertEqual(mensaje, "Contraseña para example.com guardada exitosamente.")

        # Verificar que la contraseña se haya guardado
        contrasena = self.session.query(Contrasena).filter_by(sitio_web="example.com").first()
        self.assertIsNotNone(contrasena)
        self.assertEqual(contrasena.usuario_sitio, "user@example.com")

    def test_descifrar_contraseña_usuario(self):
        """Prueba para verificar que una contraseña se descifra correctamente."""
        # Agregar una contraseña de prueba
        guardar_contraseña(
            self.session,
            self.usuario.id,
            "example3.com",
            "user3@example.com",
            "mypassword3",
            "Otros"
        )

        contrasena_descifrada = descifrar_contraseña_usuario(self.session, self.usuario.id, "example3.com")
        self.assertEqual(contrasena_descifrada, "mypassword3")

    def test_error_descifrar_contraseña_usuario(self):
        """Prueba para verificar que se lanza un error si no se encuentra la contraseña o el usuario."""
        with self.assertRaises(ValueError):
            descifrar_contraseña_usuario(self.session, self.usuario.id, "nonexistent.com")  # Sitio no existe
        with self.assertRaises(ValueError):
            descifrar_contraseña_usuario(self.session, 9999, "example3.com")  # Usuario no existe


if __name__ == "__main__":
    unittest.main()
