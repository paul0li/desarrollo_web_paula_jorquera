const validateName = (name) => {
  if(!name) return false;
  let lengthValid = name.trim().length >= 4;
  
  return lengthValid;
}

const validateEmail = (email) => {
  if (!email) return false;
  let lengthValid = email.length > 15;

  // validamos el formato
  let re = /^[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/;
  let formatValid = re.test(email);

  // devolvemos la lógica AND de las validaciones.
  return lengthValid && formatValid;
};

const validatePhoneNumber = (phoneNumber) => {
  if (!phoneNumber) return false;
  // validación de longitud
  let lengthValid = phoneNumber.length >= 8;

  // validación de formato
  let re = /^[0-9]+$/;
  let formatValid = re.test(phoneNumber);

  // devolvemos la lógica AND de las validaciones.
  return lengthValid && formatValid;
};

const validateFiles = (files) => {
  if (!files) return false;

  // validación del número de archivos
  let lengthValid = 1 <= files.length && files.length <= 5;

  // validación del tipo de archivo
  let typeValid = true;

  for (const file of files) {
    // el tipo de archivo debe ser "image/<foo>" o "application/pdf"
    let fileFamily = file.type.split("/")[0];
    typeValid &&= fileFamily == "image" || file.type == "application/pdf";
  }

  // devolvemos la lógica AND de las validaciones.
  return lengthValid && typeValid;
};

const validateSelect = (select) => {
  if(!select) return false;
  return true
}

const validateForm = () => {
  // obtener elementos del DOM usando el nombre del formulario.
  let myForm = document.forms["actividadForm"];
  let email = myForm["email"].value;
  let phoneNumber = myForm["celular"].value;
  let name = myForm["nombre"].value;
  let files = myForm["foto[]"].files;
  let region = myForm["region"].value;
  let comuna = myForm["comuna"].value;

  // variables auxiliares de validación y función.
  let invalidInputs = [];
  let isValid = true;
  const setInvalidInput = (inputName) => {
    invalidInputs.push(inputName);
    isValid &&= false;
  };

  // lógica de validación
  if (!validateName(name)) {
    setInvalidInput("Nombre");
  }
  if (!validateEmail(email)) {
    setInvalidInput("Email");
  }
  if (!validatePhoneNumber(phoneNumber)) {
    setInvalidInput("Número");
  }
  if (!validateFiles(files)) {
    setInvalidInput("Fotos");
  }
  if (!validateSelect(region)) {
    setInvalidInput("Región");
  }
  if (!validateSelect(comuna)) {
    setInvalidInput("Comuna");
  }

  // finalmente mostrar la validación
  let validationBox = document.getElementById("val-box");
  let validationMessageElem = document.getElementById("val-msg");
  let validationListElem = document.getElementById("val-list");
  let formContainer = document.querySelector(".main-container");

  if (!isValid) {
    validationListElem.textContent = "";
    // agregar elementos inválidos al elemento val-list.
    for (input of invalidInputs) {
      let listElement = document.createElement("li");
      listElement.innerText = input;
      validationListElem.append(listElement);
    }
    // establecer val-msg
    validationMessageElem.innerText = "Los siguientes campos son inválidos:";

    // aplicar estilos de error
    validationBox.style.backgroundColor = "#ffdddd";
    validationBox.style.borderLeftColor = "#f44336";

    // hacer visible el mensaje de validación
    validationBox.hidden = false;
  } else {
    // Ocultar el formulario
    myForm.style.display = "none";

    // establecer mensaje de éxito
    validationMessageElem.innerText = "¡Formulario válido! ¿Deseas enviarlo o volver?";
    validationListElem.textContent = "";

    // aplicar estilos de éxito
    validationBox.style.backgroundColor = "#ddffdd";
    validationBox.style.borderLeftColor = "#4CAF50";

    // Agregar botones para enviar el formulario o volver
    let submitButton = document.createElement("button");
    submitButton.innerText = "Enviar";
    submitButton.style.marginRight = "10px";
    submitButton.addEventListener("click", () => {
      // myForm.submit();
      // no tenemos un backend al cual enviarle los datos
    });

    let backButton = document.createElement("button");
    backButton.innerText = "Volver";
    backButton.addEventListener("click", () => {
      // Mostrar el formulario nuevamente
      myForm.style.display = "block";
      validationBox.hidden = true;
    });

    validationListElem.appendChild(submitButton);
    validationListElem.appendChild(backButton);

    // hacer visible el mensaje de validación
    validationBox.hidden = false;
  }
};


let submitBtn = document.getElementById("submit-btn");
submitBtn.addEventListener("click", (e) => {
  e.preventDefault(); // para evitar submit real
  
  // Validar el formulario antes de mostrar la confirmación
  let myForm = document.forms["actividadForm"];
  let isValid = true;
  let errorMessages = [];
  
  // Validaciones básicas - acumular mensajes de error
  if (!myForm["comuna"].value) {
    isValid = false;
    errorMessages.push("Debe seleccionar una comuna");
  }
  if (!myForm["nombre"].value) {
    isValid = false;
    errorMessages.push("Debe ingresar un nombre");
  }
  if (!myForm["email"].value) {
    isValid = false;
    errorMessages.push("Debe ingresar un email");
  }
  if (!myForm["inicio"].value) {
    isValid = false;
    errorMessages.push("Debe ingresar una fecha y hora de inicio");
  }
  if (!myForm["tema"].value) {
    isValid = false;
    errorMessages.push("Debe seleccionar un tema");
  }
  
  // Validar que la fecha de término sea posterior a la fecha de inicio, si es que la fecha de termino existe
  const fechaInicio = new Date(myForm["inicio"].value);
  const fechaTermino = new Date(myForm["termino"].value);
  
  if (fechaTermino <= fechaInicio && fechaTermino) {
    isValid = false;
    errorMessages.push("La fecha y hora de término debe ser posterior a la fecha y hora de inicio");
  }
  
  // Mostrar todos los errores en un solo alert si hay alguno
  if (!isValid && errorMessages.length > 0) {
    alert("Por favor corrija los siguientes errores:\n- " + errorMessages.join("\n- "));
    return; // Salir de la función sin mostrar la confirmación
  }
  
  // Si el formulario es válido, mostrar confirmación
  if (isValid) {
    document.getElementById("actividadForm").style.display = "none";
    document.getElementById("confirmacion").hidden = false;
  }
});


document.getElementById("confirmar-si").addEventListener("click", () => {
  document.getElementById("confirmacion").hidden = true;
  // Submit the form to the server
  document.getElementById("actividadForm").submit();
  // Show thank you message
  document.getElementById("agradecimiento").hidden = false;
});

document.getElementById("confirmar-no").addEventListener("click", () => {
  document.getElementById("confirmacion").hidden = true;
  document.getElementById("actividadForm").style.display = "block";
});
