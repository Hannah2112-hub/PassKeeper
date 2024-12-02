import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from src.DATABASE.DB import Base, Usuario
from src.logica.cifrado import generar_clave, cifrar_contraseña
from src.logica.gestion import validar_contraseña
import re


# Función para validar el correo
def validar_correo(correo):
    patron = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(patron, correo))


class TestRegistroUsuario(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configura una base de datos en memoria para las pruebas."""
        cls.engine = create_engine("sqlite:///:memory:")  # Base de datos en memoria
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()

    @classmethod
    def tearDownClass(cls):
        """Cierra la base de datos en memoria después de las pruebas."""
        cls.session.close()
        cls.engine.dispose()

    def setUp(self):
        """Limpia la base de datos antes de cada prueba."""
        self.session.query(Usuario).delete()
        self.session.commit()

    def registrar_usuario(self, nombre, correo, contraseña):
        """Simula el registro de un usuario."""
        if not nombre or not correo or not contraseña:
            raise ValueError("Todos los campos son obligatorios.")

        if not validar_correo(correo):
            raise ValueError("El correo electrónico no es válido.")

        usuario_existente = self.session.query(Usuario).filter(
            (Usuario.nombre == nombre) | (Usuario.email == correo)
        ).first()
        if usuario_existente:
            raise ValueError("El usuario o correo ya está registrado.")

        if not validar_contraseña(contraseña):
            raise ValueError(
                "La contraseña debe tener al menos 8 caracteres, incluir mayúsculas, minúsculas, números y caracteres especiales."
            )

        clave_usuario = generar_clave()
        contraseña_cifrada = cifrar_contraseña(contraseña, clave_usuario)

        nuevo_usuario = Usuario(
            nombre=nombre,
            email=correo,
            contrasena_maestra=contraseña_cifrada,
            clave=clave_usuario
        )

        self.session.add(nuevo_usuario)
        self.session.commit()

    def test_registro_exitoso(self):
        """Prueba el registro exitoso de un usuario."""
        try:
            self.registrar_usuario("testuser", "testuser@example.com", "Password1!")
            usuario = self.session.query(Usuario).filter_by(nombre="testuser").first()
            self.assertIsNotNone(usuario)
            self.assertEqual(usuario.email, "testuser@example.com")
        except Exception as e:
            self.fail(f"Registro falló con excepción: {e}")

    def test_campos_vacios(self):
        """Prueba el registro con campos vacíos."""
        with self.assertRaises(ValueError):
            self.registrar_usuario("", "testuser@example.com", "Password1!")
        with self.assertRaises(ValueError):
            self.registrar_usuario("testuser", "", "Password1!")
        with self.assertRaises(ValueError):
            self.registrar_usuario("testuser", "testuser@example.com", "")

    def test_correo_invalido(self):
        """Prueba el registro con correos inválidos."""
        with self.assertRaises(ValueError):
            self.registrar_usuario("testuser", "correo_invalido", "Password1!")

    def test_usuario_existente(self):
        """Prueba el registro con un usuario o correo duplicado."""
        self.registrar_usuario("testuser", "testuser@example.com", "Password1!")
        with self.assertRaises(ValueError):
            self.registrar_usuario("testuser", "otro_correo@example.com", "Password1!")
        with self.assertRaises(ValueError):
            self.registrar_usuario("otro_usuario", "testuser@example.com", "Password1!")

    def test_contraseña_insegura(self):
        """Prueba el registro con contraseñas inseguras."""
        with self.assertRaises(ValueError):
            self.registrar_usuario("testuser", "testuser@example.com", "short")
        with self.assertRaises(ValueError):
            self.registrar_usuario("testuser", "testuser@example.com", "nouppercase1!")
        with self.assertRaises(ValueError):
            self.registrar_usuario("testuser", "testuser@example.com", "NOLOWERCASE1!")
        with self.assertRaises(ValueError):
            self.registrar_usuario("testuser", "testuser@example.com", "NoNumbers!")
        with self.assertRaises(ValueError):
            self.registrar_usuario("testuser", "testuser@example.com", "NoSpecialChar1")
        with self.assertRaises(ValueError):
            self.registrar_usuario("testuser", "testuser@example.com", "Spaces not allowed1!")


if __name__ == "__main__":
    unittest.main()
