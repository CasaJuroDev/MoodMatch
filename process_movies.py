# Importamos las herramientas necesarias 
import pandas as pd  
import numpy as np 
import json         

# Leemos el archivo CSV 
df = pd.read_csv("Nuevo_DataSet.csv", encoding='utf-8')

# Limpiamos los datos 
df["score"] = pd.to_numeric(df["score"], errors="coerce")  # Convertimos puntuaciones a números
df["gross"] = pd.to_numeric(df["gross"], errors="coerce")  # Convertimos ingresos a números
df = df.dropna(subset=["name", "score", "gross", "released"])  # Borramos filas con datos faltantes

print(f"Total de filas después de limpiar: {len(df)}")  # Contamos cuántas películas quedan
print(f"Filas para 1980: {len(df[df['year'] == 1980])}")  # Contamos solo las de 1980

# Filtramos solo las películas de 1980 
df_1980 = df[df["year"] == 1980]

# Escogemos las 5 mejores puntuadas y las 5 que más dinero ganaron
top_rated = df_1980.nlargest(5, "score")[["name", "released", "score", "gross", "genre"]]
top_grossing = df_1980.nlargest(5, "gross")[["name", "released", "score", "gross", "genre"]]

print(f"Películas mejor puntuadas:\n{top_rated}")
print(f"Películas más taquilleras:\n{top_grossing}")

# Función para formatear los ingresos (como decir "1M" en vez de 1,000,000)
def format_revenue(value):
    if np.isnan(value):  # Si no hay dato, ponemos "N/A"
        return "N/A"
    if value >= 1_000_000_000:  # Si es mucho dinero (miles de millones)
        return f"{value / 1_000_000_000:.1f}B"
    elif value >= 1_000_000:  # Si son millones
        return f"{value / 1_000_000:.1f}M"
    else:  # Si es poco (miles)
        return f"{value / 1_000:.1f}K"

# Aplicamos la función a las tablas
top_rated["gross"] = top_rated["gross"].apply(format_revenue)
top_grossing["gross"] = top_grossing["gross"].apply(format_revenue)

# Función para crear tablas HTML 
def df_to_html_table(df, title):
    html = f"<h2>{title}</h2>\n"  # Título de la tabla
    html += "<table class='movie-table'>\n"
    # Encabezados de la tabla
    html += "<tr><th>Nombre</th><th>Fecha de Estreno</th><th>Puntuación</th><th>Ingresos</th><th>Género</th></tr>\n"
    # Rellenamos con datos de cada película
    for _, row in df.iterrows():
        html += "<tr>\n"
        html += f"<td>{row['name']}</td>\n"
        html += f"<td>{row['released']}</td>\n"
        html += f"<td>{row['score']:.1f}</td>\n"
        html += f"<td>{row['gross']}</td>\n"
        html += f"<td>{row['genre']}</td>\n"
        html += "</tr>\n"
    html += "</table>\n"
    return html

# Preparamos datos para el gráfico de barras (puntuaciones)
bar_chart_data = {
    "type": "bar",
    "data": {
        "labels": top_rated["name"].tolist(),  # Nombres de películas
        "datasets": [{
            "label": "Puntuación",
            "data": top_rated["score"].tolist(),  # Puntuaciones
            "backgroundColor": ["#FF6F3C", "#FFC107", "#FF8F5C", "#FFAB91", "#FFD54F"],  # Colores acordes a la paleta de colores
            "borderColor": ["#FF4500", "#FFCA28", "#FF7043", "#FF8A65", "#FFB300"],
            "borderWidth": 1
        }]
    },
    "options": {
        "scales": {
            "y": {"beginAtZero": True, "title": {"display": True, "text": "Puntuación"}},
            "x": {"title": {"display": True, "text": "Películas"}}
        },
        "plugins": {
            "title": {"display": True, "text": "Top 5 Películas Mejor Puntuadas (1980)"}
        }
    }
}

# Preparamos datos para el gráfico de pastel
pie_chart_data = {
    "type": "pie",
    "data": {
        "labels": top_grossing["name"].tolist(),
        "datasets": [{
            "label": "Ingresos",
            "data": [float(g.replace('M', '').replace('B', 'e9').replace('K', 'e3')) if isinstance(g, str) and g != "N/A" else 0 for g in top_grossing["gross"]],  # Convertimos "1M" a 1000000
            "backgroundColor": ["#FF6F3C", "#FFC107", "#FF8F5C", "#FFAB91", "#FFD54F"],
            "borderWidth": 1
        }]
    },
    "options": {
        "plugins": {
            "title": {"display": True, "text": "Top 5 Películas por Ingresos (1980)"}
        }
    }
}

# Juntamos todo el HTML 
html_content = df_to_html_table(top_rated, "Top 5 Películas Mejor Puntuadas (1980)") + "\n"
html_content += df_to_html_table(top_grossing, "Top 5 Películas Más Vistas por Ingresos (1980)") + "\n"
html_content += "<h2>Gráficos</h2>\n"
html_content += f"<canvas id='barChart' style='width: 100%; height: 400px; margin-bottom: 20px;'></canvas>\n"
html_content += f"<script>var barChartData = {json.dumps(bar_chart_data)};</script>\n"
html_content += f"<canvas id='pieChart' style='width: 100%; height: 400px;'></canvas>\n"
html_content += f"<script>var pieChartData = {json.dumps(pie_chart_data)};</script>\n"

# Creamos el HTML final
html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Información</title>
    <link rel="stylesheet" href="./style.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>  # Usamos una librería para dibujar gráficos
</head>
<body>
    <nav class="navbar">
        <ul>
            <li><a href="index.html">INICIO</a></li>
            <li><a href="form.html">FORMULARIO</a></li>
            <li><a href="about.html">INFORMACIÓN</a></li>
        </ul>
    </nav>
    <div class="container">
        {html_content}
    </div>
    <script>
        // Dibujamos los gráficos cuando la página se cargue
        document.addEventListener('DOMContentLoaded', () => {{
            new Chart(document.getElementById('barChart').getContext('2d'), barChartData);
            new Chart(document.getElementById('pieChart').getContext('2d'), pieChartData);
        }});
    </script>
</body>
</html>
"""

# Guardamos todo en "about.html" 
with open("about.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print("¡Archivo 'about.html' creado con éxito! 🎉")