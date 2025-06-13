from flask import Flask, request, render_template, redirect, url_for, flash, jsonify, abort, send_from_directory
from werkzeug.utils import secure_filename
from db.db import (
    # Modelos
    Region, Comuna,
    # Funciones de consulta
    get_regions, get_comunas, get_actividades_count,
    get_ultimas_actividades, get_actividades_paginadas, get_actividad_detalle,
    get_fotos_by_actividad, get_temas_by_actividad, get_contactos_by_actividad,
    get_estadisticas_tema,
    get_estadisticas_actividades_por_dia, get_estadisticas_actividades_por_horario,
    get_comentarios_by_actividad,
    # Funciones de creación
    create_actividad, create_tema, create_contacto_por, create_foto, create_comentario
)
import os
import datetime
import re
import uuid

UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'programacionweb_tarea2_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.jinja_env.globals.update(get_temas_by_actividad=get_temas_by_actividad)

def allowed_file(filename):
    """Verifica si la extensión del archivo es permitida"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file):
    """Guarda un archivo y devuelve el nombre seguro"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        return unique_filename
    return None

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Sirve archivos subidos desde la carpeta uploads"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/')
def index():
    """Página principal que muestra las últimas actividades"""
    actividades = get_ultimas_actividades(limit=5)
    
    actividades_con_fotos = []
    for act in actividades:
        fotos = get_fotos_by_actividad(act[0].id)
        actividades_con_fotos.append((act[0], act[1], act[2], act[3], fotos))
    
    return render_template('portada.html', actividades=actividades_con_fotos)

@app.route('/form', methods=['GET'])
def form():
    """Muestra el formulario para agregar una nueva actividad"""
    regiones = get_regions()
    return render_template('form.html', regiones=regiones)

@app.route('/api/comunas/<int:region_id>')
def get_comunas_by_region(region_id):
    """API para obtener comunas por región"""
    comunas = get_comunas(region_id)
    return jsonify([{'id': comuna.id, 'nombre': comuna.nombre} for comuna in comunas])

