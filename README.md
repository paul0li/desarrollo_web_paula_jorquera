# Plataforma de Actividades - Desarrollo Web TAREA 3

Este proyecto es una plataforma web para gestionar y visualizar actividades, desarrollada para el curso de Desarrollo Web en la Universidad de Chile. La aplicación permite registrar actividades, ver su listado, visualizar detalles y está preparada para mostrar estadísticas en futuras implementaciones.

## Implementación

### Tecnologías Utilizadas
- **Backend**: Python con Flask
- **Base de Datos**: MySQL con SQLAlchemy como ORM
- **Frontend**: HTML5, CSS3, JavaScript
- **Plantillas**: Jinja2

### Estructura del Proyecto

```
.
├── app.py                  # Aplicación principal Flask
├── .gitignore              # Archivos y carpetas ignorados por Git
├── requirements.txt        # Dependencias de Python
├── db/                     # Módulos de base de datos
│   ├── db.py               # Modelos y funciones de acceso a datos
│   ├── init_db.py          # Script de inicialización de la base de datos
│   ├── tarea2.sql          # Estructura de la base de datos
│   ├── region-comuna.sql   # Datos de regiones y comunas
│   └── create_user.sql     # Script para crear usuario de la base de datos
├── static/                 # Archivos estáticos
│   ├── css/                # Hojas de estilo
│   │   ├── base.css        # Estilos base y tipografía
│   │   ├── components.css  # Componentes reutilizables
│   │   ├── layout.css      # Estructura y responsividad
│   │   └── main.css        # Importa los otros archivos CSS
│   ├── js/                 # JavaScript
│   │   ├── validation.js   # Validación de formularios
│   │   └── visor.js        # Visor de imágenes
│   ├── img/                # Imágenes del sitio
│   └── uploads/            # Carpeta para archivos subidos (ignorada por Git)
├── templates/              # Plantillas Jinja2
│   ├── base.html           # Plantilla base con estructura común
│   ├── portada.html        # Página de inicio
│   ├── form.html           # Formulario para agregar actividades
│   ├── listado.html        # Listado de actividades con paginación
│   ├── actividad.html      # Detalle de una actividad
│   └── estadisticas.html   # Página de estadísticas (pendiente)
├── components/             # Componentes reutilizables del frontend
├── utils/                  # Utilidades y funciones auxiliares
└── venv/                   # Entorno virtual (ignorado por Git)
```

### Funcionalidades Implementadas

#### 1. Portada
- Muestra mensaje de bienvenida
- Menú de navegación completo
- Listado de las últimas 5 actividades desde la base de datos
- Cada actividad muestra su información básica y una imagen si está disponible

#### 2. Formulario de Actividades
- Validación en tiempo real con JavaScript en el lado del cliente
- Validación en el servidor con Flask
- Almacenamiento de múltiples imágenes
- Soporte para múltiples temas y métodos de contacto
- Manejo de errores con mensajes descriptivos
- Redirección a la portada tras agregar exitosamente

#### 3. Listado de Actividades
- Obtiene actividades desde la base de datos
- Implementa paginación mostrando 5 actividades por página
- Controles de navegación entre páginas
- Enlace a la vista detallada de cada actividad

#### 4. Vista Detallada de Actividad
- Muestra toda la información de la actividad seleccionada
- Visor de imágenes con diseño modal
- Muestra temas y métodos de contacto relacionados
- Información de ubicación (región y comuna)

#### 5. Sistema de Comentarios (Nuevo)
- Base de datos preparada para comentarios de actividades
- Estructura definida en `tabla-comentario.sql`

### Decisiones de Implementación

#### Base de Datos
- Se utiliza SQLAlchemy como ORM para interactuar con MySQL
- Modelos definidos para: Región, Comuna, Actividad, Foto, ContactarPor y ActividadTema
- Relaciones establecidas entre entidades para facilitar consultas
- Estructura preparada para sistema de comentarios

#### Estructura CSS
Se organizó el CSS en tres archivos principales:
- **base.css**: Estilos base, tipografía, colores y reset
- **components.css**: Componentes reutilizables como botones, navegación y tablas
- **layout.css**: Estructura, páginas específicas y estilos responsivos

#### Validación
- **Cliente**: Validación en tiempo real con JavaScript
- **Servidor**: Validación adicional en Flask antes de guardar en la base de datos
- Manejo de errores para evitar datos inconsistentes

#### Seguridad
- Sanitización de entradas para prevenir inyección SQL
- Nombres de archivo seguros para uploads
- Validación de tipos de archivo permitidos
- Límite de tamaño para archivos subidos

#### Control de Versiones
- Configuración de `.gitignore` para excluir:
  - Entorno virtual (`venv/`)
  - Archivos de caché de Python (`__pycache__/`)
  - Archivos subidos por usuarios (`uploads/`)
  - Archivos del sistema (`.DS_Store`)

## Configuración

### Requisitos
- Python 3.8+
- MySQL 5.7+
- Paquetes de Python: Flask, SQLAlchemy, PyMySQL

### Instrucciones de Instalación

#### 1. Preparación del Entorno
```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd desarrollo_web_paula_jorquera

# Crear un entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

#### 2. Configuración de la Base de Datos
```sql
-- Crear la base de datos
CREATE DATABASE tarea2;

-- Crear usuario
CREATE USER 'cc5002'@'localhost' IDENTIFIED BY 'programacionweb';

-- Otorgar permisos
GRANT ALL PRIVILEGES ON tarea2.* TO 'cc5002'@'localhost';
FLUSH PRIVILEGES;
```

#### 3. Inicialización
```bash
# Inicializar la base de datos
python db/init_db.py

# Ejecutar la aplicación
python app.py
```

#### Estructura de Archivos Ignorados
El archivo `.gitignore` está configurado para ignorar:
- `venv/` - Entorno virtual de Python
- `uploads/` - Archivos subidos por usuarios
- `__pycache__/` - Archivos de caché de Python
- `*.DS_Store` - Archivos del sistema macOS
- `db/__pycache__/` - Caché específico del módulo de base de datos

## Desarrollo

### Agregar Nuevas Funcionalidades
1. **Modelos de Base de Datos**: Definir en `db/db.py`
2. **Rutas y Controladores**: Implementar en `app.py`
3. **Plantillas**: Crear archivos HTML en `templates/`
4. **Estilos**: Añadir CSS en `static/css/`
5. **JavaScript**: Implementar en `static/js/`

### Mejores Prácticas
- Mantener la separación de responsabilidades
- Validar datos tanto en cliente como servidor
- Utilizar transacciones de base de datos para operaciones críticas
- Mantener el código documentado y comentado
- Seguir las convenciones de nomenclatura de Python (PEP 8)


## Notas Adicionales

- La carpeta `uploads/` está ignorada por Git para evitar subir archivos de usuario al repositorio
- El entorno virtual `venv/` también está ignorado para mantener el repositorio limpio
- Los archivos `__pycache__/` se ignoran automáticamente para evitar conflictos entre diferentes versiones de Python
