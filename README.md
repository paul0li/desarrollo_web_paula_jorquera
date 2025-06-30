# Plataforma de Actividades - Desarrollo Web TAREA 4

Este proyecto es una plataforma web para gestionar y visualizar actividades, desarrollada para el curso de Desarrollo Web en la Universidad de Chile. La aplicación permite registrar actividades, ver su listado, visualizar detalles, mostrar estadísticas y **evaluar actividades finalizadas** mediante una arquitectura de microservicios.

## Arquitectura de Microservicios

### Tecnologías Utilizadas
- **Frontend & Backend Principal**: Python con Flask (Puerto 5000)
- **Microservicio de Evaluaciones**: Java con Spring Boot (Puerto 8080)
- **Base de Datos**: MySQL compartida entre ambos servicios
- **ORM**: SQLAlchemy (Flask) y JPA/Hibernate (Spring Boot)
- **Frontend**: HTML5, CSS3, JavaScript con llamadas asíncronas (fetch API)
- **Plantillas**: Jinja2

### Descripción de la Arquitectura

```
┌─────────────────┐    HTTP/REST    ┌──────────────────┐
│   Flask App     │ ◄──────────────► │   Spring Boot    │
│   Puerto 5000   │                 │   Puerto 8080    │
│                 │                 │                  │
│ • Frontend      │                 │ • API Evaluaciones│
│ • Gestión Activ.│                 │ • Notas/Promedios │
│ • Estadísticas  │                 │ • Validaciones    │
│ • Listados      │                 │                  │
└─────────┬───────┘                 └────────┬─────────┘
          │                                  │
          │                                  │
          └──────────► MySQL ◄───────────────┘
                    Puerto 3306
```

### Funcionalidades por Servicio

#### Flask Service (Puerto 5000)
- 🏠 **Portada** con últimas actividades
- ➕ **Formulario** para agregar nuevas actividades
- 📋 **Listado** de actividades con paginación
- 👁️ **Vista detallada** de actividades
- 📊 **Estadísticas** con gráficos dinámicos
- 🏆 **Interfaz de evaluaciones** (frontend)
- 💬 **Sistema de comentarios**

#### Spring Boot Service (Puerto 8080)
- 📝 **API REST** para gestión de evaluaciones
- ⭐ **Sistema de notas** (escala 1-7)
- 📈 **Cálculo de promedios** en tiempo real
- ✅ **Validaciones** de negocio
- 🔄 **Operaciones asíncronas**

### Estructura del Proyecto

