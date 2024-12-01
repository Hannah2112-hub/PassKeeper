from xmlrpc.client import boolean

from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Base class for SQLAlchemy models
Base = declarative_base()

# Modelo para Usuario
class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    contrasena_maestra = Column(String(255), nullable=False)  # Contraseña cifrada
    clave = Column(String(255), nullable=False)  # Clave de cifrado

    # Relaciones
    contrasenas = relationship("Contrasena", back_populates="usuario", cascade="all, delete-orphan")

# Modelo para Contrasena
class Contrasena(Base):
    __tablename__ = 'contrasenas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sitio_web = Column(String, nullable=False)
    usuario_sitio = Column(String, nullable=False)
    contrasena_encriptada = Column(String, nullable=False)
    categoria = Column(String, nullable=True)
    favorita = Column(Integer, default=0)

    # Relación con Usuario
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    usuario = relationship("Usuario", back_populates="contrasenas")

# Configuración de la base de datos
def setup_database():
    engine = create_engine("sqlite:///gestor_contrasenas.db")
    Base.metadata.create_all(engine)
    return engine

# Ejemplo de sesión
if __name__ == "__main__":
    engine = setup_database()
    Session = sessionmaker(bind=engine)
    session = Session()
