document.addEventListener('DOMContentLoaded', () => {
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

    // Manejo del formulario (survey.html)
    const form = document.getElementById('formulario');
    const recommendationDiv = document.getElementById('recommendation');

    if (form && recommendationDiv) {
        // Animación de desvanecimiento para el formulario
        form.style.opacity = 0;
        let formOpacity = 0;
        const formFadeIn = setInterval(() => {
            if (formOpacity >= 1) {
                clearInterval(formFadeIn);
            }
            form.style.opacity = formOpacity;
            formOpacity += 0.05;
        }, 50);

        // Mapeo de emociones a géneros de TMDb
        const genreMap = {
            feliz: [35, 16], // Comedia, Animación
            triste: [18, 10749], // Drama, Romance
            romántico: [10749, 18], // Romance, Drama
            emocionado: [28, 12, 53] // Acción, Aventura, Suspenso
        };

        // Mapeo de géneros del formulario a IDs de TMDb
        const formGenreMap = {
            animación: 16,
            romance: 10749,
            suspenso: 53,
            musical: 10402
        };

        // Clave de la API de TMDb
        const apiKey = 'YOUR_API_KEY'; // ¡Reemplaza con tu clave de API!
        const baseUrl = 'https://api.themoviedb.org/3';
        const imageBaseUrl = 'https://image.tmdb.org/t/p/w500';

        // Función para obtener recomendaciones
        async function getRecommendations(emocion, tipo, genero, duracion) {
            const genreId = formGenreMap[genero] || genreMap[emocion][0];
            const endpoint = tipo === 'pelicula' ? '/discover/movie' : '/discover/tv';
            const url = `${baseUrl}${endpoint}?api_key=${apiKey}&with_genres=${genreId}&language=es-MX&sort_by=popularity.desc`;

            try {
                const response = await fetch(url);
                if (!response.ok) {
                    throw new Error('Error en la solicitud a la API');
                }
                const data = await response.json();
                let results = data.results.slice(0, 5); // Limitar a 5 resultados

                // Filtrar por duración (solo para películas)
                if (tipo === 'pelicula' && duracion === '1-2h') {
                    results = results.filter(async (movie) => {
                        const details = await fetch(`${baseUrl}/movie/${movie.id}?api_key=${apiKey}&language=es-MX`);
                        const movieData = await details.json();
                        return movieData.runtime >= 60 && movieData.runtime <= 120;
                    });
                }

                return results;
            } catch (error) {
                console.error('Error:', error);
                return [];
            }
        }

        // Función para mostrar recomendaciones
        function displayRecommendations(movies) {
            recommendationDiv.innerHTML = '';
            if (movies.length === 0) {
                recommendationDiv.textContent = 'No se encontraron recomendaciones. Intenta de nuevo.';
                recommendationDiv.style.display = 'block';
                return;
            }

            movies.forEach((movie) => {
                const movieCard = document.createElement('div');
                movieCard.classList.add('movie-card');
                const title = movie.title || movie.name;
                const posterPath = movie.poster_path ? `${imageBaseUrl}${movie.poster_path}` : 'https://via.placeholder.com/200x300?text=Sin+Poster';
                movieCard.innerHTML = `
                    <img src="${posterPath}" alt="${title}">
                    <h3>${title}</h3>
                    <p>${movie.overview || 'Sin descripción disponible'}</p>
                `;
                recommendationDiv.appendChild(movieCard);
            });
            recommendationDiv.style.display = 'flex';
        }

        // Manejo del envío del formulario
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const emocion = document.getElementById('emocion').value;
            const tipo = document.getElementById('tipo').value;
            const genero = document.getElementById('genero').value;
            const duracion = document.getElementById('duracion').value;

            // Validación
            if (!emocion || !tipo || !genero || !duracion) {
                recommendationDiv.textContent = 'Por favor, completa todas las opciones.';
                recommendationDiv.style.display = 'block';
                return;
            }

            recommendationDiv.textContent = 'Buscando recomendaciones...';
            recommendationDiv.style.display = 'block';

            const movies = await getRecommendations(emocion, tipo, genero, duracion);
            displayRecommendations(movies);
        });
    }
});