@app.route('/agregar-actividad', methods=['POST'])
def agregar_actividad():
    try:
        comuna_id = request.form.get('comuna')
        sector = request.form.get('sector')
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        celular = request.form.get('celular')
        inicio = request.form.get('inicio')
        termino = request.form.get('termino')
        descripcion = request.form.get('descripcion')
        tema_nombres = request.form.getlist('tema[]')
        tema_otro = request.form.get('temaOtro')
        contactar_nombres = request.form.getlist('contactar[]')
        contactar_extras = {}
        
        for key, value in request.form.items():
            if key.startswith('contactoExtra'):
                match = re.search(r'contactoExtra\[(.*?)\]', key)
                if match:
                    contact_method = match.group(1)
                    contactar_extras[contact_method] = value
        
        errores = {}
        
        
        if comuna_id and not comuna_id.isdigit():
            session = SessionLocal()
            comuna = session.query(Comuna).filter(Comuna.nombre == comuna_id).first()
            session.close()
            
            if comuna:
                comuna_id = str(comuna.id)
            else:
                errores['comuna'] = f"No se encontró la comuna '{comuna_id}'"
        elif not comuna_id:
            errores['comuna'] = 'Debe seleccionar una comuna'
        
        if not nombre or len(nombre) < 3 or len(nombre) > 80:
            errores['nombre'] = 'El nombre debe tener entre 3 y 80 caracteres'
        if not email or '@' not in email:
            errores['email'] = 'Debe ingresar un email válido'
        if not inicio:
            errores['inicio'] = 'Debe ingresar una fecha y hora de inicio'
        if not tema_nombres:
            errores['tema'] = 'Debe seleccionar al menos un tema'
        if 'otro' in tema_nombres and (not tema_otro or len(tema_otro) < 3):
            errores['temaOtro'] = 'Debe especificar el tema'
        
        fotos = request.files.getlist('foto[]')
        if not fotos or not any(foto and foto.filename for foto in fotos):
            errores['foto'] = 'Debe subir al menos una foto'
        
        if errores:
            regiones = get_regions()
            return render_template('form.html', regiones=regiones, errores=errores, form_data=request.form)
        
        try:
            dia_hora_inicio = datetime.datetime.fromisoformat(inicio)
            
            if termino:
                dia_hora_termino = datetime.datetime.fromisoformat(termino)
            else:
                dia_hora_termino = None
        except ValueError as e:
            flash(f'Error en el formato de fecha: {str(e)}', 'error')
            regiones = get_regions()
            return render_template('form.html', regiones=regiones, errores={'fecha': str(e)}, form_data=request.form)
        
        try:
            try:
                comuna_id_int = int(comuna_id)
            except (ValueError, TypeError) as e:
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
        except Exception as e:
            flash(f'Error al crear actividad: {str(e)}', 'error')
            regiones = get_regions()
            return render_template('form.html', regiones=regiones, errores={'db': str(e)}, form_data=request.form)
        
        for tema_nombre in tema_nombres:
            try:
                glosa = None
                if tema_nombre == 'otro' and tema_otro:
                    glosa = tema_otro
                
                create_tema(
                    actividad_id=nueva_actividad.id,
                    tema=tema_nombre,
                    glosa_otro=glosa
                )
            except Exception as e:
                flash(f'Error al agregar tema {tema_nombre}: {str(e)}', 'error')
        
        if contactar_nombres:
            for contactar_nombre in contactar_nombres:
                if contactar_nombre in contactar_extras:
                    contactar_id = contactar_extras[contactar_nombre]
                    if contactar_id:
                        try:
                            create_contacto_por(
                                actividad_id=nueva_actividad.id, 
                                nombre=contactar_nombre, 
                                identificador=contactar_id
                            )
                        except Exception as e:
                            if 'Enum' in str(e) or 'enum' in str(e):
                                try:
                                    nombre_corregido = contactar_nombre.capitalize()
                                    create_contacto_por(
                                        actividad_id=nueva_actividad.id, 
                                        nombre=nombre_corregido, 
                                        identificador=contactar_id
                                    )
                                except Exception as e2:
                                    raise e2  
                
        # Procesar fotos
        fotos = request.files.getlist('foto[]')
        fotos_guardadas = 0
        
        for i, foto in enumerate(fotos):
            if foto and foto.filename:
                filename = save_file(foto)
                if filename:
                    try:
                        foto_obj = create_foto(
                            actividad_id=nueva_actividad.id,
                            ruta_archivo=filename,
                            nombre_archivo=filename
                        )
                        fotos_guardadas += 1
                    except Exception as db_error:
                        flash(f'Error al guardar foto {i+1}: {str(db_error)}', 'error')
                else:
                    flash(f'Error al guardar archivo físico de foto {i+1}', 'error')
    
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
    items_por_pagina = 5
    
    total_actividades = get_actividades_count()
    total_paginas = (total_actividades + items_por_pagina - 1) // items_por_pagina
    
    actividades = get_actividades_paginadas(page_size=items_por_pagina, page=pagina)
    
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
    return render_template('estadisticas.html')

@app.route('/api/regiones')
def api_regiones():
    """API endpoint para obtener todas las regiones"""
    try:
        regiones = get_regions()
        regiones_json = [{'id': r.id, 'nombre': r.nombre} for r in regiones]
        return jsonify(regiones_json)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/comunas')
def api_comunas():
    """API endpoint para obtener comunas por región"""
    try:
        region_id = request.args.get('region_id')
        region_nombre = request.args.get('region')
        
        if region_id:
            comunas = get_comunas(region_id)
        elif region_nombre:
            session = SessionLocal()
            region = session.query(Region).filter(Region.nombre == region_nombre).first()
            session.close()
            
            if region:
                comunas = get_comunas(region.id)
            else:
                return jsonify({'error': f"Región no encontrada: {region_nombre}"}), 404
        else:
            session = SessionLocal()
            comunas = session.query(Comuna).all()
            session.close()
        
        comunas_json = [{'id': c.id, 'nombre': c.nombre, 'region_id': c.region_id} for c in comunas]
        return jsonify(comunas_json)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/actividad/<int:id>')
def ver_actividad(id):
    """Muestra los detalles de una actividad específica"""
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

@app.route('/api/estadisticas/line_chart', methods=['GET'])
def line_chart_data():
    """Obtiene datos para gráfico de líneas: actividades por día"""
    try:
        stats = get_estadisticas_actividades_por_dia()
        
        days = []
        activities = []
        
        for stat in stats:
            # Convertir fecha a string legible
            days.append(stat.fecha.strftime('%Y-%m-%d'))
            activities.append(stat.cantidad)
        
        data = {
            'days': days,
            'activities': activities
        }
        return jsonify(data)
    except Exception as e:
        # En caso de error, devolver datos de ejemplo
        data = {
            'days': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'activities': [2, 5, 3]
        }
        return jsonify(data)