```
.
├── flask/                           # Servicio Flask
│   ├── app.py                       # Aplicación principal Flask
│   ├── requirements.txt             # Dependencias Python
│   ├── db/                          # Módulos de base de datos
│   │   ├── db.py                    # Modelos SQLAlchemy y funciones
│   │   ├── init_db.py               # Inicialización de BD
│   │   ├── tarea2.sql               # Estructura base de datos
│   │   ├── region-comuna.sql        # Datos de regiones y comunas
│   │   └── create_user.sql          # Usuario de BD
│   ├── static/                      # Archivos estáticos
│   │   ├── css/                     # Hojas de estilo
│   │   │   ├── base.css             # Estilos base
│   │   │   ├── components.css       # Componentes reutilizables
│   │   │   ├── layout.css           # Estructura y responsividad
│   │   │   ├── evaluaciones.css     # Estilos específicos evaluaciones
│   │   │   └── main.css             # Importa otros CSS
│   │   ├── js/                      # JavaScript
│   │   │   ├── validation.js        # Validación formularios
│   │   │   └── visor.js             # Visor de imágenes
│   │   ├── img/                     # Imágenes del sitio
│   │   └── uploads/                 # Archivos subidos usuarios
│   ├── templates/                   # Plantillas Jinja2
│   │   ├── base.html                # Plantilla base
│   │   ├── portada.html             # Página inicio
│   │   ├── form.html                # Formulario actividades
│   │   ├── listado.html             # Listado actividades
│   │   ├── actividad.html           # Detalle actividad
│   │   ├── estadisticas.html        # Estadísticas con gráficos
│   │   └── evaluaciones_flask.html  # Interfaz evaluaciones
│   ├── components/                  # Componentes reutilizables
│   ├── utils/                       # Utilidades Flask
│   └── venv/                        # Entorno virtual Python
├── springboot/                      # Servicio Spring Boot
│   ├── src/main/java/com/example/demo/
│   │   ├── DemoApplication.java     # Aplicación principal Spring
│   │   ├── controller/              # Controladores REST
│   │   │   └── EvaluacionController.java
│   │   ├── service/                 # Lógica de negocio
│   │   │   └── EvaluacionService.java
│   │   ├── repository/              # Repositorios JPA
│   │   │   ├── ActividadRepository.java
│   │   │   ├── NotaRepository.java
│   │   │   ├── ComunaRepository.java
│   │   │   └── ActividadTemaRepository.java
│   │   └── entity/                  # Entidades JPA
│   │       ├── Actividad.java
│   │       ├── Nota.java
│       ├── Comuna.java
│   │       └── ActividadTema.java
│   ├── src/main/resources/
│   │   └── application.properties   # Configuración Spring Boot
│   ├── pom.xml                      # Dependencias Maven
│   └── mvnw, mvnw.cmd              # Maven Wrapper
├── tabla-nota.sql                   # Script tabla evaluaciones
└── README.md                        # Este archivo
```

## Funcionalidades Implementadas

### 1. Portada
- Muestra mensaje de bienvenida con tema de gatitos 🐱
- Menú de navegación responsivo
- Listado de las últimas 5 actividades desde BD
- Cada actividad muestra información básica e imágenes

### 2. Gestión de Actividades
- **Formulario**: Validación cliente/servidor, múltiples imágenes, temas y contactos
- **Listado**: Paginación, filtros, enlace a vista detallada
- **Detalle**: Información completa, visor de imágenes modal, sistema de comentarios

### 3. Estadísticas Dinámicas
- **Gráfico de líneas**: Actividades por día
- **Gráfico de torta**: Distribución por tipo de actividad (datos reales de BD)
- **Gráfico de barras**: Actividades por horario y mes
- Powered by Highcharts con datos desde API

### 4. Sistema de Evaluaciones (NUEVO) ⭐
- **Interfaz en Flask**: Tabla de actividades finalizadas
- **API en Spring Boot**: Gestión completa de evaluaciones
- **Evaluación asíncrona**: Modal con escala 1-7, JavaScript fetch
- **Promedio en tiempo real**: Actualización sin recarga de página
- **Validaciones**: Cliente y servidor para integridad de datos

### 5. Sistema de Comentarios
- Comentarios por actividad con validación
- Interfaz AJAX para experiencia fluida

## Configuración e Instalación

### Requisitos
- Python 3.8+
- Java 17+
- Maven 3.6+
- MySQL 8.0+

### 1. Configuración de Base de Datos

```sql
-- Crear la base de datos
CREATE DATABASE tarea2;

-- Crear usuario
CREATE USER 'cc5002'@'localhost' IDENTIFIED BY 'programacionweb';

-- Otorgar permisos
GRANT ALL PRIVILEGES ON tarea2.* TO 'cc5002'@'localhost';
FLUSH PRIVILEGES;
```

```bash
# Ejecutar scripts de BD
mysql -u cc5002 -p tarea2 < flask/db/tarea2.sql
mysql -u cc5002 -p tarea2 < flask/db/region-comuna.sql
mysql -u cc5002 -p tarea2 < tabla-nota.sql
```

### 2. Configuración Flask Service

```bash
cd flask/

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Inicializar BD (si es necesario)
python db/init_db.py

# Ejecutar Flask (Puerto 5000)
python app.py
```

### 3. Configuración Spring Boot Service

