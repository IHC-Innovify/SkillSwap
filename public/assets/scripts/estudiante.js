// --- Script para la página de Estudiante ---

// Función para mostrar la sección correcta y ocultar las demás
function mostrarSeccionEstudiante(idSeccionAMostrar) {
    // 1. Ocultar todas las secciones
    document.querySelectorAll('.panel-seccion').forEach(seccion => {
      seccion.classList.remove('activa');
    });
    
    // 2. Mostrar solo la sección deseada
    const seccion = document.getElementById(idSeccionAMostrar);
    if (seccion) {
      seccion.classList.add('activa');
    }
}

// Se ejecuta cuando todo el HTML está cargado
document.addEventListener('DOMContentLoaded', () => {
  // --- Lógica para el Dark Mode ---
    
    // Encontrar el interruptor
    const themeToggle = document.getElementById('theme-toggle');
    
    // Comprobar si hay un tema guardado en localStorage al cargar la página
    const currentTheme = localStorage.getItem('theme');
    if (currentTheme) {
        document.body.classList.add(currentTheme);
        // Sincronizar el interruptor si el tema guardado es 'dark-mode'
        if (currentTheme === 'dark-mode' && themeToggle) {
            themeToggle.checked = true;
        }
    }

    // Añadir el listener para el clic (evento 'change')
    if (themeToggle) { // Comprobar que el interruptor exista en esta página
        themeToggle.addEventListener('change', function() {
            if (this.checked) {
                // Si está marcado, activa el dark mode
                document.body.classList.add('dark-mode');
                localStorage.setItem('theme', 'dark-mode'); // Guardar preferencia
            } else {
                // Si no está marcado, desactiva el dark mode
                document.body.classList.remove('dark-mode');
                localStorage.setItem('theme', 'light-mode'); // Guardar preferencia
            }
        });
    }
    // --- Fin de la lógica para el Dark Mode ---

    // --- Lógica para botones toggle del Perfil ---

  /**
   * Configura un grupo de botones para que sean "toggleables".
   * @param {string} containerId El ID del div que contiene los botones.
   */
  function setupToggleButtons(containerId) {
      const container = document.getElementById(containerId);
      if (!container) {
          // Si el contenedor no existe en la página actual, no hace nada.
          return; 
      }

      const toggleType = container.dataset.toggle; // 'single' o 'multiple'
      const buttons = container.querySelectorAll('.boton-toggle');

      buttons.forEach(button => {
          button.addEventListener('click', (e) => {
              e.preventDefault(); // Previene cualquier acción por defecto del botón

              if (toggleType === 'single') {
                  // --- Lógica para SELECCIÓN ÚNICA ---
                  // 1. Quita la clase 'activo' de todos los botones de este grupo
                  buttons.forEach(btn => btn.classList.remove('activo'));
                  // 2. Añade la clase 'activo' solo al botón que fue clickeado
                  e.target.classList.add('activo');

              } else if (toggleType === 'multiple') {
                  // --- Lógica para SELECCIÓN MÚLTIPLE ---
                  // Simplemente añade o quita la clase del botón clickeado
                  e.target.classList.toggle('activo');
              }
          });
      });
  }

  // Registramos los 3 grupos de botones que acabamos de crear en el HTML
  setupToggleButtons('btn-group-estado');
  setupToggleButtons('btn-group-dias');
  setupToggleButtons('btn-group-tipo');
  
  // --- Fin Lógica para botones toggle del Perfil ---

// --- (NUEVO) Lógica para botones de Añadir Habilidades/Dominio ---
    
    // Botón '+' de Habilidades
    const btnAddHabilidades = document.getElementById('btn-add-habilidades');
    if (btnAddHabilidades) {
        btnAddHabilidades.addEventListener('click', (e) => {
            e.preventDefault();
            // Llama a la función que ya creamos para cambiar de panel
            mostrarSeccionEstudiante('panel-add-habilidades');
        });
    }

    // Botón '+' de Temas de Dominio
    const btnAddDominio = document.getElementById('btn-add-dominio');
    if (btnAddDominio) {
        btnAddDominio.addEventListener('click', (e) => {
            e.preventDefault();
            // Llama a la función que ya creamos para cambiar de panel
            mostrarSeccionEstudiante('panel-add-dominio');
        });
    }

    // --- Fin Lógica para botones de Añadir ---

    // --- Lógica para Campos Editables del Perfil ---
  
  /**
   * Configura un botón para que haga un campo de texto editable.
   * @param {HTMLElement} button El botón que tiene el atributo 'data-target'.
   */
  function setupEditableField(button) {
    const targetId = button.dataset.target;
    if (!targetId) return;

    const field = document.getElementById(targetId);
    if (!field) return;

    button.addEventListener('click', (e) => {
      e.preventDefault();
      
      const isEditable = field.isContentEditable;
      
      if (isEditable) {
        // Si YA ESTÁ editable, lo "guardamos" (desactivamos)
        field.contentEditable = false;
        field.classList.remove('editable-field-active');
        button.textContent = '✏️'; // Cambia ícono a lápiz
        button.title = 'Editar';
        // Aquí podrías añadir el código para guardar el dato en una base de datos
        // console.log("Guardado:", field.textContent); 
      } else {
        // Si NO ESTÁ editable, lo activamos
        field.contentEditable = true;
        field.classList.add('editable-field-active');
        button.textContent = '💾'; // Cambia ícono a guardar (disquete)
        button.title = 'Guardar';
        field.focus(); // Pone el cursor en el campo
      }
    });
  }

  // Aplicamos la lógica a TODOS los botones que tengan la clase .btn-edit-field
  document.querySelectorAll('.btn-edit-field').forEach(setupEditableField);

  // --- Fin Lógica para Campos Editables ---

  // --- NAVEGACIÓN PRINCIPAL ---

  // Link "Mis tutores"
  document.getElementById('nav-mis-tutores').addEventListener('click', (e) => {
    e.preventDefault();
    mostrarSeccionEstudiante('panel-tutores');
  });

  // Link "Sesiones"
  document.getElementById('nav-sesiones').addEventListener('click', (e) => {
    e.preventDefault();
    mostrarSeccionEstudiante('panel-sesiones');
  });

  // Link "Lupa (Buscar)"
  document.getElementById('nav-buscar').addEventListener('click', (e) => {
    e.preventDefault();
    mostrarSeccionEstudiante('panel-buscar');
  });

  // Link "Perfil (Icono)"
  document.getElementById('nav-perfil').addEventListener('click', (e) => {
    e.preventDefault();
    mostrarSeccionEstudiante('panel-perfil');
  });

  // --- BOTONES DENTRO DEL DASHBOARD ---

  // Botón "Aprender un nuevo tema"
  const btnAprender = document.getElementById('nav-aprender');
  if (btnAprender) {
    btnAprender.addEventListener('click', (e) => {
        e.preventDefault();
        mostrarSeccionEstudiante('panel-buscar');
    });
  }

  // aseguramos de que el dashboard sea lo primero que se vea al cargar la página.
  mostrarSeccionEstudiante('panel-dashboard-estudiante');
});