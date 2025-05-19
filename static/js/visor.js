// Variables globales para el visor
let fotosActividad = [];
let indiceActual = 0;

document.addEventListener('DOMContentLoaded', () => {
    // Cerrar el visor con la tecla Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            document.getElementById('visor').style.display = 'none';
        } else if (e.key === 'ArrowLeft') {
            navegarFoto(-1);
        } else if (e.key === 'ArrowRight') {
            navegarFoto(1);
        }
    });
    
    // Configurar los botones de navegación
    const prevBtn = document.getElementById('prevFoto');
    const nextBtn = document.getElementById('nextFoto');
    
    if (prevBtn) {
        prevBtn.addEventListener('click', () => navegarFoto(-1));
    }
    
    if (nextBtn) {
        nextBtn.addEventListener('click', () => navegarFoto(1));
    }
});

// Función para mostrar una foto en el visor con todas las fotos de la actividad
function mostrarFoto(src, actividadId, fotoIndex = 0) {
    const imgGrande = document.getElementById('imgGrande');
    const visor = document.getElementById('visor');
    const fotoIndicador = document.getElementById('fotoIndicador');
    
    if (imgGrande && visor) {
        // Si se proporciona un ID de actividad, cargar todas las fotos
        if (actividadId) {
            // Obtener todas las fotos de esta actividad desde el atributo data
            const contenedorFotos = document.querySelector(`[data-actividad-id="${actividadId}"]`);
            if (contenedorFotos) {
                fotosActividad = JSON.parse(contenedorFotos.getAttribute('data-fotos'));
                indiceActual = fotoIndex;
            } else {
                // Si no hay contenedor de fotos, usar solo la foto actual
                fotosActividad = [src];
                indiceActual = 0;
            }
        } else {
            // Si no hay ID de actividad, mostrar solo la foto actual
            fotosActividad = [src];
            indiceActual = 0;
        }
        
        // Mostrar la foto actual
        actualizarVisor();
        
        // Mostrar el visor
        visor.style.display = 'flex';
    }
}

// Función para navegar entre fotos
function navegarFoto(direccion) {
    if (fotosActividad.length <= 1) return;
    
    indiceActual = (indiceActual + direccion + fotosActividad.length) % fotosActividad.length;
    actualizarVisor();
}

// Función para actualizar el visor con la foto actual
function actualizarVisor() {
    const imgGrande = document.getElementById('imgGrande');
    const fotoIndicador = document.getElementById('fotoIndicador');
    const prevBtn = document.getElementById('prevFoto');
    const nextBtn = document.getElementById('nextFoto');
    
    if (imgGrande) {
        imgGrande.src = fotosActividad[indiceActual];
    }
    
    if (fotoIndicador) {
        fotoIndicador.textContent = `${indiceActual + 1} de ${fotosActividad.length}`;
    }
    
    // Habilitar/deshabilitar botones de navegación
    if (prevBtn) {
        prevBtn.disabled = fotosActividad.length <= 1;
    }
    
    if (nextBtn) {
        nextBtn.disabled = fotosActividad.length <= 1;
    }
}

// Hacer las funciones disponibles globalmente
window.mostrarFoto = mostrarFoto;
window.navegarFoto = navegarFoto;
