// --- Script COMPLETO CORREGIDO para la página de Estudiante ---

// 1. Función para cambiar de sección (Panel)
function mostrarSeccionEstudiante(idSeccionAMostrar) {
    // Ocultar todas las secciones activas
    document.querySelectorAll('.panel-seccion').forEach(seccion => {
      seccion.classList.remove('activa');
    });
    
    // Mostrar la sección deseada
    const seccion = document.getElementById(idSeccionAMostrar);
    if (seccion) {
      seccion.classList.add('activa');
      // Scrollear arriba al cambiar de sección
      window.scrollTo(0, 0);
    } else {
        console.warn("No se encontró la sección:", idSeccionAMostrar);
    }
}

// 2. Función para botones de opción (Perfil - Estado, Días, Tipo)
function setupToggleButtons(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const toggleType = container.dataset.toggle; // 'single' o 'multiple'
    const buttons = container.querySelectorAll('.boton-toggle');

    buttons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            if (toggleType === 'single') {
                buttons.forEach(btn => btn.classList.remove('activo'));
                e.target.classList.add('activo');
            } else if (toggleType === 'multiple') {
                e.target.classList.toggle('activo');
            }
        });
    });
}

// 3. Función para editar texto (Perfil - Lápiz/Guardar)
function setupEditableField(button) {
    const targetId = button.dataset.target;
    if (!targetId) return;
    const field = document.getElementById(targetId);
    if (!field) return;

    button.addEventListener('click', (e) => {
      e.preventDefault();
      const isEditable = field.isContentEditable;
      
      if (isEditable) {
        // Guardar
        field.contentEditable = false;
        field.classList.remove('editable-field-active');
        button.textContent = '✎'; 
        button.title = 'Editar';
      } else {
        // Editar
        field.contentEditable = true;
        field.classList.add('editable-field-active');
        button.textContent = '💾'; 
        button.title = 'Guardar';
        field.focus(); 
      }
    });
}


