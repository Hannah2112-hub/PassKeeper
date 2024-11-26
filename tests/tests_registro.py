import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.DATABASE.DB import Base, Usuario
from src.logica.cifrado import generar_clave
from src.logica.gestion import validar_contraseña
from src.vista.registro import validar_correo


class TestRegistro(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configura una base de datos en memoria para las pruebas."""
        cls.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()

    @classmethod
    def tearDownClass(cls):
        """Cierra la base de datos en memoria después de las pruebas."""
        cls.session.close()
        cls.engine.dispose()

    def test_validar_correo(self):
        """Prueba para verificar la validación de correos electrónicos."""
        self.assertTrue(validar_correo("user@example.com"))
        self.assertTrue(validar_correo("user.name+alias@domain.co"))
        self.assertFalse(validar_correo("user@.com"))
        self.assertFalse(validar_correo("user@domain"))
        self.assertFalse(validar_correo("user@domain..com"))
        self.assertFalse(validar_correo("plainaddress"))

    def test_validar_contraseña(self):
        """Prueba para verificar la validación de contraseñas."""
        self.assertTrue(validar_contraseña("Password1!"))  # Contraseña válida
        self.assertFalse(validar_contraseña("short"))  # Demasiado corta
        self.assertFalse(validar_contraseña("nouppercase1!"))  # Sin mayúsculas
        self.assertFalse(validar_contraseña("NOLOWERCASE1!"))  # Sin minúsculas
        self.assertFalse(validar_contraseña("NoNumbers!"))  # Sin números
        self.assertFalse(validar_contraseña("NoSpecialChar1"))  # Sin caracteres especiales
        self.assertFalse(validar_contraseña("Spaces not allowed1!"))  # Contiene espacios

    def test_registrar_usuario_exitoso(self):
        """Prueba para verificar que un usuario se registre correctamente."""
        clave_usuario = generar_clave()
        nuevo_usuario = Usuario(
            nombre="testuser",
            email="testuser@example.com",
            contrasena_maestra="password123",
            clave=clave_usuario
        )
        self.session.add(nuevo_usuario)
        self.session.commit()

        # Verificar que el usuario se haya registrado
        usuario_registrado = self.session.query(Usuario).filter_by(nombre="testuser").first()
        self.assertIsNotNone(usuario_registrado)
        self.assertEqual(usuario_registrado.email, "testuser@example.com")

    def test_usuario_duplicado(self):
        """Prueba para verificar que no se permita el registro de usuarios duplicados."""
        clave_usuario = generar_clave()
        usuario1 = Usuario(
            nombre="testuser",
            email="testuser@example.com",
            contrasena_maestra="password123",
            clave=clave_usuario
        )
        self.session.add(usuario1)
        self.session.commit()

        # Intentar agregar un usuario con el mismo nombre o correo
        usuario_duplicado = Usuario(
            nombre="testuser",
            email="testuser@example.com",
            contrasena_maestra="password456",
            clave=clave_usuario
        )
        with self.assertRaises(Exception):
            self.session.add(usuario_duplicado)
            self.session.commit()

        # Rollback después del error
        self.session.rollback()

    def test_registro_usuario_campos_vacios(self):
        """Prueba para verificar que no se permita el registro con campos vacíos."""
        with self.assertRaises(Exception):
            usuario_invalido = Usuario(
                nombre=None,  # Nombre vacío
                email=None,  # Correo vacío
                contrasena_maestra=None,  # Contraseña vacía
                clave=None  # Clave vacía
            )
            self.session.add(usuario_invalido)
            self.session.commit()

        # Rollback después del error
        self.session.rollback()


if __name__ == "__main__":
    unittest.main()
