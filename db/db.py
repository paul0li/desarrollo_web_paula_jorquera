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
    actividad_id = Column(Integer, ForeignKey('actividad.id'), primary_key=True, nullable=False)

class ContactarPor(Base):
    __tablename__ = 'contactar_por'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(Enum('whatsapp', 'telegram', 'X', 'instagram', 'tiktok', 'otra'), nullable=False)
    identificador = Column(String(150), nullable=False)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), primary_key=True, nullable=False)

class ActividadTema(Base):
    __tablename__ = 'actividad_tema'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tema = Column(Enum('música', 'deporte', 'ciencias', 'religión', 'política', 'tecnología', 'juegos', 'baile', 'comida', 'otro'), nullable=False)
    glosa_otro = Column(String(15), nullable=True)
    actividad_id = Column(Integer, ForeignKey('actividad.id'), primary_key=True, nullable=False)

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

def get_actividades(comuna_id=None, limit=None, offset=None):
    session = SessionLocal()
    query = session.query(Actividad)
    
    if comuna_id:
        query = query.filter_by(comuna_id=comuna_id)
    
    query = query.order_by(Actividad.dia_hora_inicio.desc())
    
    if limit:
        query = query.limit(limit)
    
    if offset:
        query = query.offset(offset)
    
    actividades = query.all()
    session.close()
    return actividades

def get_actividad_by_id(actividad_id):
    session = SessionLocal()
    actividad = session.query(Actividad).filter_by(id=actividad_id).first()
    session.close()
    return actividad

def get_actividades_count():
    session = SessionLocal()
    count = session.query(Actividad).count()
    session.close()
    return count

def get_ultimas_actividades(limit=5):
    session = SessionLocal()
    actividades = session.query(
        Actividad, Comuna, Region, ActividadTema
    ).join(
        Comuna, Actividad.comuna_id == Comuna.id
    ).join(
        Region, Comuna.region_id == Region.id
    ).join(
        ActividadTema, Actividad.id == ActividadTema.actividad_id
    ).order_by(
        Actividad.dia_hora_inicio.desc()
    ).limit(limit).all()
    session.close()
    return actividades

def get_actividades_paginadas(page_size=5, page=1):
    offset = (page - 1) * page_size
    session = SessionLocal()
    
    # Primero obtenemos las actividades paginadas sin el join con temas
    actividades_base = session.query(
        Actividad, Comuna, Region
    ).join(
        Comuna, Actividad.comuna_id == Comuna.id
    ).join(
        Region, Comuna.region_id == Region.id
    ).order_by(
        Actividad.dia_hora_inicio.desc()
    ).offset(offset).limit(page_size).all()
    
    # Luego, para cada actividad, obtenemos su primer tema (para mantener compatibilidad)
    resultado = []
    for act, comuna, region in actividades_base:
        # Obtener el primer tema de la actividad
        tema = session.query(ActividadTema).filter_by(actividad_id=act.id).first()
        if tema:
            resultado.append((act, comuna, region, tema))
        else:
            # Si no hay tema, creamos un objeto vacío para mantener la estructura
            from sqlalchemy import inspect
            mapper = inspect(ActividadTema)
            tema_vacio = ActividadTema()
            tema_vacio.tema = "Sin tema"
            tema_vacio.glosa_otro = None
            resultado.append((act, comuna, region, tema_vacio))
    
    session.close()
    return resultado

def get_actividad_detalle(actividad_id):
    session = SessionLocal()
    actividad = session.query(
        Actividad, Comuna, Region
    ).join(
        Comuna, Actividad.comuna_id == Comuna.id
    ).join(
        Region, Comuna.region_id == Region.id
    ).filter(
        Actividad.id == actividad_id
    ).first()
    session.close()
    return actividad

def get_fotos_by_actividad(actividad_id):
    session = SessionLocal()
    fotos = session.query(Foto).filter_by(actividad_id=actividad_id).all()
    session.close()
    return fotos

def get_temas_by_actividad(actividad_id):
    session = SessionLocal()
    temas = session.query(ActividadTema).filter_by(actividad_id=actividad_id).all()
    session.close()
    return temas

def get_contactos_by_actividad(actividad_id):
    session = SessionLocal()
    contactos = session.query(ContactarPor).filter_by(actividad_id=actividad_id).all()
    session.close()
    return contactos

def get_estadisticas_region():
    session = SessionLocal()
    stats = session.query(
        Region.nombre, session.func.count(Actividad.id)
    ).join(
        Comuna, Region.id == Comuna.region_id
    ).join(
        Actividad, Comuna.id == Actividad.comuna_id
    ).group_by(
        Region.nombre
    ).all()
    session.close()
    return stats

def get_estadisticas_tema():
    session = SessionLocal()
    stats = session.query(
        ActividadTema.tema, session.func.count(ActividadTema.id)
    ).group_by(
        ActividadTema.tema
    ).all()
    session.close()
    return stats
    
def create_actividad(comuna_id, sector, nombre, email, celular, dia_hora_inicio, dia_hora_termino, descripcion):
    session = SessionLocal()
    actividad = Actividad(
        comuna_id=comuna_id, sector=sector, nombre=nombre,
        email=email, celular=celular, dia_hora_inicio=dia_hora_inicio,
        dia_hora_termino=dia_hora_termino, descripcion=descripcion
    )
    session.add(actividad)
    session.commit()
    session.refresh(actividad)  # Refresh to get the generated ID
    actividad_id = actividad.id
    session.close()
    return actividad

def create_tema(actividad_id, tema, glosa_otro=None):
    session = SessionLocal()
    tema_obj = ActividadTema(
        actividad_id=actividad_id, tema=tema, glosa_otro=glosa_otro
    )
    session.add(tema_obj)
    session.commit()
    
    # Get the ID before closing the session
    tema_id = tema_obj.id
    
    # Create a detached copy of the object's attributes
    tema_dict = {
        'id': tema_id,
        'actividad_id': actividad_id,
        'tema': tema,
        'glosa_otro': glosa_otro
    }
    
    session.close()
    
    # Return the detached object with its ID
    return tema_obj

def create_contacto_por(actividad_id, nombre, identificador):
    session = SessionLocal()
    contacto = ContactarPor(
        actividad_id=actividad_id, nombre=nombre, identificador=identificador
    )
    session.add(contacto)
    session.commit()
    
    # Get the ID before closing the session
    contacto_id = contacto.id
    
    # Create a detached copy of the object's attributes
    contacto_dict = {
        'id': contacto_id,
        'actividad_id': actividad_id,
        'nombre': nombre,
        'identificador': identificador
    }
    
    session.close()
    
    # Return the detached object with its ID
    return contacto

def create_foto(actividad_id, ruta_archivo, nombre_archivo):
    session = SessionLocal()
    foto = Foto(
        actividad_id=actividad_id, ruta_archivo=ruta_archivo, nombre_archivo=nombre_archivo
    )
    session.add(foto)
    session.commit()
    
    # Get the ID before closing the session
    foto_id = foto.id
    
    # Create a detached copy of the object's attributes
    foto_dict = {
        'id': foto_id,
        'actividad_id': actividad_id,
        'ruta_archivo': ruta_archivo,
        'nombre_archivo': nombre_archivo
    }
    
    session.close()
    
    # Return the detached object with its ID
    return foto