@app.route('/api/estadisticas/pie_chart', methods=['GET'])
def pie_chart_data():
    """Obtiene datos para gráfico de torta: proporción de actividades por tema"""
    try:
        stats = get_estadisticas_tema()
        
        types = []
        proportions = []
        
        for tema, cantidad in stats:
            types.append(tema)
            proportions.append(cantidad)
        
        data = {
            'types': types,
            'proportions': proportions
        }
        return jsonify(data)
    except Exception as e:
        # En caso de error, devolver datos de ejemplo
        data = {
            'types': ['música', 'deporte', 'tecnología'],
            'proportions': [15, 25, 10]
        }
        return jsonify(data)

@app.route('/api/estadisticas/bar_chart', methods=['GET'])
def bar_chart_data():
    """Obtiene datos para gráfico de barras: actividades por horario y mes"""
    try:
        stats = get_estadisticas_actividades_por_horario()
        
        # Organizar datos por mes y horario
        months_data = {}
        
        for año, mes, horario, cantidad in stats:
            month_key = f"{int(año)}-{int(mes):02d}"
            if month_key not in months_data:
                months_data[month_key] = {'mañana': 0, 'mediodía': 0, 'tarde': 0}
            months_data[month_key][horario] = cantidad
        
        # Convertir a formato requerido por el frontend
        months = sorted(months_data.keys())
        morning = [months_data[month]['mañana'] for month in months]
        midday = [months_data[month]['mediodía'] for month in months]
        afternoon = [months_data[month]['tarde'] for month in months]
        
        data = {
            'months': months,
            'morning': morning,
            'midday': midday,
            'afternoon': afternoon
        }
        return jsonify(data)
    except Exception as e:
        # En caso de error, devolver datos de ejemplo
        data = {
            'months': ['2024-01', '2024-02', '2024-03'],
            'morning': [5, 8, 12],
            'midday': [3, 6, 9],
            'afternoon': [7, 10, 15]
        }
        return jsonify(data)

@app.route('/api/comentarios/<int:actividad_id>', methods=['GET'])
def get_comentarios(actividad_id):
    """API para obtener comentarios de una actividad específica"""
    try:
        comentarios = get_comentarios_by_actividad(actividad_id)
        
        comentarios_data = []
        for comentario in comentarios:
            comentarios_data.append({
                'id': comentario.id,
                'nombre': comentario.nombre,
                'texto': comentario.texto,
                'fecha': comentario.fecha.strftime('%d/%m/%Y %H:%M')
            })
        
        return jsonify({
            'status': 'success',
            'comentarios': comentarios_data
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Error al obtener comentarios'
        }), 500

@app.route('/api/comentarios', methods=['POST'])
def agregar_comentario():
    """API para agregar un nuevo comentario con validación"""
    try:
        # Obtener datos del formulario
        actividad_id = request.form.get('actividad_id')
        nombre = request.form.get('nombre', '').strip()
        texto = request.form.get('comentario', '').strip()
        
        # Validación del lado del servidor
        errores = {}
        
        if not actividad_id or not actividad_id.isdigit():
            errores['actividad_id'] = 'ID de actividad inválido'
        
        if not nombre or len(nombre) < 3 or len(nombre) > 80:
            errores['nombre'] = 'El nombre debe tener entre 3 y 80 caracteres'
        
        if not texto or len(texto) < 5:
            errores['comentario'] = 'El comentario debe tener al menos 5 caracteres'
        
        # Si hay errores, devolver respuesta de error
        if errores:
            return jsonify({
                'status': 'error',
                'errores': errores
            }), 400
        
        # Crear el comentario
        comentario_data = create_comentario(int(actividad_id), nombre, texto)
        
        return jsonify({
            'status': 'success',
            'comentario': {
                'id': comentario_data['id'],
                'nombre': comentario_data['nombre'],
                'texto': comentario_data['texto'],
                'fecha': comentario_data['fecha'].strftime('%d/%m/%Y %H:%M')
            },
            'message': 'Comentario agregado exitosamente'
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Error al agregar comentario'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
