/**
 * Función para validar el formulario de actividades usando los validadores existentes
 * de validation.js
 */
const validarFormulario = () => {
  console.log("========== INICIO DE VALIDACIÓN DE FORMULARIO ==========");
  
  // Obtener elementos del DOM usando el nombre del formulario
  let myForm = document.forms["actividadForm"];
  if (!myForm) {
    console.error("ERROR: No se encontró el formulario 'actividadForm'");
    return { isValid: false, errores: ["Error interno: formulario no encontrado"] };
  }
  
  console.log("Formulario encontrado:", myForm.id, "| Action:", myForm.action, "| Method:", myForm.method);
  
  // Obtener valores de los campos
  let email = myForm["email"] ? myForm["email"].value : null;
  let phoneNumber = myForm["celular"] ? myForm["celular"].value : null;
  let name = myForm["nombre"] ? myForm["nombre"].value : null;
  // Obtener todos los campos de archivo (pueden ser múltiples con el mismo nombre)
  let allFileInputs = document.querySelectorAll('input[type="file"][name="foto[]"]');
  let files = [];
  
  // Recopilar todos los archivos de todos los campos
  allFileInputs.forEach(input => {
    if (input.files && input.files.length > 0) {
      // Convertir FileList a Array y concatenar
      files = files.concat(Array.from(input.files));
    }
  });
  
  console.log("Campos de archivo encontrados:", allFileInputs.length);
  console.log("Total de archivos recopilados:", files.length);
  let region = myForm["region"] ? myForm["region"].value : null;
  let comuna = myForm["comuna"] ? myForm["comuna"].value : null;
  let inicio = myForm["inicio"] ? myForm["inicio"].value : null;
  let termino = myForm["termino"] ? myForm["termino"].value : null;
  // Obtener los temas seleccionados (ahora son checkboxes)
  let temasSeleccionados = [];
  const temasCheckboxes = document.querySelectorAll('input[name="tema[]"]:checked');
  temasCheckboxes.forEach(checkbox => {
    temasSeleccionados.push(checkbox.value);
  });
  let temaOtro = myForm["temaOtro"] ? myForm["temaOtro"].value : "";

  console.log("Valores del formulario:");
  console.log("- Email:", email);
  console.log("- Teléfono:", phoneNumber);
  console.log("- Nombre:", name);
  console.log("- Archivos:", files ? `${files.length} archivos` : "ninguno");
  console.log("- Región:", region);
  console.log("- Comuna:", comuna);
  console.log("- Inicio:", inicio);
  console.log("- Término:", termino);
  console.log("- Temas seleccionados:", temasSeleccionados);
  console.log("- Tema Otro:", temaOtro);

  // Variables auxiliares de validación
  let errores = [];
  
  console.log("\nIniciando validaciones...");
  
  // Validar campos obligatorios
  if (!comuna) {
    errores.push("Debe seleccionar una comuna");
    console.log("ERROR: Comuna no seleccionada");
  }
  
  console.log("Validando nombre...");
  if (!validateName(name)) {
    errores.push("El nombre debe tener al menos 4 caracteres");
    console.log(`ERROR: Nombre inválido: "${name}"`); 
  } else {
    console.log("Nombre válido");
  }
  
  console.log("Validando email...");
  if (!validateEmail(email)) {
    errores.push("Debe ingresar un email válido");
    console.log(`ERROR: Email inválido: "${email}"`); 
  } else {
    console.log("Email válido");
  }
  
  if (!inicio) {
    errores.push("Debe ingresar una fecha y hora de inicio");
    console.log("ERROR: Fecha de inicio no proporcionada");
  }

  console.log("Validando fecha de término sea mayor que la de inicio...");
  if (!termino) {
    errores.push("Debe ingresar una fecha y hora de término");
    console.log("ERROR: Fecha de término no proporcionada");
  } else if (new Date(termino) <= new Date(inicio)) {
    errores.push("La fecha y hora de término debe ser posterior a la fecha y hora de inicio");
    console.log("ERROR: Fecha y hora de término no es posterior a la de inicio");
  }
  
  if (temasSeleccionados.length === 0) {
    errores.push("Debe seleccionar al menos un tema");
    console.log("ERROR: Ningún tema seleccionado"); 
  }
  
  if (temasSeleccionados.includes("otro") && !temaOtro) {
    errores.push("Debe especificar el tema 'otro'");
    console.log("ERROR: Tema 'otro' sin especificar"); 
  }
  
  console.log("Validando archivos...");
  // Verificar directamente si hay archivos en el array
  if (files.length === 0) {
    errores.push("Debe subir al menos una foto válida");
    console.log("ERROR: No se proporcionaron archivos");
  } else {
    // Verificar que todos los archivos sean válidos
    let todosValidos = true;
    
    console.log(`- Cantidad de archivos: ${files.length}`);
    for (let i = 0; i < files.length; i++) {
      console.log(`- Archivo ${i+1}: ${files[i].name} (${files[i].type})`);
      
      // Verificar que sea una imagen
      if (!files[i].type.startsWith('image/')) {
        todosValidos = false;
        console.log(`  ERROR: El archivo ${i+1} no es una imagen`);
      }
    }
    
    if (!todosValidos) {
      errores.push("Todos los archivos deben ser imágenes válidas");
      console.log("ERROR: Algunos archivos no son imágenes válidas");
    } else {
      console.log("Todos los archivos son válidos");
    }
  }
  
  console.log("\nResultado de la validación:", errores.length === 0 ? "VÁLIDO" : "INVÁLIDO");
  if (errores.length > 0) {
    console.log("Errores encontrados:", errores);
  }
  
  console.log("========== FIN DE VALIDACIÓN DE FORMULARIO ==========\n");
  
  return {
    isValid: errores.length === 0,
    errores: errores
  };
};

