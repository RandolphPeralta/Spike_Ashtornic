import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuración de la base de datos PostgreSQL
POSTGRES_CONFIG = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "Yokona@76",
    "port": 5433
}

def connect_postgres():
    """Conectar a la base de datos PostgreSQL."""
    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        return conn
    except Exception as e:
        st.error(f"Error al conectar a PostgreSQL: {e}")
        return None

def fetch_data(conn, table_name):
    """Obtener datos de una tabla específica."""
    try:
        query = f"SELECT * FROM {table_name};"
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Error al obtener datos de {table_name}: {e}")
        return pd.DataFrame()

def main():
    st.title("Dashboard de Análisis Financiero")
    st.markdown("Visualización y análisis de la evolución financiera.")

    # Conectar a PostgreSQL
    conn = connect_postgres()
    if not conn:
        return

    # Obtener datos de las tablas
    declaraciones_renta = fetch_data(conn, "declaraciones_renta")
    informacion_exogena = fetch_data(conn, "informacion_exogena")
    escrituras_publicas = fetch_data(conn, "escrituras_publicas")
    extractos_bancarios = fetch_data(conn, "extractos_bancarios")

    # Cerrar la conexión
    conn.close()

    # --- Comparación Año a Año del Patrimonio Neto ---
    st.header("1. Comparación Año a Año del Patrimonio Neto")
    if not declaraciones_renta.empty:
        fig_patrimonio = px.bar(
            declaraciones_renta,
            x="año",
            y="patrimonio_neto",
            title="Crecimiento del Patrimonio Neto",
            labels={"año": "Año", "patrimonio_neto": "Patrimonio Neto"}
        )
        st.plotly_chart(fig_patrimonio)
    else:
        st.warning("No hay datos de declaraciones de renta para mostrar.")

    # --- Evolución de Ingresos vs. Gastos ---
    st.header("2. Evolución de Ingresos vs. Gastos")
    if not extractos_bancarios.empty:
        fig_ingresos_gastos = go.Figure()
        fig_ingresos_gastos.add_trace(go.Scatter(
            x=extractos_bancarios.index,
            y=extractos_bancarios["total_ingresos"],
            name="Ingresos",
            mode="lines+markers"
        ))
        fig_ingresos_gastos.add_trace(go.Scatter(
            x=extractos_bancarios.index,
            y=extractos_bancarios["total_egresos"],
            name="Gastos",
            mode="lines+markers"
        ))
        fig_ingresos_gastos.update_layout(
            title="Evolución de Ingresos vs. Gastos",
            xaxis_title="Periodo",
            yaxis_title="Monto"
        )
        st.plotly_chart(fig_ingresos_gastos)
    else:
        st.warning("No hay datos de extractos bancarios para mostrar.")

    # --- Distribución del Patrimonio en Propiedades e Inversiones ---
    st.header("3. Distribución del Patrimonio en Propiedades e Inversiones")
    if not declaraciones_renta.empty:
        patrimonio_bruto = declaraciones_renta["patrimonio_bruto"].iloc[0]
        if patrimonio_bruto:
            df_patrimonio = pd.DataFrame(patrimonio_bruto.items(), columns=["Tipo", "Valor"])
            fig_pastel = px.pie(
                df_patrimonio,
                values="Valor",
                names="Tipo",
                title="Distribución del Patrimonio Bruto"
            )
            st.plotly_chart(fig_pastel)
        else:
            st.warning("No hay datos de patrimonio bruto para mostrar.")
    else:
        st.warning("No hay datos de declaraciones de renta para mostrar.")

    # --- Identificación de Posibles Problemas Financieros ---
    st.header("4. Identificación de Posibles Problemas Financieros")
    if not extractos_bancarios.empty:
        deuda_tarjetas = extractos_bancarios["deuda_tarjetas"].iloc[-1]
        saldo_final = extractos_bancarios["saldo_final"].iloc[-1]
        
        st.subheader("Indicadores Clave")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Deuda en Tarjetas de Crédito", f"${deuda_tarjetas:,.2f}")
        with col2:
            st.metric("Saldo Final Disponible", f"${saldo_final:,.2f}")
        
        if deuda_tarjetas > saldo_final:
            st.error("⚠️ Posible sobreendeudamiento: La deuda en tarjetas supera el saldo disponible.")
        else:
            st.success("✅ Situación financiera estable.")
    else:
        st.warning("No hay datos de extractos bancarios para mostrar.")

if __name__ == "__main__":
    main()