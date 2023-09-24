// MENU DESPLEGABLE TABLET / MOBILE

let iconoMenu = document.getElementById("icono-menu");
let nav = document.getElementById("navbar");

iconoMenu.addEventListener("click", function () {
  if (nav.classList.contains("mostrar")) {
    nav.classList.remove("mostrar");
    nav.classList.add("cerrar");
  } else {
    nav.classList.add("mostrar");
    nav.classList.remove("cerrar");
  }
});
