const region_comuna = {
  "Región de Tarapacá": ["Camiña","Huara","Pozo Almonte","Iquique","Pica","Colchane","Alto Hospicio"],

  "Región de Antofagasta": ["Tocopilla","Maria Elena","Ollague","Calama","San Pedro Atacama","Sierra Gorda","Mejillones","Antofagasta","Taltal"],

  "Región de Atacama": ["Diego de Almagro","Chañaral","Caldera","Copiapo","Tierra Amarilla","Huasco","Freirina","Vallenar","Alto del Carmen"],

  "Región de Coquimbo ": ["La Higuera","La Serena","Vicuña","Paihuano","Coquimbo","Andacollo","Rio Hurtado","Ovalle","Monte Patria","Punitaqui","Combarbala","Mincha","Illapel","Salamanca",
"Los Vilos"],

  "Región de Valparaíso": ["Petorca","Cabildo","Papudo","La Ligua","Zapallar","Putaendo","Santa Maria","San Felipe","Pencahue","Catemu","Llay Llay","Nogales","La Calera","Hijuelas","La Cruz",
"Quillota","Olmue","Limache","Los Andes","Rinconada","Calle Larga","San Esteban","Puchuncavi","Quintero","Viña del Mar","Villa Alemana","Quilpue","Valparaiso","Juan Fernandez","Casablanca",
"Concon","Isla de Pascua","Algarrobo","El Quisco","El Tabo","Cartagena","San Antonio","Santo Domingo"],

  "Región del Libertador Bernardo O'Higgins": ["Mostazal","Codegua","Graneros","Machali","Rancagua","Olivar","Doñihue","Requinoa","Coinco","Coltauco","Quinta Tilcoco","Las Cabras","Rengo",
"Peumo","Pichidegua","Malloa","San Vicente","Navidad","La Estrella","Marchigue","Pichilemu","Litueche","Paredones","San Fernando","Peralillo","Placilla","Chimbarongo","Palmilla","Nancagua",
"Santa Cruz","Pumanque","Chepica","Lolol"],

  "Región del Maule": ["Teno","Romeral","Rauco","Curico","Sagrada Familia","Hualañe","Vichuquen","Molina","Licanten","Rio Claro","Curepto","Pelarco","Talca","Pencahue","San Clemente",
"Constitucion","Maule","Empedrado","San Rafael","San Javier","Colbun","Villa Alegre","Yerbas Buenas","Linares","Longavi","Retiro","Parral","Chanco","Pelluhue","Cauquenes"],

  "Región del Biobío": ["Tome","Florida","Penco","Talcahuano","Concepcion","Hualqui","Coronel","Lota","Santa Juana","Chiguayante","San Pedro de la Paz","Hualpen","Cabrero","Yumbel","Tucapel",
"Antuco","San Rosendo","Laja","Quilleco","Los Angeles","Nacimiento","Negrete","Santa Barbara","Quilaco","Mulchen","Alto Bio Bio","Arauco","Curanilahue","Los Alamos","Lebu","Cañete","Contulmo",
"Tirua"],

  "Región de La Araucanía": ["Renaico","Angol","Collipulli","Los Sauces","Puren","Ercilla","Lumaco","Victoria","Traiguen","Curacautin","Lonquimay","Perquenco","Galvarino","Lautaro","Vilcun",
"Temuco","Carahue","Melipeuco","Nueva Imperial","Puerto Saavedra","Cunco","Freire","Pitrufquen","Teodoro Schmidt","Gorbea","Pucon","Villarrica","Tolten","Curarrehue","Loncoche","Padre Las Casas",
"Cholchol"],

  "Región de Los Lagos": ["San Pablo","San Juan","Osorno","Puyehue","Rio Negro","Purranque","Puerto Octay","Frutillar","Fresia","Llanquihue","Puerto Varas","Los Muermos","Puerto Montt",
"Maullin","Calbuco","Cochamo","Ancud","Quemchi","Dalcahue","Curaco de Velez","Castro","Chonchi","Queilen","Quellon","Quinchao","Puqueldon","Chaiten","Futaleufu","Palena","Hualaihue"],

  "Región Aisén del General Carlos Ibáñez del Campo": ["Guaitecas","Cisnes","Aysen","Coyhaique","Lago Verde","Rio Ibañez","Chile Chico","Cochrane","Tortel","O'Higins"],

  "Región de Magallanes y la Antártica Chilena": ["Torres del Paine","Puerto Natales","Laguna Blanca","San Gregorio","Rio Verde","Punta Arenas","Porvenir","Primavera","Timaukel","Antartica"],

  "Región Metropolitana de Santiago ": ["Tiltil","Colina","Lampa","Conchali","Quilicura","Renca","Las Condes","Pudahuel","Quinta Normal","Providencia","Santiago","La Reina","Ñuñoa","San Miguel",
"Maipu","La Cisterna","La Florida","La Granja","Independencia","Huechuraba","Recoleta","Vitacura","Lo Barrenechea","Macul","Peñalolen","San Joaquin","La Pintana","San Ramon","El Bosque","Pedro Aguirre Cerda",
"Lo Espejo","Estacion Central","Cerrillos","Lo Prado","Cerro Navia","San Jose de Maipo","Puente Alto","Pirque","San Bernardo","Calera de Tango","Buin","Paine","Peñaflor","Talagante","El Monte","Isla de Maipo",
"Curacavi","Maria Pinto","Melipilla","San Pedro","Alhue","Padre Hurtado"],

  "Región de Los Ríos": ["Lanco","Mariquina","Panguipulli","Mafil","Valdivia","Los Lagos","Corral","Paillaco","Futrono","Lago Ranco","La Union","Rio Bueno"],

  "Región Arica y Parinacota": ["Gral. Lagos","Putre","Arica","Camarones"],

  "Región del Ñuble": ["Cobquecura","Ñiquen","San Fabian","San Carlos","Quirihue","Ninhue","Trehuaco","San Nicolas","Coihueco","Chillan","Portezuelo","Pinto","Coelemu","Bulnes","San Ignacio",
"Ranquil","Quillon","El Carmen","Pemuco","Yungay","Chillan Viejo"]
  };

