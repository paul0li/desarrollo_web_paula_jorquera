from flask import Flask, request, render_template, redirect, url_for, flash, session, jsonify, abort, send_from_directory
from werkzeug.utils import secure_filename
from db.db import (
    # Modelos
    Region, Comuna, Actividad, Foto, ContactarPor, ActividadTema,
    # Funciones de consulta
    get_regions, get_comunas, get_actividades, get_actividades_count,
    get_ultimas_actividades, get_actividades_paginadas, get_actividad_detalle,
    get_fotos_by_actividad, get_temas_by_actividad, get_contactos_by_actividad,
    get_estadisticas_region, get_estadisticas_tema,
    # Funciones de creación
    create_actividad, create_tema, create_contacto_por, create_foto
)
import os
import datetime
import hashlib
import uuid

# Configuración de la aplicación
UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'programacionweb_tarea2_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Registrar funciones globales para las plantillas
app.jinja_env.globals.update(get_temas_by_actividad=get_temas_by_actividad)

# Funciones auxiliares
def allowed_file(filename):
    """Verifica si la extensión del archivo es permitida"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file):
    """Guarda un archivo y devuelve el nombre seguro"""
    if file and allowed_file(file.filename):
        # Generar un nombre de archivo único
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        
        # Guardar el archivo en la carpeta de uploads
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        print(f"[DEBUG] Archivo guardado en: {file_path}")
        return unique_filename
    return None

# --- Rutas principales ---

@app.route('/')
def index():
    """Página principal que muestra las últimas actividades"""
    # Obtener las últimas 5 actividades usando la función de db.py
    actividades = get_ultimas_actividades(limit=5)
    
    # Obtener fotos para cada actividad
    actividades_con_fotos = []
    for act in actividades:
        fotos = get_fotos_by_actividad(act[0].id)
        actividades_con_fotos.append((act[0], act[1], act[2], act[3], fotos))
    
    return render_template('portada.html', actividades=actividades_con_fotos)

# --- Rutas de actividades ---

@app.route('/form', methods=['GET'])
def form():
    """Muestra el formulario para agregar una nueva actividad"""
    # Obtener todas las regiones para el formulario usando la función de db.py
    regiones = get_regions()
    return render_template('form.html', regiones=regiones)

# --- Rutas de API ---

@app.route('/api/comunas/<int:region_id>')
def get_comunas_by_region(region_id):
    """API para obtener comunas por región"""
    # Usar la función get_comunas de db.py
    comunas = get_comunas(region_id)
    return jsonify([{'id': comuna.id, 'nombre': comuna.nombre} for comuna in comunas])

@app.route('/agregar-actividad', methods=['POST'])
def agregar_actividad():
    """Procesa el formulario para agregar una nueva actividad"""
    try:
        print("\n[DEBUG] Recibiendo datos del formulario de actividad")
        print(f"[DEBUG] Método de la solicitud: {request.method}")
        print(f"[DEBUG] Encabezados: {request.headers}")
        
        # Validar datos del formulario en el servidor
        comuna_id = request.form.get('comuna')
        sector = request.form.get('sector')
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        celular = request.form.get('celular')
        inicio = request.form.get('inicio')
        termino = request.form.get('termino')
        descripcion = request.form.get('descripcion')
        # Obtener múltiples temas
        tema_nombres = request.form.getlist('tema[]')
        tema_otro = request.form.get('temaOtro')
        # Obtener métodos de contacto múltiples
        contactar_nombres = request.form.getlist('contactar[]')
        contactar_extras = {}
        
        # Procesar los campos de contacto extra
        for key, value in request.form.items():
            if key.startswith('contactoExtra'):
                # Extraer el nombre del método de contacto de la clave usando una forma más robusta
                import re
                match = re.search(r'contactoExtra\[(.*?)\]', key)
                if match:
                    contact_method = match.group(1)
                    contactar_extras[contact_method] = value
        
        # Imprimir para depuración
        print(f"[DEBUG] Claves de contacto extras sin procesar: {[k for k in request.form.keys() if k.startswith('contactoExtra')]}")
        print(f"[DEBUG] Contactar extras procesados: {contactar_extras}")
        print(f"[DEBUG] Temas: {[t for t in tema_nombres]}")
        
        print("\n[DEBUG] Datos recibidos del formulario:")
        print(f"[DEBUG] Comuna ID: {comuna_id}")
        print(f"[DEBUG] Sector: {sector}")
        print(f"[DEBUG] Nombre: {nombre}")
        print(f"[DEBUG] Email: {email}")
        print(f"[DEBUG] Celular: {celular}")
        print(f"[DEBUG] Inicio: {inicio}")
        print(f"[DEBUG] Termino: {termino}")
        print(f"[DEBUG] Tema: {tema_nombres}")
        print(f"[DEBUG] Tema Otro: {tema_otro if tema_otro else 'Ninguno'}")
        
        # Verificar si hay archivos adjuntos
        print(f"\n[DEBUG] Archivos recibidos: {len(request.files.getlist('foto[]'))}")
        for i, foto in enumerate(request.files.getlist('foto[]')):
            print(f"[DEBUG] Foto {i+1}: {foto.filename} ({foto.content_type})")
        
        
        # Validaciones del servidor
        print("\n[DEBUG] Iniciando validaciones del servidor")
        errores = {}
        
        # Validar comuna_id - debe ser un número entero
        print(f"[DEBUG] Validando comuna_id: '{comuna_id}', tipo: {type(comuna_id)}")
        try:
            # Intentar obtener la comuna por nombre si es un string
            if comuna_id and not comuna_id.isdigit():
                print(f"[DEBUG] Comuna_id no es un número: '{comuna_id}'. Intentando buscar por nombre...")
                session = SessionLocal()
                comuna = session.query(Comuna).filter(Comuna.nombre == comuna_id).first()
                session.close()
                
                if comuna:
                    comuna_id = str(comuna.id)
                    print(f"[DEBUG] Comuna encontrada por nombre. ID: {comuna_id}")
                else:
                    print(f"[DEBUG] No se encontró comuna con nombre: '{comuna_id}'")
                    errores['comuna'] = f"No se encontró la comuna '{comuna_id}'"
            elif not comuna_id:
                errores['comuna'] = 'Debe seleccionar una comuna'
                print("[DEBUG] Error: Comuna no seleccionada")
        except Exception as e:
            print(f"[DEBUG] Error al validar comuna: {str(e)}")
            errores['comuna'] = f"Error al validar comuna: {str(e)}"
        
        if not nombre or len(nombre) < 3 or len(nombre) > 80:
            errores['nombre'] = 'El nombre debe tener entre 3 y 80 caracteres'
            print(f"[DEBUG] Error: Nombre inválido: {nombre}")
        if not email or '@' not in email:
            errores['email'] = 'Debe ingresar un email válido'
            print(f"[DEBUG] Error: Email inválido: {email}")
        if not inicio:
            errores['inicio'] = 'Debe ingresar una fecha y hora de inicio'
            print("[DEBUG] Error: Fecha de inicio no proporcionada")
        if not tema_nombres:
            errores['tema'] = 'Debe seleccionar al menos un tema'
            print("[DEBUG] Error: Ningún tema seleccionado")
        if 'otro' in tema_nombres and (not tema_otro or len(tema_otro) < 3):
            errores['temaOtro'] = 'Debe especificar el tema'
            print("[DEBUG] Error: Tema 'otro' sin especificar")
        
        # Verificar archivos
        fotos = request.files.getlist('foto[]')
        if not fotos or not any(foto and foto.filename for foto in fotos):
            errores['foto'] = 'Debe subir al menos una foto'
            print("[DEBUG] Error: No se proporcionaron fotos")
        
        # Si hay errores, volver al formulario
        if errores:
            print(f"\n[DEBUG] Se encontraron {len(errores)} errores de validación:")
            for campo, mensaje in errores.items():
                print(f"[DEBUG] - {campo}: {mensaje}")
            regiones = get_regions()
            return render_template('form.html', regiones=regiones, errores=errores, form_data=request.form)
        
        # Convertir fechas a formato datetime
        print("\n[DEBUG] Convirtiendo fechas a formato datetime")
        try:
            dia_hora_inicio = datetime.datetime.fromisoformat(inicio)
            print(f"[DEBUG] Fecha de inicio convertida: {dia_hora_inicio}")
            
            if termino:
                dia_hora_termino = datetime.datetime.fromisoformat(termino)
                print(f"[DEBUG] Fecha de término convertida: {dia_hora_termino}")
            else:
                dia_hora_termino = None
                print("[DEBUG] No se proporcionó fecha de término")
        except ValueError as e:
            print(f"[DEBUG] Error al convertir fechas: {str(e)}")
            flash(f'Error en el formato de fecha: {str(e)}', 'error')
            regiones = get_regions()
            return render_template('form.html', regiones=regiones, errores={'fecha': str(e)}, form_data=request.form)
        
        # Crear nueva actividad usando la función de db.py
        print("\n[DEBUG] Creando nueva actividad en la base de datos")
        print(f"[DEBUG] Parámetros para create_actividad:")
        print(f"[DEBUG] - comuna_id: '{comuna_id}' (tipo: {type(comuna_id)})")
        print(f"[DEBUG] - sector: '{sector}'")
        print(f"[DEBUG] - nombre: '{nombre}'")
        print(f"[DEBUG] - email: '{email}'")
        print(f"[DEBUG] - celular: '{celular}'")
        print(f"[DEBUG] - dia_hora_inicio: {dia_hora_inicio}")
        print(f"[DEBUG] - dia_hora_termino: {dia_hora_termino}")
        print(f"[DEBUG] - descripcion: '{descripcion}'")
        
        try:
            # Asegurarse de que comuna_id sea un entero
            try:
                comuna_id_int = int(comuna_id)
                print(f"[DEBUG] Comuna ID convertido a entero: {comuna_id_int}")
            except (ValueError, TypeError) as e:
                print(f"[DEBUG] Error al convertir comuna_id a entero: {str(e)}")
                errores['comuna'] = f"ID de comuna inválido: {comuna_id}"
                regiones = get_regions()
                return render_template('form.html', regiones=regiones, errores=errores, form_data=request.form)
            
            nueva_actividad = create_actividad(
                comuna_id=comuna_id_int,
                sector=sector,
                nombre=nombre,
                email=email,
                celular=celular,
                dia_hora_inicio=dia_hora_inicio,
                dia_hora_termino=dia_hora_termino,
                descripcion=descripcion
            )
            print(f"[DEBUG] Actividad creada exitosamente con ID: {nueva_actividad.id}")
        except Exception as e:
            print(f"[DEBUG] Error al crear actividad: {str(e)}")
            print(f"[DEBUG] Tipo de excepción: {type(e).__name__}")
            import traceback
            print(f"[DEBUG] Traceback: {traceback.format_exc()}")
            flash(f'Error al crear actividad: {str(e)}', 'error')
            regiones = get_regions()
            return render_template('form.html', regiones=regiones, errores={'db': str(e)}, form_data=request.form)
        
        # Agregar temas usando la función de db.py
        print("\n[DEBUG] Agregando temas a la actividad")
        print(f"[DEBUG] Temas seleccionados: {tema_nombres}")
        
        for tema_nombre in tema_nombres:
            try:
                # Determinar si es necesario incluir glosa_otro
                glosa = None
                if tema_nombre == 'otro' and tema_otro:
                    glosa = tema_otro
                
                print(f"[DEBUG] Agregando tema: {tema_nombre} con glosa: {glosa}")
                tema = create_tema(
                    actividad_id=nueva_actividad.id,
                    tema=tema_nombre,
                    glosa_otro=glosa
                )
                print(f"[DEBUG] Tema agregado exitosamente con ID: {tema.id}")
            except Exception as e:
                print(f"[DEBUG] Error al agregar tema {tema_nombre}: {str(e)}")
                flash(f'Error al agregar tema {tema_nombre}: {str(e)}', 'error')
                # Continuamos a pesar del error
        
        # Agregar métodos de contacto múltiples si se proporcionan
        if contactar_nombres:
            print(f"[DEBUG] Métodos de contacto seleccionados: {contactar_nombres}")
            print(f"[DEBUG] Datos de contacto extras: {contactar_extras}")
            
            for contactar_nombre in contactar_nombres:
                try:
                    # Verificar si hay un identificador para este método de contacto
                    if contactar_nombre in contactar_extras:
                        contactar_id = contactar_extras[contactar_nombre]
                        if contactar_id:  # Verificar que el identificador no esté vacío
                            print(f"[DEBUG] Agregando contacto: {contactar_nombre} - {contactar_id}")
                            try:
                                contacto = create_contacto_por(
                                    actividad_id=nueva_actividad.id, 
                                    nombre=contactar_nombre, 
                                    identificador=contactar_id
                                )
                                print(f"[DEBUG] Contacto agregado con ID: {contacto.id}")
                            except Exception as e:
                                print(f"[DEBUG] Error al crear contacto en la base de datos: {str(e)}")
                                # Si hay un error específico con el Enum, intentar convertir a mayúsculas/minúsculas
                                if 'Enum' in str(e) or 'enum' in str(e):
                                    print(f"[DEBUG] Intentando corregir valor de Enum para: {contactar_nombre}")
                                    # Intentar con la primera letra en mayúscula
                                    try:
                                        nombre_corregido = contactar_nombre.capitalize()
                                        contacto = create_contacto_por(
                                            actividad_id=nueva_actividad.id, 
                                            nombre=nombre_corregido, 
                                            identificador=contactar_id
                                        )
                                        print(f"[DEBUG] Contacto agregado con nombre corregido: {nombre_corregido}")
                                    except Exception as e2:
                                        print(f"[DEBUG] Error al intentar con nombre corregido: {str(e2)}")
                                        raise e  # Re-lanzar el error original
                        else:
                            print(f"[DEBUG] El identificador para {contactar_nombre} está vacío, no se guardará")
                    else:
                        print(f"[DEBUG] No se encontró identificador para {contactar_nombre} en {list(contactar_extras.keys())}")
                except Exception as e:
                    print(f"[DEBUG] Error al agregar contacto {contactar_nombre}: {str(e)}")
                    flash(f'Error al agregar contacto {contactar_nombre}: {str(e)}', 'error')
                    # Continuamos a pesar del error
        
        # Procesar fotos
        print("\n[DEBUG] Procesando fotos")
        fotos = request.files.getlist('foto[]')
        fotos_guardadas = 0
        
        # Imprimir información detallada sobre las fotos recibidas
        print(f"[DEBUG] Número total de fotos recibidas: {len(fotos)}")
        for i, foto in enumerate(fotos):
            if foto and foto.filename:
                print(f"[DEBUG] Foto {i+1}: {foto.filename} ({foto.content_type})")
            else:
                print(f"[DEBUG] Foto {i+1}: No tiene nombre de archivo o está vacía")
        
        # Procesar cada foto individualmente
        for i, foto in enumerate(fotos):
            if foto and foto.filename:
                try:
                    print(f"[DEBUG] Procesando foto {i+1}: {foto.filename}")
                    
                    # Guardar el archivo físicamente
                    filename = save_file(foto)
                    if filename:
                        print(f"[DEBUG] Archivo guardado con nombre: {filename}")
                        
                        # Guardar la referencia en la base de datos
                        try:
                            foto_obj = create_foto(
                                actividad_id=nueva_actividad.id,
                                ruta_archivo=filename,  # Solo guardamos el nombre del archivo
                                nombre_archivo=filename
                            )
                            print(f"[DEBUG] Foto guardada exitosamente en BD con ID: {foto_obj.id}")
                            fotos_guardadas += 1
                        except Exception as db_error:
                            print(f"[DEBUG] Error al guardar foto en la base de datos: {str(db_error)}")
                            import traceback
                            print(f"[DEBUG] Traceback: {traceback.format_exc()}")
                    else:
                        print(f"[DEBUG] Error al guardar archivo físico de foto {i+1}")
                except Exception as e:
                    print(f"[DEBUG] Error al procesar foto {i+1}: {str(e)}")
                    import traceback
                    print(f"[DEBUG] Traceback: {traceback.format_exc()}")
                    flash(f'Error al procesar foto: {str(e)}', 'error')
                    # Continuamos a pesar del error
        
        print(f"\n[DEBUG] Se guardaron {fotos_guardadas} fotos de {len(fotos)} enviadas")
        print("\n[DEBUG] Proceso de creación de actividad completado exitosamente")
        
        flash('Actividad agregada exitosamente', 'success')
        return redirect(url_for('index'))
    
    except Exception as e:
        flash(f'Error al agregar actividad: {str(e)}', 'error')
        regiones = get_regions()
        return render_template('form.html', regiones=regiones, errores={'general': str(e)}, form_data=request.form)

@app.route('/listado')
@app.route('/listado/<int:pagina>')
def listado(pagina=1):
    """Muestra el listado completo de actividades con paginación"""
    # Configuración de paginación
    items_por_pagina = 5
    
    # Obtener el total de actividades usando la función de db.py
    total_actividades = get_actividades_count()
    total_paginas = (total_actividades + items_por_pagina - 1) // items_por_pagina
    
    # Obtener actividades para la página actual usando la función de db.py
    actividades = get_actividades_paginadas(page_size=items_por_pagina, page=pagina)
    
    # Obtener fotos para cada actividad
    actividades_con_fotos = []
    for act in actividades:
        fotos = get_fotos_by_actividad(act[0].id)
        actividades_con_fotos.append((act[0], act[1], act[2], act[3], fotos))
    
    return render_template(
        'listado.html', 
        actividades=actividades_con_fotos, 
        pagina_actual=pagina, 
        total_paginas=total_paginas
    )

@app.route('/estadisticas')
def estadisticas():
    """Muestra estadísticas de actividades por región y tema"""
    # Obtener estadísticas usando las funciones de db.py
    #stats_region = get_estadisticas_region()
    #stats_tema = get_estadisticas_tema()
    
    return render_template('estadisticas.html')

@app.route('/api/regiones')
def api_regiones():
    """API endpoint para obtener todas las regiones"""
    try:
        regiones = get_regions()
        # Convertir a formato JSON
        regiones_json = [{'id': r.id, 'nombre': r.nombre} for r in regiones]
        return jsonify(regiones_json)
    except Exception as e:
        print(f"[DEBUG] Error al obtener regiones: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/comunas')
def api_comunas():
    """API endpoint para obtener comunas por región"""
    try:
        region_id = request.args.get('region_id')
        region_nombre = request.args.get('region')
        
        if region_id:
            # Si se proporciona el ID de la región
            comunas = get_comunas(region_id)
        elif region_nombre:
            # Si se proporciona el nombre de la región, buscar su ID primero
            session = SessionLocal()
            region = session.query(Region).filter(Region.nombre == region_nombre).first()
            session.close()
            
            if region:
                comunas = get_comunas(region.id)
            else:
                return jsonify({'error': f"Región no encontrada: {region_nombre}"}), 404
        else:
            # Si no se proporciona región, devolver todas las comunas
            session = SessionLocal()
            comunas = session.query(Comuna).all()
            session.close()
        
        # Convertir a formato JSON
        comunas_json = [{'id': c.id, 'nombre': c.nombre, 'region_id': c.region_id} for c in comunas]
        return jsonify(comunas_json)
    except Exception as e:
        print(f"[DEBUG] Error al obtener comunas: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/actividad/<int:id>')
def ver_actividad(id):
    """Muestra los detalles de una actividad específica"""
    # Obtener detalles de la actividad usando las funciones de db.py
    actividad = get_actividad_detalle(id)
    if not actividad:
        abort(404)
    
    fotos = get_fotos_by_actividad(id)
    temas = get_temas_by_actividad(id)
    contactos = get_contactos_by_actividad(id)
    
    return render_template('actividad.html', 
                          actividad=actividad[0], 
                          comuna=actividad[1], 
                          region=actividad[2], 
                          fotos=fotos, 
                          temas=temas, 
                          contactos=contactos)




if __name__ == '__main__':
    app.run(debug=True, port=5000)
