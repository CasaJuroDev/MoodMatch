import pandas as pd
import numpy as np
import json

# Read the CSV file
df = pd.read_csv("Nuevo_DataSet.csv", encoding='utf-8')

# Clean the data
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["gross"] = pd.to_numeric(df["gross"], errors="coerce")
df = df.dropna(subset=["name", "score", "gross", "released"])

print(f"Total rows after cleaning: {len(df)}")
print(f"Rows for 1980: {len(df[df['year'] == 1980])}")

# Filter for 1980 (based on the dataset's focus)
df_1980 = df[df["year"] == 1980]

# Get top 5 highest-rated and top 5 highest-grossing movies
top_rated = df_1980.nlargest(5, "score")[["name", "released", "score", "gross", "genre"]]
top_grossing = df_1980.nlargest(5, "gross")[["name", "released", "score", "gross", "genre"]]

print(f"Top rated movies:\n{top_rated}")
print(f"Top grossing movies:\n{top_grossing}")

# Format revenue
def format_revenue(value):
    if np.isnan(value):
        return "N/A"
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f}B"
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    else:
        return f"{value / 1_000:.1f}K"
    return str(value)  # Fallback

top_rated["gross"] = top_rated["gross"].apply(format_revenue)
top_grossing["gross"] = top_grossing["gross"].apply(format_revenue)

# Generate HTML tables
def df_to_html_table(df, title):
    html = f"<h2>{title}</h2>\n"
    html += "<table class='movie-table'>\n"
    html += "<tr><th>Nombre</th><th>Fecha de Estreno</th><th>Puntuación</th><th>Ingresos</th><th>Género</th></tr>\n"
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

# Generate chart data for top rated (bar chart)
bar_chart_id = "barChart"
bar_chart_data = {
    "type": "bar",
    "data": {
        "labels": top_rated["name"].tolist(),
        "datasets": [{
            "label": "Puntuación",
            "data": top_rated["score"].tolist(),
            "backgroundColor": ["#FF6F3C", "#FFC107", "#FF8F5C", "#FFAB91", "#FFD54F"],
            "borderColor": ["#FF4500", "#FFCA28", "#FF7043", "#FF8A65", "#FFB300"],
            "borderWidth": 1
        }]
    },
    "options": {
        "scales": {
            "y": {
                "beginAtZero": True,
                "title": {"display": True, "text": "Puntuación"}
            },
            "x": {
                "title": {"display": True, "text": "Películas"}
            }
        },
        "plugins": {
            "legend": {"position": "top"},
            "title": {"display": True, "text": "Top 5 Películas Mejor Puntuadas (1980)"}
        }
    }
}

# Generate chart data for top grossing (pie chart)
pie_chart_id = "pieChart"
pie_chart_data = {
    "type": "pie",
    "data": {
        "labels": top_grossing["name"].tolist(),
        "datasets": [{
            "label": "Ingresos",
            "data": [float(g.replace('M', '').replace('B', 'e9').replace('K', 'e3')) if isinstance(g, str) and g != "N/A" else 0 for g in top_grossing["gross"]],
            "backgroundColor": ["#FF6F3C", "#FFC107", "#FF8F5C", "#FFAB91", "#FFD54F"],
            "borderColor": ["#FF4500", "#FFCA28", "#FF7043", "#FF8A65", "#FFB300"],
            "borderWidth": 1
        }]
    },
    "options": {
        "plugins": {
            "legend": {"position": "right"},
            "title": {"display": True, "text": "Top 5 Películas por Ingresos (1980)"}
        }
    }
}

# Combine HTML content with tables and charts
html_content = df_to_html_table(top_rated, "Top 5 Películas Mejor Puntuadas (1980)") + "\n"
html_content += df_to_html_table(top_grossing, "Top 5 Películas Más Vistas por Ingresos (1980)") + "\n"
html_content += "<h2>Gráficos</h2>\n"
html_content += f"<canvas id='{bar_chart_id}' style='width: 100%; height: 400px; margin-bottom: 20px;'></canvas>\n"
html_content += f"<script>var {bar_chart_id}Data = {json.dumps(bar_chart_data)};</script>\n"
html_content += f"<canvas id='{pie_chart_id}' style='width: 100%; height: 400px;'></canvas>\n"
html_content += f"<script>var {pie_chart_id}Data = {json.dumps(pie_chart_data)};</script>\n"

# Add a debug message if content is empty
if not html_content.strip():
    html_content = "<p>¡Error: No se generó contenido! Verifica los datos.</p>"

print(f"HTML content length: {len(html_content)}")  # Depuración para verificar si hay contenido

# Generate JavaScript separately to avoid f-string issues
javascript_code = """
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            // Create bar chart
            const barCtx = document.getElementById('barChart').getContext('2d');
            new Chart(barCtx, barChartData);

            // Create pie chart
            const pieCtx = document.getElementById('pieChart').getContext('2d');
            new Chart(pieCtx, pieChartData);
        });
    </script>
"""

# Add navigation and structure for about.html with Chart.js
html_template = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Información</title>
    <link rel="stylesheet" href="./style.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <nav class="navbar">
        <div class="navbar-logo">
            <img src="./image/logo.png" alt="Logo" class="logo-nav">
        </div>
        <ul class="navbar-links">
            <li><a href="index.html" class="navbar-link">INICIO</a></li>
            <li><a href="form.html" class="navbar-link">FORMULARIO</a></li>
            <li><a href="about.html" class="navbar-link">INFORMACIÓN</a></li>
        </ul>
    </nav>
    <div class="container">
        <h2>Acerca de las Películas</h2>
        <p>A continuación, se presentan las películas mejor puntuadas y las más vistas (según ingresos) de nuestra base de datos.</p>
        <div id="movie-data">
            {html_content}
        </div>
    </div>
    {javascript_code}
</body>
</html>
"""

# Save to about.html
with open("about.html", "w", encoding="utf-8") as f:
    f.write(html_template)

print("HTML file 'about.html' has been generated successfully.")