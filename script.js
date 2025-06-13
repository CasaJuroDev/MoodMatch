document.addEventListener('DOMContentLoaded', () => {
    // Configuración de la API de TMDb
    const apiKey = '2a6bb1234acd6ffaf34745a0582b761d';
    const baseUrl = 'https://api.themoviedb.org/3';
    const imageBaseUrl = 'https://image.tmdb.org/t/p/w200';

    // Mapeo de emociones a géneros de TMDb
    const genreMap = {
        feliz: [35, 16], // Comedia, Animación
        triste: [18, 10749], // Drama, Romance
        romantico: [10749, 18], // Romance, Drama
        emocionado: [28, 12, 53] // Acción, Aventura, Suspenso
    };

    // Animación para la página de bienvenida (index.html)
    const welcomeMessage = document.getElementById('welcome-message');
    const ctaButton = document.getElementById('cta-button');

    if (welcomeMessage && ctaButton) {
        welcomeMessage.style.opacity = 0;
        let opacity = 0;
        const fadeIn = setInterval(() => {
            if (opacity >= 1) {
                clearInterval(fadeIn);
            }
            welcomeMessage.style.opacity = opacity;
            opacity += 0.05;
        }, 50);

        ctaButton.addEventListener('click', () => {
            ctaButton.style.transform = 'scale(0.95)';
            setTimeout(() => {
                ctaButton.style.transform = 'scale(1)';
            }, 100);
        });
    }

    // Manejo del formulario (form.html)
    const form = document.getElementById('formulario');
    if (form) {
        // Animación de desvanecimiento del formulario
        form.style.opacity = 0;
        let formOpacity = 0;
        const formFadeIn = setInterval(() => {
            if (formOpacity >= 1) {
                clearInterval(formFadeIn);
            }
            form.style.opacity = formOpacity;
            formOpacity += 0.05;
        }, 50);
    }

    // Manejo de recomendaciones (recommendations.html)
    const recommendationDiv = document.getElementById('recommendation');
    if (recommendationDiv) {
        // Obtener parámetros de la URL
        const urlParams = new URLSearchParams(window.location.search);
        const emocion = urlParams.get('emocion')?.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
        const tipo = urlParams.get('tipo')?.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
        const genero = urlParams.get('genero')?.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
        const duracion = urlParams.get('duracion')?.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');

        // Validación
        if (!emocion || !tipo || !genero || !duracion) {
            recommendationDiv.textContent = 'Error: Por favor, completa todos los campos en el formulario.';
            recommendationDiv.style.display = 'block';
            console.error('Parámetros faltantes:', { emocion, tipo, genero, duracion });
            return;
        }

        recommendationDiv.textContent = 'Buscando recomendaciones...';
        recommendationDiv.style.display = 'block';

        // Obtener y mostrar recomendaciones
        obtenerRecomendaciones(emocion, tipo, genero, duracion)
            .then(recomendaciones => {
                console.log('Recomendaciones recibidas:', recomendaciones);
                mostrarRecomendaciones(recomendaciones);
            })
            .catch(error => {
                recommendationDiv.textContent = `Error al obtener recomendaciones: ${error.message} (Revisa la consola para más detalles).`;
                recommendationDiv.style.display = 'block';
                console.error('Error en obtenerRecomendaciones:', error);
            });
    }

    // Mapeo de géneros del formulario a IDs de TMDb
    function obtenerIdGenero(genero) {
        const generos = {
            animacion: 16,
            romance: 10749,
            suspenso: 53,
            musical: 10402
        };
        return generos[genero];
    }

    // Mapeo de tipo (película o serie)
    function obtenerIdTipo(tipo) {
        return tipo === 'serie' ? 'tv' : 'movie';
    }

    // Filtro de duración
    function obtenerFiltroDuracion(duracion) {
        if (duracion === '1-2h') {
            return '&with_runtime.gte=60&with_runtime.lte=120';
        } else if (duracion === 'maraton') {
            return '&with_runtime.gte=120';
        }
        return '';
    }

    // Emoción (sin transformación)
    function obtenerIdEmocion(emocion) {
        return emocion;
    }

    // Función para obtener recomendaciones
    async function obtenerRecomendaciones(emocion, tipo, genero, duracion) {
        try {
            const genreId = obtenerIdGenero(genero) || genreMap[emocion]?.[0];
            const tipoId = obtenerIdTipo(tipo);
            const duracionFilter = obtenerFiltroDuracion(duracion);

            if (!genreId || !tipoId) {
                throw new Error('Parámetros inválidos para género o tipo');
            }

            const url = `${baseUrl}/discover/${tipoId}?api_key=${apiKey}&with_genres=${genreId}&language=es-MX&sort_by=popularity.desc${duracionFilter}`;
            console.log('URL de la API:', url);

            const response = await fetch(url);
            console.log('Estado de la respuesta:', response.status, response.statusText);
            if (!response.ok) {
                throw new Error(`Error HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            console.log('Datos de la API:', data);
            return data.results ? data.results.slice(0, 10) : [];
        } catch (error) {
            console.error('Error en la solicitud a la API:', error);
            throw error;
        }
    }

    // Función para mostrar recomendaciones
    function mostrarRecomendaciones(recomendaciones) {
        recommendationDiv.innerHTML = '';
        if (!recomendaciones || recomendaciones.length === 0) {
            recommendationDiv.textContent = 'No se encontraron recomendaciones. Intenta con otras opciones.';
            recommendationDiv.style.display = 'block';
            return;
        }

        recomendaciones.forEach((item) => {
            const movieCard = document.createElement('div');
            movieCard.classList.add('movie-card');
            const title = item.title || item.name || 'Sin título';
            const poster = item.poster_path
                ? `${imageBaseUrl}${item.poster_path}`
                : 'https://via.placeholder.com/200x300?text=Sin+Poster';
            movieCard.innerHTML = `
                <img src="${poster}" alt="${title}">
                <h3>${title}</h3>
                <p>${item.overview || 'Sin descripción disponible'}</p>
            `;
            recommendationDiv.appendChild(movieCard);
        });
        recommendationDiv.style.display = 'flex';
    }
});