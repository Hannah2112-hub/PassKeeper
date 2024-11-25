from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Base class for SQLAlchemy models
Base = declarative_base()


# Model for Usuario
class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    contrasena_maestra = Column(String(255), nullable=False)  # Contraseña cifrada
    clave = Column(String(255), nullable=False)  # Clave de cifrado

    # Relationships
    historial_contrasenas = relationship("HistorialContrasenas", back_populates="usuario", cascade="all, delete-orphan")
    notificaciones = relationship("Notificacion", back_populates="usuario", cascade="all, delete-orphan")
    configuracion = relationship("Configuracion", back_populates="usuario", uselist=False, cascade="all, delete-orphan")
    contrasenas = relationship("Contrasena", back_populates="usuario", cascade="all, delete-orphan")


# Model for HistorialContrasenas
class HistorialContrasenas(Base):
    __tablename__ = 'historial_contrasenas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_modificacion = Column(Date, nullable=False)
    cambios = Column(String, nullable=False)

    # Foreign key relationship
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    usuario = relationship("Usuario", back_populates="historial_contrasenas")


# Model for Contrasena
class Contrasena(Base):
    __tablename__ = 'contrasenas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sitio_web = Column(String, nullable=False)
    usuario_sitio = Column(String, nullable=False)
    contrasena_encriptada = Column(String, nullable=False)
    categoria = Column(String, nullable=True)
    historial_cambios = Column(String, nullable=True)

    # Foreign key relationship
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    usuario = relationship("Usuario", back_populates="contrasenas")

    # Security Relationship
    seguridad = relationship("Seguridad", back_populates="contrasena", uselist=False, cascade="all, delete-orphan")


# Model for Seguridad
class Seguridad(Base):
    __tablename__ = 'seguridad'

    id = Column(Integer, primary_key=True, autoincrement=True)
    clave_encriptacion = Column(String, nullable=False)

    # Foreign key relationship
    contrasena_id = Column(Integer, ForeignKey('contrasenas.id'), nullable=False)
    contrasena = relationship("Contrasena", back_populates="seguridad")


# Model for Notificacion
class Notificacion(Base):
    __tablename__ = 'notificaciones'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String, nullable=False)
    mensaje = Column(String, nullable=False)

    # Foreign key relationship
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    usuario = relationship("Usuario", back_populates="notificaciones")


# Model for Configuracion
class Configuracion(Base):
    __tablename__ = 'configuracion'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tiempo_bloqueo = Column(Integer, nullable=False)

    # Foreign key relationship
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    usuario = relationship("Usuario", back_populates="configuracion")


# Database setup
def setup_database():
    engine = create_engine("sqlite:///gestor_contrasenas.db")
    Base.metadata.create_all(engine)
    return engine

# Example session
if __name__ == "__main__":
    engine = setup_database()
    Session = sessionmaker(bind=engine)
    session = Session()