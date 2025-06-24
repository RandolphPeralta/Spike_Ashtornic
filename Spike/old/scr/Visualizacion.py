import psycopg2
import pandas as pd
import streamlit as st

# Configuración de la base de datos PostgreSQL
POSTGRES_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "Yokona@76",
    "host": "localhost",
    "port": "5433"
}

def fetch_data():
    """Obtiene los datos financieros desde PostgreSQL."""
    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        query = "SELECT id, nombre_archivo, contenido FROM datos_financieros"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Error al obtener los datos: {e}")
        return pd.DataFrame()

# Interfaz de Streamlit
st.title("Dashboard de Análisis Financiero 📊")

df = fetch_data()

if df.empty:
    st.warning("No hay datos disponibles en la base de datos.")
else:
    st.subheader("Vista General de los Datos")
    st.dataframe(df)

    # Opciones de análisis
    archivo_seleccionado = st.selectbox("Selecciona un archivo:", df["nombre_archivo"].unique())

    if archivo_seleccionado:
        datos_filtrados = df[df["nombre_archivo"] == archivo_seleccionado]
        st.subheader(f"Contenido de {archivo_seleccionado}")
        st.write(datos_filtrados["contenido"].values[0])

st.sidebar.header("Opciones de Visualización")
st.sidebar.write("Añadir gráficos personalizados aquí.")

# Ejecutar con: streamlit run Visualizacion.py
