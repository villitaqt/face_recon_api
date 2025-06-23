# database.py
# Este módulo configura la conexión a la base de datos PostgreSQL
# y define el modelo de datos para los usuarios y sus embeddings.

from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import UUIDType # Para usar UUID como ID, si no, puedes usar String o Integer
import uuid # Para generar UUIDs
import os # Para acceder a variables de entorno
import pickle
from datetime import datetime

# Importar el tipo VECTOR de pgvector para SQLAlchemy
from pgvector.sqlalchemy import Vector # ¡Importante para los embeddings!

# --- Configuración de la Base de Datos ---
# Se recomienda usar variables de entorno para las credenciales de la base de datos
# DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@host:port/dbname")
# Para pruebas locales, puedes definirla directamente así:
# ¡IMPORTANTE! Cambia estos valores por los de tu base de datos PostgreSQL
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://admin:admin@localhost:5432/reconocimiento_facial_db"
)

# Función para obtener las dimensiones del modelo PCA
def get_pca_dimensions():
    """Obtiene las dimensiones del modelo PCA cargado."""
    try:
        with open('models/pca_model.pkl', 'rb') as f:
            pca_model = pickle.load(f)
        return pca_model.n_components_
    except Exception as e:
        print(f"Error al cargar el modelo PCA: {e}")
        return 33  # Valor por defecto

# `create_engine` es el punto de entrada a la base de datos.
# `echo=True` es útil para depuración, ya que muestra las sentencias SQL generadas.
engine = create_engine(DATABASE_URL, echo=False) # Deja echo en False para producción

# `sessionmaker` crea una clase de sesión para interactuar con la base de datos.
# `autocommit=False`: Las transacciones no se confirman automáticamente.
# `autoflush=False`: Los objetos no se "sincronizan" con la base de datos automáticamente.
# `bind=engine`: Asocia la sesión con el motor de base de datos.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# `declarative_base` es una base para nuestras clases de modelos de SQLAlchemy.
Base = declarative_base()

# --- Definición del Modelo de Usuario ---
# Aquí definimos cómo se verá la tabla 'users' en nuestra base de datos.
class User(Base):
    __tablename__ = "users" # Nombre de la tabla en PostgreSQL

    # ID del usuario, usaremos UUID para IDs únicos y robustos.
    # Si prefieres IDs enteros, cambia UUIDType a Integer y genera automáticamente.
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True) # Nombre de la persona
    email = Column(String, unique=True, index=True) # Email único del usuario
    telefono = Column(String, index=True) # Teléfono del usuario
    requested = Column(Boolean, default=False, index=True) # Estado "Requested" para alertas
    created_at = Column(DateTime, default=datetime.utcnow) # Fecha de creación
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) # Fecha de actualización
    
    # Campo para almacenar el embedding del rostro (Vector de características)
    # Las dimensiones se obtienen dinámicamente del modelo PCA
    embedding = Column(Vector(get_pca_dimensions())) # Tipo de dato VECTOR de pgvector

    # Opcional: Para el caso de múltiples embeddings por usuario,
    # podrías tener una tabla separada 'FaceEmbeddings'
    # o almacenar un array de embeddings si tu ORM lo soporta bien.
    # Por ahora, mantendremos un embedding por fila, lo que permite múltiples filas por usuario ID.
    
    # Puedes añadir más campos si necesitas:
    # image_url = Column(String) # Si guardas la URL de la imagen original

    def __repr__(self):
        # Representación para depuración
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}', telefono='{self.telefono}', requested={self.requested}, embedding_shape={self.embedding.shape if self.embedding is not None else None})>"

# --- Función para crear las tablas en la base de datos ---
# Esta función debe ser llamada una vez para inicializar tu esquema de BD.
def create_db_tables():
    Base.metadata.create_all(bind=engine)
    print("Tablas de la base de datos creadas/verificadas.")

# --- Dependencia de FastAPI para obtener una sesión de BD ---
# Esta es una función generadora que se usa con `Depends` en las rutas de FastAPI.
# Asegura que una sesión de base de datos se abre y se cierra correctamente.
def get_db():
    db = SessionLocal() # Abre una nueva sesión de base de datos
    try:
        yield db # Pasa la sesión a la ruta de FastAPI
    finally:
        db.close() # Cierra la sesión después de que la ruta ha terminado

# --- Bloque de Prueba para Inicialización de DB ---
if __name__ == "__main__":
    print("Intentando crear/verificar tablas de la base de datos...")
    create_db_tables()
    print("Recuerda: Si es la primera vez, necesitas haber habilitado la extensión 'vector' en PostgreSQL.")
    print("Ejecuta 'CREATE EXTENSION vector;' en tu base de datos si aún no lo has hecho.")