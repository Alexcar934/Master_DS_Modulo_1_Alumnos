# ----------------------------------------
# 1. Imports básicos
# ----------------------------------------
import streamlit as st           # framework principal
import pandas as pd              # manipulación de DataFrames
import matplotlib.pyplot as plt  # para crear figuras y ejes
import seaborn as sns            # para gráficos estadísticos

# ----------------------------------------
# 2. Configuración global de la página
# ----------------------------------------
st.set_page_config(
    page_title="🎧 Music Explorer",  # Título en la pestaña del navegador
    layout="wide",                   # “wide” usa todo el ancho de la ventana
    initial_sidebar_state="expanded"# Sidebar abierto al iniciar
)

# ----------------------------------------
# 3. Definimos una función para cargar datos
# ----------------------------------------
@st.cache_data  
def load_data():
    """
    Lee el CSV una vez y guarda el resultado en caché.
    Así evitarás volver a leer el archivo cada vez que muevas un widget.
    """
    return pd.read_csv("data/SpotifyFeatures.csv")

# 4. Llamamos a la función para tener el DataFrame listo
df = load_data()
# ----------------------------------------

# 5. Menú lateral: elige sección
st.sidebar.title("🔀 Navigation")
page = st.sidebar.radio(
    "Go to",                             # Texto arriba de las opciones
    ["Data", "Explore", "Visualizations", "Random Song"]
)

# 6. Separador
st.sidebar.markdown("---")

# 7. Filtros en la barra lateral
st.sidebar.title("⚙️ Filters")

# 7.1 Slider para popularidad mínima
pop_min = st.sidebar.slider(
    "Min Popularity",  # etiqueta
    0,                 # valor mínimo
    100,               # valor máximo
    50                 # valor inicial
)

# 7.2 Selectbox para género
genres = ["All"] + sorted(df["genre"].unique().tolist())
genre = st.sidebar.selectbox("Genre", genres)

# 7.3 Slider para tempo (range)
tempo_range = st.sidebar.slider(
    "Tempo Range (BPM)",
    int(df["tempo"].min()), 
    int(df["tempo"].max()),
    (60, 160)          # tupla (min, max)
)

# 7.4 Checkbox para instrumentalness alto
inst_only = st.sidebar.checkbox("Only Instrumentalness > 0.5")

# 8. Empezamos con todo el DataFrame
df_filtered = df.copy()

# 8.1 Filtramos por popularidad
df_filtered = df_filtered[df_filtered["popularity"] >= pop_min]

# 8.2 Si el usuario eligió un género distinto de "All", filtramos por él
if genre != "All":
    df_filtered = df_filtered[df_filtered["genre"] == genre]

# 8.3 Filtramos por tempo usando la tupla tempo_range
min_tempo, max_tempo = tempo_range
df_filtered = df_filtered[
    (df_filtered["tempo"] >= min_tempo) &
    (df_filtered["tempo"] <= max_tempo)
]

# 8.4 Si la casilla de instrumentalness está marcada, aplicamos ese filtro
if inst_only:
    df_filtered = df_filtered[df_filtered["instrumentalness"] > 0.5]

# 9. Página "Data": mostrar datos crudos
if page == "Data":
    st.header("📊 Raw Data")
    st.write("First 10 rows of your dataset:")
    st.dataframe(df.head(10), use_container_width=True)
    st.write("Columns:", df.columns.tolist())

# 10. Página "Explore": mostrar datos filtrados
elif page == "Explore":
    st.header("⚙️ Explore Filtered Data")
    st.write(f"Showing {len(df_filtered)} tracks after filtering")
    st.dataframe(df_filtered, use_container_width=True)

# 11. Página "Visualizations": gráficos
elif page == "Visualizations":
    st.header("📈 Visualizations")

    # 11.1 Scatter: danceability vs energy
    st.subheader("Danceability 💃 vs Energy ⚡")
    fig1, ax1 = plt.subplots()  # crea figura y ejes
    sns.scatterplot(
        data=df_filtered, x="danceability", y="energy", hue="genre", ax=ax1
    )
    ax1.set_title("Danceability vs Energy")
    ax1.set_xlabel("Danceability")
    ax1.set_ylabel("Energy")
    st.pyplot(fig1)            # renderiza la figura

    # 11.2 Histograma de loudness
    st.subheader("Loudness Distribution (dB)")
    fig2, ax2 = plt.subplots()
    ax2.hist(df_filtered["loudness"], bins=30)
    ax2.set_title("Histogram of Loudness")
    ax2.set_xlabel("Loudness (dB)")
    ax2.set_ylabel("Frequency")
    st.pyplot(fig2)

# 12. Página "Random Song": botón y canción aleatoria
elif page == "Random Song":
    st.header("🎲 Random Song")
    if st.button("Give me a random track"):
        song = df_filtered.sample(1).iloc[0]
        st.markdown(f"**{song['track_name']}** – {song['artist_name']}")
        st.write(f"Genre: {song['genre']}, Popularity: {song['popularity']}")

# 13. Footer: separador y mensaje final
st.markdown("---")