```bash
cd springboot/

# Compilar y ejecutar (Puerto 8080)
./mvnw spring-boot:run

# O usando Maven directamente
mvn spring-boot:run
```

### 4. Verificación de Servicios

```bash
# Verificar Flask
curl http://127.0.0.1:5000/

# Verificar Spring Boot
curl http://127.0.0.1:8080/api/actividades/1/promedio
```

## API Endpoints

### Flask Service (Puerto 5000)
- `GET /` - Portada
- `GET /form` - Formulario actividades
- `POST /agregar-actividad` - Agregar actividad
- `GET /listado` - Listado paginado
- `GET /actividad/<id>` - Detalle actividad
- `GET /estadisticas` - Página estadísticas
- `GET /evaluaciones` - Interfaz evaluaciones
- `GET /api/estadisticas/*` - APIs para gráficos

### Spring Boot Service (Puerto 8080)
- `POST /api/actividades/{id}/nota` - Agregar evaluación
- `GET /api/actividades/{id}/promedio` - Obtener promedio
- Configurado con CORS para comunicación cross-origin

## Comunicación Entre Servicios

### Patrón de Arquitectura
1. **Frontend en Flask** presenta la interfaz de evaluaciones
2. **JavaScript** realiza llamadas asíncronas a Spring Boot
3. **Spring Boot** procesa evaluaciones y calcula promedios
4. **Respuesta JSON** actualiza interfaz sin recargar página

### Ejemplo de Comunicación Asíncrona

```javascript
// Frontend (Flask) llama a Spring Boot
const response = await fetch(`http://localhost:8080/api/actividades/${id}/nota`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nota: 7 })
});

const data = await response.json();
// Actualiza promedio en tiempo real
document.getElementById(`promedio-${id}`).textContent = data.nuevoPromedio;
```

## Características Técnicas

### Seguridad
- Sanitización de entradas SQL injection
- Validación dual (cliente/servidor)
- CORS configurado para comunicación segura
- Manejo de errores robusto

### Performance
- Paginación eficiente en listados
- Llamadas asíncronas para evaluaciones
- Optimización de consultas SQL
- CSS y JS organizados y minificados

### Escalabilidad
- Arquitectura de microservicios
- Servicios independientes y deployables
- Base de datos compartida con conexiones optimizadas
- API RESTful stateless

## Desarrollo y Extensión

### Agregar Nueva Funcionalidad
1. **Decidir servicio**: ¿Flask (frontend/gestión) o Spring Boot (evaluaciones)?
2. **Flask**: Modelos en `db/db.py`, rutas en `app.py`, templates en `templates/`
3. **Spring Boot**: Entidades, repositorios, servicios, controladores
4. **Frontend**: HTML/CSS/JS con llamadas asíncronas entre servicios

### Mejores Prácticas
- Mantener separación clara de responsabilidades entre servicios
- Usar transacciones de BD para operaciones críticas
- Validar datos en ambos extremos de la comunicación
- Documentar APIs con ejemplos de uso
- Manejo de errores consistente entre servicios

## Notas de Deployment

### Desarrollo
```bash
# Terminal 1: Flask
cd flask && python app.py

# Terminal 2: Spring Boot  
cd springboot && ./mvnw spring-boot:run
```

### Producción
- Flask: WSGI server (Gunicorn, uWSGI)
- Spring Boot: JAR ejecutable o containerización
- MySQL: Configuración de producción con pools de conexiones
- Reverse proxy (Nginx) para routing entre servicios

## Control de Versiones

### Archivos Ignorados
- `flask/venv/` - Entorno virtual Python
- `flask/uploads/` - Archivos subidos usuarios
- `*/__pycache__/` - Cache Python  
- `springboot/target/` - Compilados Maven
- `*.DS_Store` - Archivos sistema macOS

El proyecto sigue las mejores prácticas de desarrollo con arquitectura de microservicios, proporcionando una plataforma robusta y escalable para la gestión de actividades con capacidades avanzadas de evaluación.
