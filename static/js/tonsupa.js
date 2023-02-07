const form = document.querySelector('#form');


let comentarios = [];
let editar = false;
let comentarioId = null;
window.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch("/goodtrip/comentarioTonsupa")
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

    if (!editar) {
        const response = await fetch('/goodtrip/comentarioTonsupa', {
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
        comentarios.unshift(data);
        renderComentario(comentarios)
        form.reset()
    }
    else {
        const response = await fetch(`/goodtrip/comentarioTonsupa/${comentarioId}`, {
            method: 'PUT',
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

        const updataUser = await response.json()
        comentarios = comentarios.map(comentario => comentario.id === updataUser.id ? updataUser : comentario)
        renderComentario(comentarios)
        editar = false
        comentarioId = null
    }

    renderComentario(comentarios);
    form.reset();

});

function renderComentario(comentarios) {
    const comentarioList = document.querySelector('#comentarioList')
    comentarioList.innerHTML = ""
    comentarios.forEach(comentario => {
        const comentarioItem = document.createElement('li')
        comentarioItem.classList = 'list-group list-group-item-dark my-2'
        comentarioItem.innerHTML = `
        <header>
        <div>
        <h3>${comentario.nombre}  ${comentario.apellido}</h3>
        </div>
        </header>
        <body    >
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
        <div class="d-flex align-items-center;">
            <button class="btn-delete btn btn-danger">borrar</button>
            <button class="btn-edit btn  btn-danger "  >actualizar</button>
        </div>
        
        </body>
        `

        const btnDelete = comentarioItem.querySelector('.btn-delete')

        btnDelete.addEventListener('click', async () => {
            console.log(comentario.id)
            const response = await fetch(`/goodtrip/comentarioTonsupa/${comentario.id}`, {
                method: 'DELETE',
            })
            const data = await response.json()
            console.log(data)
            comentarios = comentarios.filter(comentario => comentario.id !== data.id)
            renderComentario(comentarios)
        })

        const btnEdit = comentarioItem.querySelector('.btn-edit')

        btnEdit.addEventListener('click', async () => {
            console.log(comentario.id)
            const response = await fetch(`/goodtrip/comentarioTonsupa/${comentario.id}`)
            const data = await response.json()

            form['nombre'].value = data.nombre;
            form['apellido'].value = data.apellido;
            form['sexo'].value = data.sexo;
            form['nacionalidad'].value = data.nacionalidad;
            form['observacion'].value = data.observacion;
            form['conclucion'].value = data.conclucion;

            editar = true
            console.log(data)
            comentarioId = comentario.id
        })





        console.log(comentarioItem);
        comentarioList.append(comentarioItem);
    })
}