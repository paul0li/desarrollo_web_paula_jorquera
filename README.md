# Plataforma de Actividades - Desarrollo Web

Este proyecto es una plataforma web para gestionar y visualizar actividades relacionadas con gatos y cine, desarrollada para el curso de Desarrollo Web en la Universidad de Chile.

## Decisiones de Diseño

### 1. Estilo Bohemio
Se implementó un diseño con estética bohemia, caracterizado por:
- Paleta de colores cálidos y terrosos (#f5e6d3, #ddbea9, #b08968)
- Tipografía combinada: 'Amatic SC' para títulos y 'Crimson Text' para texto
- Elementos decorativos sutiles como bordes redondeados y sombras suaves
- Transiciones suaves para mejorar la interactividad

### 2. Visor de Imágenes
Se implementó un visor de imágenes con las siguientes características:
- Diseño modal con fondo semitransparente
- Vista ampliada de imágenes al hacer clic
- Controles intuitivos (botón de cierre, tecla Escape)
- Efecto hover en miniaturas para indicar interactividad

### 3. Estructura Modular
El código se organizó de manera modular:
- Componentes reutilizables (visor.html)
- Separación de estilos (styles.css)
- JavaScript modular (visor.js, validation.js)

### 4. Validación de Formularios
Se implementó validación de formularios con:
- Validación en tiempo real
- Mensajes de error claros y descriptivos
- Estilos visuales para estados de validación

## Consideraciones Técnicas

### Compatibilidad
- El proyecto utiliza JavaScript moderno
- Se recomienda usar navegadores actualizados (Chrome, Firefox, Safari)
- Las imágenes deben estar ubicadas en la carpeta img/

### Estructura de Archivos
```
.
├── components/
│   └── visor.html
├── js/
│   ├── select.js
│   ├── visor.js
│   └── validation.js
├── img/
├── styles.css
├── portada.html
├── listado.html
├── estadisticas.html
└── form.html
```