const poblarRegiones = () => {
  console.log("Cargando regiones desde la API...");
  let regionSelect = document.getElementById("region");
  
  // Limpiar el dropdown de regiones
  regionSelect.innerHTML = '<option value="">Seleccione una región</option>';
  
  // Obtener regiones desde la API
  fetch('/api/regiones')
    .then(response => {
      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }
      return response.json();
    })
    .then(regiones => {
      console.log("Regiones recibidas:", regiones);
      
      // Agregar las regiones al dropdown
      regiones.forEach(region => {
        let option = document.createElement("option");
        option.value = region.id; // Usar el ID como valor
        option.text = region.nombre; // Mostrar el nombre
        option.setAttribute('data-nombre', region.nombre); // Guardar el nombre como atributo
        regionSelect.appendChild(option);
      });
    })
    .catch(error => {
      console.error("Error al obtener regiones:", error);
      
      // Fallback: usar los datos estáticos si la petición falla
      console.log("Usando datos estáticos como fallback para regiones");
      for (const region in region_comuna) {
        let option = document.createElement("option");
        option.value = region;
        option.text = region;
        regionSelect.appendChild(option);
      }
    });
};

const updateComunas = () => {
  let regionSelect = document.getElementById("region");
  let comunaSelect = document.getElementById("comuna");
  let selectedRegionId = regionSelect.value;
  
  // Limpiar el dropdown de comunas
  comunaSelect.innerHTML = '<option value="">Seleccione una comuna</option>';
  
  if (!selectedRegionId) {
    console.log("No se ha seleccionado ninguna región");
    return;
  }
  
  console.log("Cargando comunas para la región ID:", selectedRegionId);
  
  // Obtener comunas desde la API usando el ID de la región
  fetch(`/api/comunas?region_id=${encodeURIComponent(selectedRegionId)}`)
    .then(response => {
      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }
      return response.json();
    })
    .then(comunas => {
      console.log("Comunas recibidas:", comunas);
      
      // Agregar las comunas al dropdown
      comunas.forEach(comuna => {
        let option = document.createElement("option");
        option.value = comuna.id; // Usar el ID como valor
        option.text = comuna.nombre; // Mostrar el nombre
        option.setAttribute('data-nombre', comuna.nombre); // Guardar el nombre como atributo
        comunaSelect.appendChild(option);
      });
      
      // Si no hay comunas, mostrar un mensaje
      if (comunas.length === 0) {
        let option = document.createElement("option");
        option.value = "";
        option.text = "No hay comunas disponibles";
        option.disabled = true;
        comunaSelect.appendChild(option);
      }
    })
    .catch(error => {
      console.error("Error al obtener comunas:", error);
      
      // Fallback: usar los datos estáticos si la petición falla
      const selectedOption = regionSelect.options[regionSelect.selectedIndex];
      const regionNombre = selectedOption.getAttribute('data-nombre') || selectedOption.text;
      
      if (region_comuna[regionNombre]) {
        console.log("Usando datos estáticos como fallback para la región:", regionNombre);
        region_comuna[regionNombre].forEach(comuna => {
          let option = document.createElement("option");
          option.value = comuna; // En el fallback, usamos el nombre como valor
          option.text = comuna;
          comunaSelect.appendChild(option);
        });
      } else {
        console.log("No se encontraron datos estáticos para la región:", regionNombre);
      }
    });
};

