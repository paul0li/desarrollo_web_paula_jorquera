from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import json

DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# --- Models ---

class Region(Base):
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    comunas = relationship('Comuna', backref='region', lazy=True)

class Comuna(Base):
    __tablename__ = 'comuna'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)
    actividades = relationship('Actividad', backref='comuna', lazy=True)

class Actividad(Base):
    __tablename__ = 'actividad'
    id = Column(Integer, primary_key=True, autoincrement=True)
    comuna_id = Column(Integer, ForeignKey('comuna.id'), nullable=False)
    sector = Column(String(100), nullable=True)
    nombre = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False)
    celular = Column(String(15), nullable=True)
    dia_hora_inicio = Column(DateTime, nullable=False)
    dia_hora_termino = Column(DateTime, nullable=True)
    descripcion = Column(String(500), nullable=True)
    fotos = relationship('Foto', backref='actividad', lazy=True, cascade="all, delete-orphan")
    contactos = relationship('ContactarPor', backref='actividad', lazy=True, cascade="all, delete-orphan")
    temas = relationship('ActividadTema', backref='actividad', lazy=True, cascade="all, delete-orphan")

class Foto(Base):
    __tablename__ = 'foto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ruta_archivo = Column(String(300), nullable=False)
    nombre_archivo = Column(String(300), nullable=False)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), nullable=False)

class ContactarPor(Base):
    __tablename__ = 'contactar_por'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(Enum('whatsapp', 'telegram', 'X', 'instagram', 'tiktok', 'otra'), nullable=False)
    identificador = Column(String(150), nullable=False)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), nullable=False)

class ActividadTema(Base):
    __tablename__ = 'actividad_tema'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tema = Column(Enum('música', 'deporte', 'ciencias', 'religión', 'política', 'tecnología', 'juegos', 'baile', 'comida', 'otro'), nullable=False)
    glosa_otro = Column(String(15), nullable=True)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), nullable=False)

# --- Database Functions ---

def get_regions():
    session = SessionLocal()
    regions = session.query(Region).all()
    session.close()
    return regions

def get_comunas(region_id):
    session = SessionLocal()
    comunas = session.query(Comuna).filter_by(region_id=region_id).all()
    session.close()
    return comunas

def get_actividades(comuna_id):
    session = SessionLocal()
    actividades = session.query(Actividad).filter_by(comuna_id=comuna_id).all()
    session.close()
    return actividades
    
def create_actividad(comuna_id, sector, nombre, email, celular, dia_hora_inicio, dia_hora_termino, descripcion):
    session = SessionLocal()
    actividad = Actividad(
        comuna_id=comuna_id, sector=sector, nombre=nombre,
        email=email, celular=celular, dia_hora_inicio=dia_hora_inicio,
        dia_hora_termino=dia_hora_termino, descripcion=descripcion
    )
    session.add(actividad)
    session.commit()
    session.close()
    return actividad

def create_contacto_por(actividad_id, nombre, identificador):
    session = SessionLocal()
    contacto = ContactarPor(
        actividad_id=actividad_id, nombre=nombre, identificador=identificador
    )
    session.add(contacto)
    session.commit()
    session.close()
    return contacto

def create_foto(actividad_id, ruta_archivo, nombre_archivo):
    session = SessionLocal()
    foto = Foto(
        actividad_id=actividad_id, ruta_archivo=ruta_archivo, nombre_archivo=nombre_archivo
    )
    session.add(foto)
    session.commit()
    session.close()
    return foto
