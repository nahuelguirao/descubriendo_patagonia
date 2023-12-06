document.getElementById('formularioContacto').addEventListener('submit', (e) => {
    e.preventDefault()

    const datos = new FormData();
    datos.append('nombre', document.getElementById('nombre').value);
    datos.append('email', document.getElementById('email').value);
    datos.append('telefono', document.getElementById('telefono').value);
    datos.append('asunto', document.getElementById('asunto').value);
    datos.append('mensaje', document.getElementById('mensaje').value);

    fetch('http://NahueOli.pythonanywhere.com/mensajes', {
        method: 'POST',
        body: datos
    })
        .then(respuesta => {
            if (respuesta.ok){
                document.querySelector('.contacto').style.display = 'none'
                alert("Formulario enviado con éxito.")
                setTimeout(function() {
                    document.getElementById('formularioContacto').reset()
                    document.querySelector('.contacto').style.display = 'block'
                }, 2000)
            } else {
                throw new Error('ERROR al enviar los datos')
            }
        })
})