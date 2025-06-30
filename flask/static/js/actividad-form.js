/**
 * Función para validar el formulario de actividades usando los validadores existentes
 * de validation.js
 */
const validarFormulario = () => {  
  // Obtener elementos del DOM usando el nombre del formulario
  let myForm = document.forms["actividadForm"];
  if (!myForm) {
    return { isValid: false, errores: ["Error interno: formulario no encontrado"] };
  }
  
  let email = myForm["email"] ? myForm["email"].value : null;
  let phoneNumber = myForm["celular"] ? myForm["celular"].value : null;
  let name = myForm["nombre"] ? myForm["nombre"].value : null;
  let allFileInputs = document.querySelectorAll('input[type="file"][name="foto[]"]');
  let files = [];
  
  allFileInputs.forEach(input => {
    if (input.files && input.files.length > 0) {
      files = files.concat(Array.from(input.files));
    }
  });
  
  let region = myForm["region"] ? myForm["region"].value : null;
  let comuna = myForm["comuna"] ? myForm["comuna"].value : null;
  let inicio = myForm["inicio"] ? myForm["inicio"].value : null;
  let termino = myForm["termino"] ? myForm["termino"].value : null;
  let temasSeleccionados = [];
  const temasCheckboxes = document.querySelectorAll('input[name="tema[]"]:checked');
  temasCheckboxes.forEach(checkbox => {
    temasSeleccionados.push(checkbox.value);
  });
  let temaOtro = myForm["temaOtro"] ? myForm["temaOtro"].value : "";

  let errores = [];
  
  if (!comuna) {
    errores.push("Debe seleccionar una comuna");
  }
  
  if (!validateName(name)) {
    errores.push("El nombre debe tener al menos 4 caracteres");
  }
  
  if (!validateEmail(email)) {
    errores.push("Debe ingresar un email válido");
  }
  
  if (!inicio) {
    errores.push("Debe ingresar una fecha y hora de inicio");
  }

  if (!termino) {
    errores.push("Debe ingresar una fecha y hora de término");
  } else if (new Date(termino) <= new Date(inicio)) {
    errores.push("La fecha y hora de término debe ser posterior a la fecha y hora de inicio");
  }
  
  if (temasSeleccionados.length === 0) {
    errores.push("Debe seleccionar al menos un tema");
  }
  
  if (temasSeleccionados.includes("otro") && !temaOtro) {
    errores.push("Debe especificar el tema 'otro'");
  }
  
  if (files.length === 0) {
    errores.push("Debe subir al menos una foto válida");
  } else {
    let todosValidos = true;
    
    for (let i = 0; i < files.length; i++) {
      if (!files[i].type.startsWith('image/')) {
        todosValidos = false;
      }
    }
    
    if (!todosValidos) {
      errores.push("Todos los archivos deben ser imágenes válidas");
    }
  }
  
  return {
    isValid: errores.length === 0,
    errores: errores
  };
};

/**
 * Función para manejar el envío del formulario
 */
const enviarFormulario = (event) => {
  
  // Prevenir el envío del formulario por defecto
  if (event) {
    event.preventDefault();
  }
  
  const formulario = document.getElementById("actividadForm");
  
  // Validar el formulario usando los validadores existentes
  const { isValid, errores } = validarFormulario();
  
  if (!isValid) {
    const mensajeError = "Por favor corrija los siguientes errores:\n- " + errores.join("\n- ");
    alert(mensajeError);
    resaltarCamposConError(errores);
    
    // Asegurarse de que el formulario siga visible
    const formulario = document.getElementById("actividadForm");
    if (formulario) {
      formulario.style.display = "block";
    }
    
    // Asegurarse de que la confirmación esté oculta
    const confirmacion = document.getElementById("confirmacion");
    if (confirmacion) {
      confirmacion.hidden = true;
    }
    
    return false;
  }
    
  // Si el formulario es válido, mostrar confirmación
  if (formulario) {
    formulario.style.display = "none";
  }
  
  const confirmacion = document.getElementById("confirmacion");
  if (confirmacion) {
    confirmacion.hidden = false;
  }
  
  return false; // Prevenir el envío del formulario
};

/**
 * Función para confirmar el envío del formulario
 */
