
  // Función para mostrar la sección correcta y ocultar las demás
  function mostrarSeccion(idSeccionAMostrar) {
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

  // Añadir los "event listeners" a los links de navegación
  // Se ejecuta cuando todo el HTML está cargado
  document.addEventListener('DOMContentLoaded', () => {
    
    // Link del Panel (icono de perfil)
    document.getElementById('nav-dashboard').addEventListener('click', (e) => {
      e.preventDefault(); // Evita que la página salte por el href="#"
      mostrarSeccion('panel-dashboard');
    });

    // Link de Verificación
    document.getElementById('nav-verificacion').addEventListener('click', (e) => {
      e.preventDefault();
      // Por defecto, mostramos el panel con contenido.
      // Puedes cambiar 'panel-verificacion' por 'panel-verificacion-vacio' si quieres probar esa vista
      mostrarSeccion('panel-verificacion'); 
    });

    // Link de Reportes
    document.getElementById('nav-reportes').addEventListener('click', (e) => {
      e.preventDefault();
      mostrarSeccion('panel-reportes');
    });

    // Link de Estudiantes
    document.getElementById('nav-estudiantes').addEventListener('click', (e) => {
      e.preventDefault();
      mostrarSeccion('panel-estudiantes');
    });

    // Opcional: Nos aseguramos de que el dashboard sea lo primero que se vea al cargar la página.
    // (Esto es una doble seguridad, ya que también pusimos la clase 'activa' en el HTML)
    mostrarSeccion('panel-dashboard');
  });
