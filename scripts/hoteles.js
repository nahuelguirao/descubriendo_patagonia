// Obtén el select y los divs
const select = document.getElementById("lugares");
const divOpcion1 = document.getElementById("divOpcion1");
const divOpcion2 = document.getElementById("divOpcion2");
const divOpcion3 = document.getElementById("divOpcion3");
const divOpcion4 = document.getElementById("divOpcion4");

// Agrega un event listener para el cambio en el select
select.addEventListener("change", function () {
  // Obtén el valor de la opción seleccionada
  const opcionSeleccionada = select.value;

  // Oculta todos los divs
  divOpcion1.style.display = "none";
  divOpcion2.style.display = "none";
  divOpcion3.style.display = "none";
  divOpcion4.style.display = "none";

  // Muestra el div correspondiente a la opción seleccionada
  if (opcionSeleccionada === "peritomoreno") {
    divOpcion1.style.display = "block";
  } else if (opcionSeleccionada === "bariloche") {
    divOpcion2.style.display = "block";
  } else if (opcionSeleccionada === "tierradelfuego") {
    divOpcion3.style.display = "block";
  } else if (opcionSeleccionada === "puertomadryn") {
    divOpcion4.style.display = "block";
  }
});
