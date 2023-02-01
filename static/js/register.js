const form = document.querySelector('#formRegistro');

let usuarios = [];
let editar = false;
let usuarioId = null;

window.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch("/goodtrip/usuarios")
    const data = await response.json()
    usuarios = data
    console.log(data)
    renderUsuario(usuarios)
})


form.addEventListener('submit', async e => {
    e.preventDefault()

    const nombre = form['nombre'].value;
    const apellido = form['apellido'].value;
    const email = form['email'].value;
    const clave = form['clave'].value;
    const sector = form['sector'].value;

    console.log(nombre, apellido, email, clave, sector)
    if (!editar) {
        const response = await fetch("/goodtrip/usuarios", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nombre,
                apellido,
                email,
                clave,
                sector,
            })
        })

        const data = await response.json();
        console.log(data);
        usuarios.unshift(data);
        renderUsuario(usuarios);
        formRegistro.reset();
    }
    else {
        const response = await fetch(`/goodtrip/usuarios/${usuarioId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nombre,
                apellido,
                email,
                clave,
                sector,
            })
        })

        const updataUser = await response.json()
        usuarios = usuarios.map(usuario => usuario.id_usuario === updataUser.id_usuario ? updataUser : usuario)
        renderUsuario(usuarios)
        editar = false
        usuarioId = null

    }

    renderUsuario(usuarios)
    form.reset()



});

function renderUsuario(usuarios) {
    const usuarioList = document.querySelector('#usuarioList')
    usuarioList.innerHTML = ""
    usuarios.forEach(user => {
        const usuarioItem = document.createElement('li')
        usuarioItem.classList = 'list-group'
        usuarioItem.innerHTML = `
        <header>
        <div>
        <h3>${user.nombre}  ${user.apellido}</h3>
        </div>
        </header>
        <body>
        <p>
        ${user.email}
        </p>
         <p>
        ${user.clave}
        </p>
         <p>
        ${user.sector}
        </p>
        <div class="d-flex align-items-center;">
            <button class="btn-delete btn btn-danger">borrar</button>
            <button class="btn-edit btn  btn-danger "  >actualizar</button>
        </div>
        
        </body>
        `
        const btnDelete = usuarioItem.querySelector('.btn-delete')

        btnDelete.addEventListener('click', async () => {
            console.log(user.id_usuario)
            const response = await fetch(`/goodtrip/usuarios/${user.id_usuario}`, {
                method: 'DELETE',
            })
            const data = await response.json()
            console.log(data)

            usuarios = usuarios.filter(usuario => usuario.id_usuario !== data.id_usuario)
            renderUsuario(usuarios)

        })
        const btnEdit = usuarioItem.querySelector('.btn-edit')

        btnEdit.addEventListener('click', async () => {
            console.log(user.id_usuario)
            const response = await fetch(`/goodtrip/usuarios/${user.id_usuario}`)
            const data = await response.json()

            form['nombre'].value = data.nombre;
            form['apellido'].value = data.apellido;
            form['email'].value = data.email;
            form['clave'].value = data.clave;
            form['sector'].value = data.sector;

            editar = true
            console.log(data)
            usuarioId = user.id_usuario
        })



        console.log(usuarioItem);
        usuarioList.append(usuarioItem);
    })
}