function extraContact() {
  // Seleccionar todos los checkboxes de contacto
  const contactCheckboxes = document.querySelectorAll('.contact-checkbox');
  
  // Agregar event listener a cada checkbox
  contactCheckboxes.forEach(checkbox => {
    // Eliminar event listeners previos para evitar duplicados
    checkbox.removeEventListener('change', toggleContactField);
    // Agregar nuevo event listener
    checkbox.addEventListener('change', toggleContactField);
    
    // Inicializar el estado del campo extra según el estado actual del checkbox
    const extraField = checkbox.closest('.contact-option').querySelector('.contacto-extra-field');
    if (checkbox.checked) {
      extraField.style.display = 'block';
    } else {
      extraField.style.display = 'none';
    }
  });
}

// Función para mostrar/ocultar el campo extra cuando se marca/desmarca un checkbox
function toggleContactField(event) {
  const checkbox = event.target;
  const extraField = checkbox.closest('.contact-option').querySelector('.contacto-extra-field');
  
  if (checkbox.checked) {
    extraField.style.display = 'block';
    // Hacer que el campo sea requerido cuando está visible
    const inputField = extraField.querySelector('input');
    if (inputField) {
      inputField.setAttribute('required', 'required');
    }
  } else {
    extraField.style.display = 'none';
    // Quitar el atributo required cuando está oculto
    const inputField = extraField.querySelector('input');
    if (inputField) {
      inputField.removeAttribute('required');
    }
  }
}

function addPhoto() {
  const photoContainer = document.getElementById("fotosContainer");
  
  if (photoContainer.childElementCount < 4) {
    // Crear un contenedor para el input y el botón de eliminación
    const photoInputContainer = document.createElement("div");
    photoInputContainer.className = "photo-input-container";
    
    // Crear el input de tipo file
    const newPhotoInput = document.createElement("input");
    newPhotoInput.type = "file";
    newPhotoInput.name = "foto[]";
    newPhotoInput.accept = "image/*";
    newPhotoInput.className = "photo-input";
    
    // Crear el botón de eliminación (cruz)
    const deleteButton = document.createElement("button");
    deleteButton.type = "button";
    deleteButton.className = "delete-photo-btn";
    deleteButton.innerHTML = "&times;";
    deleteButton.title = "Eliminar foto";
    
    // Agregar evento para eliminar el contenedor cuando se hace clic en la cruz
    deleteButton.addEventListener("click", function() {
      photoContainer.removeChild(photoInputContainer);
    });
    
    // Agregar los elementos al contenedor
    photoInputContainer.appendChild(newPhotoInput);
    photoInputContainer.appendChild(deleteButton);
    
    // Agregar el contenedor al DOM
    photoContainer.appendChild(photoInputContainer);
  } else {
    alert("No se pueden agregar más de 5 fotos.");
    return;
  }
}


function handleTemaOtro() {
  // Seleccionar todos los checkboxes de tema
  const temaCheckboxes = document.querySelectorAll('.tema-checkbox');
  
  // Agregar event listener a cada checkbox
  temaCheckboxes.forEach(checkbox => {
    // Eliminar event listeners previos para evitar duplicados
    checkbox.removeEventListener('change', toggleTemaOtroField);
    // Agregar nuevo event listener
    checkbox.addEventListener('change', toggleTemaOtroField);
    
    // Inicializar el estado del campo extra para "Otro"
    if (checkbox.id === 'otro' && checkbox.checked) {
      const otroField = document.querySelector('.tema-otro-field');
      if (otroField) {
        otroField.style.display = 'block';
        const inputField = otroField.querySelector('input');
        if (inputField) {
          inputField.setAttribute('required', 'required');
        }
      }
    }
  });
}

// Función para mostrar/ocultar el campo de texto cuando se marca/desmarca el checkbox "Otro"
function toggleTemaOtroField(event) {
  const checkbox = event.target;
  
  // Solo mostrar/ocultar el campo si es el checkbox "Otro"
  if (checkbox.id === 'otro') {
    const otroField = document.querySelector('.tema-otro-field');
    if (otroField) {
      if (checkbox.checked) {
        otroField.style.display = 'block';
        // Hacer que el campo sea requerido cuando está visible
        const inputField = otroField.querySelector('input');
        if (inputField) {
          inputField.setAttribute('required', 'required');
        }
      } else {
        otroField.style.display = 'none';
        // Quitar el atributo required cuando está oculto
        const inputField = otroField.querySelector('input');
        if (inputField) {
          inputField.removeAttribute('required');
        }
      }
    }
  }
}

window.onload = () => {
  poblarRegiones();
  extraContact();
  handleTemaOtro();

  document.getElementById("agregarFoto").addEventListener("click", addPhoto);
  document.getElementById("region").addEventListener("change", updateComunas);

};