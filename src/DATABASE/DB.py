from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
engine = create_engine('sqlite:///base_de_datos.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Modelos de Base de Datos
class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True, nullable=False)
    clave = Column(String, nullable=False)

    contrasenas = relationship("Contrasena", back_populates="usuario")

class Contrasena(Base):
    __tablename__ = 'contrasenas'
    id = Column(Integer, primary_key=True)
    sitio = Column(String, nullable=False)
    usuario_sitio = Column(String, nullable=False)
    clave = Column(String, nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))

    usuario = relationship("Usuario", back_populates="contrasenas")

def crear_tablas():
    Base.metadata.create_all(engine)