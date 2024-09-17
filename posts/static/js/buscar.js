document.addEventListener('DOMContentLoaded', function() {
    const buscarInput = document.getElementById('buscar-input');
    const buscarResultados = document.getElementById('buscar-resultados');

    if (!buscarInput || !buscarResultados) {
        console.error('Elementos no encontrados en el DOM.');
        return;
    }

    buscarInput.addEventListener('input', function() {
        const query = buscarInput.value;
        console.log(`Consulta de búsqueda: ${query}`); // Mensaje para depuración

        if (query.length === 0) {
            buscarResultados.style.display = 'none';
            buscarResultados.innerHTML = '';
            return;
        }

        fetch(`/buscar/?q=${encodeURIComponent(query)}`)
            .then(response => {
                console.log('Respuesta recibida:', response); // Mensaje para depuración
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Datos de búsqueda:', data); // Mensaje para depuración
                buscarResultados.style.display = 'block';
                buscarResultados.innerHTML = data.results.map(user => `
                    <a href="/profile/${user.id}/">${user.username}</a>
                `).join('');
            })
            .catch(error => {
                console.error('Error:', error); // Mensaje para depuración
            });
    });
});
