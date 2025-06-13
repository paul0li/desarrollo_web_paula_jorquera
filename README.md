# Plataforma de Actividades - Desarrollo Web TAREA 2

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
│   └── uploads/            # Carpeta para archivos subidos
└── templates/              # Plantillas Jinja2
    ├── base.html           # Plantilla base con estructura común
    ├── portada.html        # Página de inicio
    ├── form.html           # Formulario para agregar actividades
    ├── listado.html        # Listado de actividades con paginación
    ├── actividad.html      # Detalle de una actividad
    └── estadisticas.html   # Página de estadísticas (pendiente)
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

### Decisiones de Implementación

#### Base de Datos
- Se utiliza SQLAlchemy como ORM para interactuar con MySQL
- Modelos definidos para: Región, Comuna, Actividad, Foto, ContactarPor y ActividadTema
- Relaciones establecidas entre entidades para facilitar consultas

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

## Configuración

### Requisitos
- Python 3.8+
- MySQL 5.7+
- Paquetes de Python: Flask, SQLAlchemy, PyMySQL

### Instrucciones de Instalación
1. Clonar el repositorio
2. Crear un entorno virtual: `python -m venv venv`
3. Activar el entorno: `source venv/bin/activate` (Linux/Mac) o `venv\Scripts\activate` (Windows)
4. Instalar dependencias: `pip install -r requirements.txt`
5. Configurar la base de datos MySQL:
   - Crear la base de datos: `CREATE DATABASE tarea2;`
   - Crear usuario: `CREATE USER 'cc5002'@'localhost' IDENTIFIED BY 'programacionweb';`
   - Otorgar permisos: `GRANT ALL PRIVILEGES ON tarea2.* TO 'cc5002'@'localhost';`
6. Inicializar la base de datos: `python db/init_db.py`
7. Ejecutar la aplicación: `python app.py`

## Notas Adicionales

- Notar que la carpeta uploads esta ignorada. 