/**
 * Función para manejar el envío del formulario
 */
const enviarFormulario = (event) => {
  console.log("========== INICIO DE ENVÍO DE FORMULARIO ==========");
  console.log("Evento recibido:", event ? event.type : "ninguno");
  
  // Prevenir el envío del formulario por defecto
  if (event) {
    event.preventDefault();
    console.log("Prevención del envío por defecto activada");
  }
  
  // Obtener referencia al formulario
  const formulario = document.getElementById("actividadForm");
  console.log("Formulario:", formulario ? formulario.id : "no encontrado");
  console.log("Action:", formulario ? formulario.action : "N/A");
  console.log("Method:", formulario ? formulario.method : "N/A");
  console.log("Enctype:", formulario ? formulario.enctype : "N/A");
  
  // Validar el formulario usando los validadores existentes
  console.log("Iniciando validación del formulario...");
  const { isValid, errores } = validarFormulario();
  
  if (!isValid) {
    // Mostrar errores en un formato más amigable
    const mensajeError = "Por favor corrija los siguientes errores:\n- " + errores.join("\n- ");
    console.log("Mostrando alerta con errores:", mensajeError);
    
    // Mostrar alerta con los errores
    alert(mensajeError);
    
    // Resaltar visualmente los campos con errores
    resaltarCamposConError(errores);
    
    console.log("Formulario inválido, deteniendo envío");
    console.log("========== FIN DE ENVÍO DE FORMULARIO (CANCELADO) ==========\n");
    
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
  
  console.log("Formulario válido, mostrando confirmación");
  
  // Si el formulario es válido, mostrar confirmación
  if (formulario) {
    console.log("Ocultando formulario y mostrando confirmación");
    formulario.style.display = "none";
  } else {
    console.error("ERROR: No se encontró el formulario para ocultar");
  }
  
  const confirmacion = document.getElementById("confirmacion");
  if (confirmacion) {
    confirmacion.hidden = false;
    console.log("Panel de confirmación mostrado correctamente");
  } else {
    console.error("ERROR: No se encontró el panel de confirmación");
  }
  
  console.log("========== FIN DE ENVÍO DE FORMULARIO (PENDIENTE CONFIRMACIÓN) ==========\n");
  return false; // Prevenir el envío del formulario
};

/**
 * Función para confirmar el envío del formulario
 */
const confirmarEnvio = () => {
  console.log("========== INICIO DE CONFIRMACIÓN DE ENVÍO ==========");
  console.log("Confirmando envío del formulario...");
  
  // Ocultar panel de confirmación
  const confirmacion = document.getElementById("confirmacion");
  if (confirmacion) {
    confirmacion.hidden = true;
    console.log("Panel de confirmación ocultado");
  } else {
    console.error("ERROR: No se encontró el panel de confirmación para ocultar");
  }
  
  // Obtener referencia al formulario
  const formulario = document.getElementById("actividadForm");
  if (!formulario) {
    console.error("ERROR: No se encontró el formulario para enviar");
    return;
  }
  
  console.log("Información del formulario:");
  console.log("- ID:", formulario.id);
  console.log("- Action:", formulario.action);
  console.log("- Method:", formulario.method);
  console.log("- Enctype:", formulario.enctype);
  
  // Verificar los datos del formulario antes de enviar
  console.log("\nVerificando datos del formulario antes de enviar:");
  const formData = new FormData(formulario);
  for (const [key, value] of formData.entries()) {
    if (key !== "foto[]") {
      console.log(`- ${key}: ${value}`);
    } else {
      console.log(`- ${key}: ${value.name} (${value.type})`);
    }
  }
  
  // Asegurarse de que el formulario se envíe correctamente
  console.log("\nPreparando formulario para envío...");
  formulario.style.display = "block";
  
  // Establecer una bandera para indicar que el formulario ha sido confirmado
  console.log("Estableciendo bandera de confirmación");
  window.formularioConfirmado = true;
  
  // Enviar el formulario
  console.log("ENVIANDO FORMULARIO AL SERVIDOR...");
  try {
    formulario.submit();
    console.log("Formulario enviado correctamente");
  } catch (error) {
    console.error("ERROR al enviar el formulario:", error);
  }
  
  // Mostrar mensaje de agradecimiento
  console.log("Mostrando mensaje de agradecimiento");
  const agradecimiento = document.getElementById("agradecimiento");
  if (agradecimiento) {
    agradecimiento.hidden = false;
    console.log("Mensaje de agradecimiento mostrado correctamente");
  } else {
    console.error("ERROR: No se encontró el panel de agradecimiento");
  }
  
  // Ocultar el formulario
  formulario.style.display = "none";
  console.log("Formulario ocultado después del envío");
  
  console.log("========== FIN DE CONFIRMACIÓN DE ENVÍO ==========\n");
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
  console.log("Resaltando campos con errores...");
  
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
    // Buscar el ID del campo correspondiente al error
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
        console.log(`Resaltando campo: ${campoId}`);
        campo.classList.add("campo-error");
        
        // Agregar un evento para quitar la clase de error cuando el usuario modifique el campo
        campo.addEventListener("input", function() {
          this.classList.remove("campo-error");
        }, { once: true });
      }
    }
  });
};