const confirmarEnvio = () => {
  
  // Ocultar panel de confirmación
  const confirmacion = document.getElementById("confirmacion");
  if (confirmacion) {
    confirmacion.hidden = true;
  }
  
  // Obtener referencia al formulario
  const formulario = document.getElementById("actividadForm");
  if (!formulario) {
    return;
  }
  
  formulario.style.display = "block";
  
  window.formularioConfirmado = true;
  
  // Enviar el formulario
  try {
    formulario.submit();
  } catch (error) {
    console.error("ERROR al enviar el formulario:", error);
  }
  
  // Mostrar mensaje de agradecimiento
  const agradecimiento = document.getElementById("agradecimiento");
  if (agradecimiento) {
    agradecimiento.hidden = false;
  }
  
  // Ocultar el formulario
  formulario.style.display = "none";
};

/**
 * Función para cancelar el envío del formulario
 */
const cancelarEnvio = () => {
  document.getElementById("confirmacion").hidden = true;
  document.getElementById("actividadForm").style.display = "block";
};

/**
 * Función para resaltar visualmente los campos con errores
 */
const resaltarCamposConError = (errores) => {
  
  // Primero, eliminar todas las clases de error anteriores
  const campos = document.querySelectorAll(".campo-error");
  campos.forEach(campo => {
    campo.classList.remove("campo-error");
  });
  
  // Mapeo de mensajes de error a IDs de campos
  const mapeoErrores = {
    "Debe seleccionar una comuna": "comuna",
    "El nombre debe tener al menos 4 caracteres": "nombre",
    "Debe ingresar un email válido": "email",
    "Debe ingresar una fecha y hora de inicio": "inicio",
    "Debe seleccionar al menos un tema": "temasOptions",
    "Debe especificar el tema 'otro'": "temaOtro",
    "Debe subir al menos una foto válida": "foto[]"
  };
  
  // Resaltar los campos con errores
  errores.forEach(error => {
    let campoId = null;
    for (const [mensaje, id] of Object.entries(mapeoErrores)) {
      if (error.includes(mensaje)) {
        campoId = id;
        break;
      }
    }
    
    if (campoId) {
      const campo = document.getElementById(campoId) || document.getElementsByName(campoId)[0];
      if (campo) {
        campo.classList.add("campo-error");
        
        campo.addEventListener("input", function() {
          this.classList.remove("campo-error");
        }, { once: true });
      }
    }
  });
};

// Agregar event listeners cuando el DOM esté cargado
document.addEventListener("DOMContentLoaded", () => {
  
  // Agregar estilos CSS para los campos con error
  const style = document.createElement("style");
  style.textContent = `
    .campo-error {
      border: 2px solid red !important;
      background-color: #fff0f0 !important;
    }
  `;
  document.head.appendChild(style);
  
  // Inicializar selectores de región y comuna
  poblarRegiones();
  extraContact();
  
  // Configurar eventos para los selectores
  const agregarFotoBtn = document.getElementById("agregarFoto");
  if (agregarFotoBtn) {
    agregarFotoBtn.addEventListener("click", addPhoto);
  }
  
  const regionSelect = document.getElementById("region");
  if (regionSelect) {
    regionSelect.addEventListener("change", updateComunas);
  }
  
  const contactarSelect = document.getElementById("contactar");
  if (contactarSelect) {
    contactarSelect.addEventListener("change", extraContact);
  }
  
  // Prevenir el envío del formulario por defecto
  const formulario = document.getElementById("actividadForm");
  if (formulario) {
    formulario.addEventListener("submit", function(event) {
      // Solo prevenir el envío si no viene de la confirmación
      if (!window.formularioConfirmado) {
        event.preventDefault();
        enviarFormulario(event);
      }
    });
  }
  
  // Botón para enviar el formulario
  const submitBtn = document.getElementById("submit-btn");
  if (submitBtn) {
    submitBtn.addEventListener("click", function(event) {
      event.preventDefault();
      enviarFormulario(event);
    });
  }
  
  // Botón para confirmar el envío
  const confirmarSiBtn = document.getElementById("confirmar-si");
  if (confirmarSiBtn) {
    confirmarSiBtn.addEventListener("click", function() {
      window.formularioConfirmado = true;
      confirmarEnvio();
    });
  }
  
  // Botón para cancelar el envío
  const confirmarNoBtn = document.getElementById("confirmar-no");
  if (confirmarNoBtn) {
    confirmarNoBtn.addEventListener("click", cancelarEnvio);
  }
  
  // Botón para volver a la portada después del agradecimiento
  const volverBtn = document.getElementById("volverBtn");
  if (volverBtn) {
    volverBtn.addEventListener("click", () => {
      window.location.href = volverBtn.getAttribute("data-url") || "/";
    });
  }
});
