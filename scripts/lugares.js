function mostrarParrafo(numero) {
    var parrafo = document.getElementById("parrafo" + numero);
    
    if (parrafo.style.display === "none" || parrafo.style.display === "") {
      parrafo.style.display = "block"; // Cambia la propiedad display para mostrar
      setTimeout(function() {
        parrafo.style.opacity = 1; // Cambia gradualmente la opacidad a 1 para que aparezca de a poco
      }, 10); // Un pequeño retraso para permitir que la transición se aplique correctamente
    } else {
      parrafo.style.opacity = 0; // Cambia gradualmente la opacidad a 0 para que desaparezca de a poco
      setTimeout(function() {
        parrafo.style.display = "none"; // Cambia la propiedad display para ocultar después de la transición
      }, 500); // Espera 0.5 segundos para permitir que la transición se complete antes de ocultar el párrafo
    }
  }