// Agregar event listeners cuando el DOM esté cargado
document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM cargado, configurando event listeners...");
  
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
    console.log("Formulario encontrado, configurando evento submit");
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
    console.log("Botón de envío encontrado, configurando evento click");
    submitBtn.addEventListener("click", function(event) {
      event.preventDefault();
      enviarFormulario(event);
    });
  }
  
  // Botón para confirmar el envío
  const confirmarSiBtn = document.getElementById("confirmar-si");
  if (confirmarSiBtn) {
    console.log("Botón de confirmación encontrado, configurando evento click");
    confirmarSiBtn.addEventListener("click", function() {
      window.formularioConfirmado = true;
      confirmarEnvio();
    });
  }
  
  // Botón para cancelar el envío
  const confirmarNoBtn = document.getElementById("confirmar-no");
  if (confirmarNoBtn) {
    console.log("Botón de cancelación encontrado, configurando evento click");
    confirmarNoBtn.addEventListener("click", cancelarEnvio);
  }
  
  // Botón para volver a la portada después del agradecimiento
  const volverBtn = document.getElementById("volverBtn");
  if (volverBtn) {
    console.log("Botón de volver encontrado, configurando evento click");
    volverBtn.addEventListener("click", () => {
      window.location.href = volverBtn.getAttribute("data-url") || "/";
    });
  }
});
