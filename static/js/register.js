const form = document.querySelector('#formRegistro');

let usuarios = [];

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
    usuarios.push(data);
    renderUsuario(usuarios);
    formRegistro.reset();

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
        
        
        </body>
        `

        console.log(usuarioItem);
        usuarioList.append(usuarioItem);
    })
}