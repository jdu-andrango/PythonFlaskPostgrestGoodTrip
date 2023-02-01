const form = document.querySelector('#form');


let comentarios = [];

window.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch("/goodtrip/comentario")
    const data = await response.json()
    comentarios = data
    console.log(data)
    renderComentario(comentarios)
})


form.addEventListener('submit', async e => {
    e.preventDefault()

    const nombre = form['nombre'].value;
    const apellido = form['apellido'].value;
    const sexo = form['sexo'].value;
    const nacionalidad = form['nacionalidad'].value;
    const observacion = form['observacion'].value;
    const conclucion = form['conclucion'].value;

    console.log(nombre, apellido, sexo, nacionalidad, observacion, conclucion)

    const response = await fetch('/goodtrip/comentario', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            nombre,
            apellido,
            sexo,
            nacionalidad,
            observacion,
            conclucion,
        })
    })

    const data = await response.json();
    console.log(data);
    comentarios.push(data);
    renderComentario(comentarios);
    form.reset();

});

function renderComentario(comentarios) {
    const comentarioList = document.querySelector('#comentarioList')
    comentarioList.innerHTML = ""
    comentarios.forEach(comentario => {
        const comentarioItem = document.createElement('li')
        comentarioItem.classList = 'list-group'
        comentarioItem.innerHTML = `
        <header>
        <div>
        <h3>${comentario.nombre}  ${comentario.apellido}</h3>
        </div>
        </header>
        <body>
        <p>
        ${comentario.sexo}
        </p>
         <p>
        ${comentario.nacionalidad}
        </p>
         <p>
        ${comentario.observacion}
        </p>
         <p>
        ${comentario.conclucion}
        </p>
        
        </body>
        `

        console.log(comentarioItem);
        comentarioList.append(comentarioItem);
    })
}