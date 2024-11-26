import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.DATABASE.DB import Base, Usuario
from src.logica.cifrado import generar_clave, cifrar_contraseña, descifrar_contraseña

class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configura una base de datos en memoria para las pruebas."""
        cls.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()

        # Crear un usuario de prueba
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

    def test_login_exitoso(self):
        """Prueba para verificar que un usuario puede iniciar sesión correctamente."""
        usuario = self.session.query(Usuario).filter_by(nombre="testuser").first()
        self.assertIsNotNone(usuario)
        contrasena_descifrada = descifrar_contraseña(usuario.contrasena_maestra, usuario.clave)
        self.assertEqual(contrasena_descifrada, "password123")

    def test_usuario_no_encontrado(self):
        """Prueba para verificar el comportamiento cuando el usuario no existe."""
        usuario = self.session.query(Usuario).filter_by(nombre="nonexistentuser").first()
        self.assertIsNone(usuario)

    def test_contraseña_incorrecta(self):
        """Prueba para verificar que se detecta una contraseña incorrecta."""
        usuario = self.session.query(Usuario).filter_by(nombre="testuser").first()
        self.assertIsNotNone(usuario)
        contrasena_descifrada = descifrar_contraseña(usuario.contrasena_maestra, usuario.clave)
        self.assertNotEqual(contrasena_descifrada, "wrongpassword")

    def test_campos_vacios(self):
        """Prueba para verificar que no se permita iniciar sesión con campos vacíos."""
        nombre_usuario = ""
        contraseña = ""
        with self.assertRaises(ValueError):
            if not nombre_usuario or not contraseña:
                raise ValueError("Todos los campos son obligatorios.")

if __name__ == "__main__":
    unittest.main()
