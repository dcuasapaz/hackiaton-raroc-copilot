import streamlit as st
import pandas as pd
import os
from engine.raroc_calculator import calculate_client_raroc, simulate_what_if, calculate_portfolio_summary
from agent.copilot_agent import run_raroc_analysis, generate_commercial_script

st.set_page_config(page_title="SmartRAROC Copilot", layout="wide")

st.title("🏦 SmartRAROC Copilot & Instant Profitability Engine")
st.caption("Solución Analítica e Inteligencia Artificial para Banco Guayaquil")

# Cargar dataset
DATA_PATH = os.path.join(os.path.dirname(__file__), "data/clients_sample.csv")
df_clients = pd.read_csv(DATA_PATH)

# Definir pestañas para perfiles de usuario
tab_asesor, tab_gerencia = st.tabs(["👤 Vista Asesor Comercial (Atención Individual)", "📊 Vista Alta Gerencia (Análisis de Portafolio)"])

# ==========================================
# PESTAÑA 1: VISTA ASESOR COMERCIAL
# ==========================================
with tab_asesor:
    st.sidebar.header("Selección de Cliente")
    cif_list = df_clients['cif'].tolist()
    cif_input = st.sidebar.selectbox("Seleccione o ingrese el CIF:", options=cif_list, index=1)
    
    metrics, analysis = run_raroc_analysis(cif_input)
    
    if "error" in metrics:
        st.error(metrics["error"])
    else:
        # KPIs principales
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Cliente", metrics["nombre"], delta=metrics["tipo_cliente"])
        col2.metric("Margen Operacional", f"${metrics['margen_operacional']} USD")
        col3.metric("Pérdida Esperada", f"${metrics['perdida_esperada']} USD")
        
        rar_delta = "🟢 Rentable" if metrics["raroc_pct"] > 0 else "🔴 Destruye Valor"
        col4.metric("RAROC / RAR Actual", f"{metrics['raroc_pct']}%", delta=rar_delta)

        st.markdown("---")
        
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            st.markdown("### 📊 Desglose del P&L (USD)")
            df_chart = pd.DataFrame({
                "Concepto": ["Margen Intereses", "Costos Operativos", "Pérdida Esperada", "Margen Ajustado"],
                "Monto": [
                    metrics["margen_intereses"], 
                    -metrics["costos_operativos"], 
                    -metrics["perdida_esperada"], 
                    metrics["margen_operacional"] - metrics["perdida_esperada"]
                ]
            })
            st.bar_chart(df_chart.set_index("Concepto"))

        with col_right:
            st.markdown("### 🤖 Diagnóstico Copilot")
            st.info(analysis)

        st.markdown("---")
        
        # Simulador What-If
        st.markdown("### 🎛️ Simulador de Escenarios (What-If) en Tiempo Real")
        col_sim_in, col_sim_out = st.columns([1, 1])
        
        with col_sim_in:
            migracion_pct = st.slider("Migración a Canales Digitales (%)", min_value=0, max_value=100, value=60, step=10)
            nuevo_deposito = st.number_input("Nuevo Depósito de Ahorro / Plazo Fijo (USD)", min_value=0, value=2000, step=500)
            
            sim_res = simulate_what_if(metrics, migracion_pct, nuevo_deposito)

        with col_sim_out:
            st.markdown("#### Resultado Simulado")
            sc1, sc2 = st.columns(2)
            sc1.metric("Nuevo RAROC Simulado", f"{sim_res['raroc_sim_pct']}%", delta=f"{sim_res['delta_raroc']}% RAROC")
            sc2.metric("Nuevo Margen Operacional", f"${sim_res['margen_operacional_sim']} USD")
            
            # Script de Venta
            script_txt = generate_commercial_script(metrics["nombre"], sim_res["raroc_sim_pct"], migracion_pct, nuevo_deposito)
            st.success(script_txt)

# ==========================================
# PESTAÑA 2: VISTA ALTA GERENCIA (PORTAFOLIO)
# ==========================================
with tab_gerencia:
    st.markdown("### 🏢 Visión Consolidada de Rentabilidad del Portafolio")
    
    df_summary = calculate_portfolio_summary(df_clients)
    
    # KPIs Globales
    tot_clientes = len(df_summary)
    rentables = len(df_summary[df_summary['raroc_pct'] > 0])
    no_rentables = tot_clientes - rentables
    raroc_promedio = round(df_summary['raroc_pct'].mean(), 2)
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Clientes Evaluados", tot_clientes)
    m2.metric("Clientes Generadores de Valor", rentables)
    m3.metric("Clientes Destructores de Valor", no_rentables)
    m4.metric("RAROC Promedio Portafolio", f"{raroc_promedio}%")
    
    st.markdown("---")
    
    g_left, g_right = st.columns([1, 1])
    
    with g_left:
        st.markdown("#### Tabla General de Rentabilidad por Cliente")
        st.dataframe(
            df_summary[['cif', 'nombre', 'tipo_cliente', 'margen_operacional', 'perdida_esperada', 'raroc_pct']],
            use_container_width=True
        )

    with g_right:
        st.markdown("#### Ranking de Fugas de Valor por Costo Transaccional")
        df_top_costos = df_summary.sort_values(by='costos_transaccionales', ascending=False)
        st.bar_chart(df_top_costos.set_index('nombre')['costos_transaccionales'])
        st.caption("Clientes con mayor impacto operativo en canales tradicionales (Ventanilla física).")