import unittest
from unittest.mock import patch, MagicMock
from tkinter import messagebox
from src.vista.registro import abrir_registro
from src.DATABASE.DB import Usuario
from sqlalchemy.orm import sessionmaker

from src.vista.registro import validar_correo

class TestValidarCorreo(unittest.TestCase):

    def test_validar_correo_valido(self):
        """Test para verificar que un correo válido sea aceptado."""
        correo = "usuario@dominio.com"
        self.assertTrue(validar_correo(correo))

    def test_validar_correo_invalido(self):
        """Test para verificar que un correo inválido sea rechazado."""
        correo = "usuario@dominio"
        self.assertFalse(validar_correo(correo))

    def test_validar_correo_vacio(self):
        """Test para verificar que un correo vacío sea rechazado."""
        correo = ""
        self.assertFalse(validar_correo(correo))

if __name__ == '__main__':
    unittest.main()
