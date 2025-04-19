document.addEventListener('DOMContentLoaded', () => {
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            document.getElementById('visor').style.display = 'none';
        }
    });
});

// Función para mostrar una foto en el visor
function mostrarFoto(src) {
    const imgGrande = document.getElementById('imgGrande');
    const visor = document.getElementById('visor');
    
    if (imgGrande && visor) {
        imgGrande.src = src;
        visor.style.display = 'flex';
    }
}

// Hacer la función disponible globalmente
window.mostrarFoto = mostrarFoto;