// ==============================================================
// INICIO: Ejecución al cargar el DOM
// ==============================================================
document.addEventListener('DOMContentLoaded', () => {

  // --- A. GESTIÓN DEL MODO OSCURO (Sincronizado) ---
  const togglePerfil = document.getElementById('theme-toggle'); // Switch en perfil
  const toggleAjustes = document.getElementById('theme-toggle-ajustes'); // Switch en ajustes

  function aplicarModoOscuro(activar) {
      if (activar) {
          document.body.classList.add('dark-mode');
          localStorage.setItem('theme', 'dark-mode');
      } else {
          document.body.classList.remove('dark-mode');
          localStorage.setItem('theme', 'light-mode');
      }
      // Sincronizar ambos interruptores si existen
      if(togglePerfil) togglePerfil.checked = activar;
      if(toggleAjustes) toggleAjustes.checked = activar;
  }

  // 1. Cargar preferencia guardada
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark-mode') {
      aplicarModoOscuro(true);
  }

  // 2. Event Listeners para los switches
  if (togglePerfil) {
      togglePerfil.addEventListener('change', function() { aplicarModoOscuro(this.checked); });
  }
  if (toggleAjustes) {
      toggleAjustes.addEventListener('change', function() { aplicarModoOscuro(this.checked); });
  }


  // --- B. NAVEGACIÓN PRINCIPAL (Barra Superior) ---
  const mapNav = {
      'nav-mis-tutores': 'panel-tutores',
      'nav-sesiones': 'panel-sesiones',
      'nav-buscar': 'panel-buscar',
      'nav-perfil': 'panel-perfil',
      'nav-aprender': 'panel-buscar' // Botón amarillo del dashboard
  };

  for (const [idBtn, idPanel] of Object.entries(mapNav)) {
      const btn = document.getElementById(idBtn);
      if (btn) {
          btn.addEventListener('click', (e) => {
              e.preventDefault();
              mostrarSeccionEstudiante(idPanel);
          });
      }
  }


  // --- C. NAVEGACIÓN DE AJUSTES (Sidebar e ir/volver) ---
  
  // 1. Botón "⚙ Ajustes" en el Perfil -> Abre Apariencia
  const btnAbrirAjustes = document.querySelector('.btn-ajustes');
  if (btnAbrirAjustes) {
      btnAbrirAjustes.addEventListener('click', (e) => {
          e.preventDefault();
          mostrarSeccionEstudiante('panel-ajustes-apariencia');
      });
  }

  // 2. Navegación interna entre Apariencia y Chat
  const btnIrChat = document.getElementById('btn-ir-chat-desde-apariencia');
  if (btnIrChat) {
      btnIrChat.addEventListener('click', (e) => {
          e.preventDefault();
          mostrarSeccionEstudiante('panel-ajustes-chat');
      });
  }

  const btnIrApariencia = document.getElementById('btn-ir-apariencia-desde-chat');
  if (btnIrApariencia) {
      btnIrApariencia.addEventListener('click', (e) => {
          e.preventDefault();
          mostrarSeccionEstudiante('panel-ajustes-apariencia');
      });
  }

  // 3. Botones "Volver al Perfil"
  const btnVolver1 = document.getElementById('btn-volver-perfil-1'); // En Apariencia
  if (btnVolver1) {
      btnVolver1.addEventListener('click', (e) => {
          e.preventDefault();
          mostrarSeccionEstudiante('panel-perfil');
      });
  }

  const btnVolver2 = document.getElementById('btn-volver-perfil-2'); // En Chat
  if (btnVolver2) {
      btnVolver2.addEventListener('click', (e) => {
          e.preventDefault();
          mostrarSeccionEstudiante('panel-perfil');
      });
  }


  // --- D. LÓGICA DEL PERFIL (Campos y Botones) ---
  setupToggleButtons('btn-group-estado');
  setupToggleButtons('btn-group-dias');
  setupToggleButtons('btn-group-tipo');
  document.querySelectorAll('.btn-edit-field').forEach(setupEditableField);

  // Botones '+' (Agregar Habilidad/Dominio)
  const btnAddHabilidades = document.querySelector('.habilidades .agregar');
  if (btnAddHabilidades) {
      btnAddHabilidades.addEventListener('click', (e) => { 
          e.preventDefault(); 
          mostrarSeccionEstudiante('panel-add-habilidades'); 
      });
  }

  const btnAddDominio = document.querySelector('.temas-dominio .agregar');
  if (btnAddDominio) {
      btnAddDominio.addEventListener('click', (e) => { 
          e.preventDefault(); 
          mostrarSeccionEstudiante('panel-add-dominio'); 
      });
  }


  // --- E. TEMAS DE COLOR (Ajustes de Apariencia) ---
  const colorButtons = document.querySelectorAll('.btn-color');
  
  // Recuperar tema guardado
  const savedColorTheme = localStorage.getItem('colorTheme');
  if (savedColorTheme) {
      document.body.classList.add(savedColorTheme);
      // Actualizar selección visual
      const colorName = savedColorTheme.replace('theme-', '');
      const activeBtn = document.querySelector(`.btn-color[data-color="${colorName}"]`);
      if(activeBtn) {
          document.querySelector('.btn-color.selected')?.classList.remove('selected');
          activeBtn.classList.add('selected');
      }
  }

  colorButtons.forEach(btn => {
      btn.addEventListener('click', (e) => {
          // 1. Quitar selección anterior
          document.querySelector('.btn-color.selected')?.classList.remove('selected');
          // 2. Marcar nuevo
          e.target.classList.add('selected');

          // 3. Limpiar clases previas del body
          document.body.classList.remove('theme-pink', 'theme-lightblue', 'theme-orange');

          // 4. Aplicar nuevo
          const color = e.target.dataset.color;
          if (color !== 'default') {
              const themeClass = `theme-${color}`;
              document.body.classList.add(themeClass);
              localStorage.setItem('colorTheme', themeClass);
          } else {
              localStorage.removeItem('colorTheme'); // Default no se guarda
          }
      });
  });


  // --- F. RESPUESTAS RÁPIDAS (Ajustes de Chat) ---
  
  // 1. Referencias a elementos (usando IDs específicos)
  const inputReply = document.getElementById('input-quick-reply');
  const btnAddReply = document.getElementById('btn-add-reply');
  const listReply = document.getElementById('lista-respuestas-rapidas');
  const noRepliesMsg = document.getElementById('no-replies-msg');

  // 2. Cargar datos guardados
  let quickReplies = JSON.parse(localStorage.getItem('quickReplies')) || [
      "¡Hola! Estoy listo para la sesión.",
      "Gracias por tu ayuda.",
      "¿Podemos reagendar?"
  ];

  // 3. Función para dibujar la lista
  function renderReplies() {
      if (!listReply) return;
      listReply.innerHTML = ''; // Limpiar lista actual
      
      if (quickReplies.length === 0) {
          if(noRepliesMsg) noRepliesMsg.style.display = 'block';
      } else {
          if(noRepliesMsg) noRepliesMsg.style.display = 'none';
          
          quickReplies.forEach((text, index) => {
              const li = document.createElement('li');
              // Creamos el contenido del li
              li.innerHTML = `
                  <span>${text}</span>
                  <span class="btn-delete-reply" data-index="${index}" title="Eliminar" style="cursor:pointer; color:red; font-weight:bold;">✖</span>
              `;
              listReply.appendChild(li);
          });

          // Añadir eventos de borrado a los nuevos botones X
          document.querySelectorAll('.btn-delete-reply').forEach(btn => {
              btn.addEventListener('click', (e) => {
                  e.stopPropagation(); // Evitar burbujeo
                  const index = e.target.dataset.index;
                  deleteReply(index);
              });
          });
      }
  }

  // 4. Función para borrar
  function deleteReply(index) {
      quickReplies.splice(index, 1);
      localStorage.setItem('quickReplies', JSON.stringify(quickReplies));
      renderReplies();
  }

  // 5. Función para añadir (separada para poder reutilizarla)
  function addNewReply() {
      if (!inputReply) return;
      
      const text = inputReply.value.trim();
      if (text) {
          quickReplies.push(text);
          localStorage.setItem('quickReplies', JSON.stringify(quickReplies));
          inputReply.value = ''; // Limpiar input
          renderReplies();
          console.log("Respuesta agregada:", text);
      } else {
          alert("Por favor escribe algo antes de agregar.");
      }
  }

  // 6. Inicialización y Listeners
  if (listReply) {
      renderReplies(); // Mostrar lista al cargar

      if (btnAddReply) {
          btnAddReply.addEventListener('click', (e) => {
              e.preventDefault(); // Prevenir submit
              addNewReply();
          });
      }

      if (inputReply) {
          // Permitir agregar presionando "Enter"
          inputReply.addEventListener('keypress', (e) => {
              if (e.key === 'Enter') {
                  e.preventDefault();
                  addNewReply();
              }
          });
      }
  }


  // --- INICIO POR DEFECTO ---
  // Mostrar Dashboard al cargar
  mostrarSeccionEstudiante('panel-dashboard-estudiante');

});