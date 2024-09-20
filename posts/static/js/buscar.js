document.addEventListener('DOMContentLoaded', function () {
    const buscarInput = document.getElementById('buscar-input');
    const buscarResultados = document.getElementById('buscar-resultados');
    // si existen los elementos html
    if (!buscarInput || !buscarResultados) {
        console.error('Elementos no encontrados en el DOM.');
        return;
    }

    buscarInput.addEventListener('input', function () {
        const query = buscarInput.value;//almacena cada nuevo valor del buscador
        console.log(`Consulta de búsqueda: ${query}`);// para ver si funciona en consola

        if (query.length === 0) {// si esta vacio no busca nada
            buscarResultados.style.display = 'none';
            buscarResultados.innerHTML = '';
            return;
        }

        fetch(`/buscar/?q=${encodeURIComponent(query)}`)//realiza la solicitud para hacer la busqueda
            .then(response => {
                console.log('Respuesta recibida:', response);
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })

            .then(data => {
                console.log('Datos de búsqueda:', data);
                buscarResultados.style.display = 'block'; //lo hace visible
                buscarResultados.innerHTML = data.results.map(user => `
                    <a href="/profile/${user.id}/">${user.username}</a>
                `).join('');
            })
            .catch(error => {
                console.error('Error:', error); // Mensaje en consola
            });
    });
});
