import streamlit as st
import pandas as pd
from engine.raroc_calculator import calculate_client_raroc
from agent.copilot_agent import run_raroc_analysis

st.set_page_config(page_title="SmartRAROC Copilot", layout="wide")

st.title("🏦 SmartRAROC Copilot & Instant Profitability Engine")
st.subheader("Decisiones Financieras Impulsadas por IA")

st.sidebar.header("Selección de Cliente")
cif_input = st.sidebar.number_input("Ingrese el código del cliente:", value=1002, step=1)
btn_analyze = st.sidebar.button("Analizar Rentabilidad", type="primary")

if btn_analyze:
    with st.spinner("Procesando datos financieros y ejecutando evaluación de IA..."):
        metrics, analysis = run_raroc_analysis(cif_input)
        
        if "error" in metrics:
            st.error(metrics["error"])
        else:
            # Sección de KPIs
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Cliente", metrics["nombre"])
            col2.metric("Margen Operacional", f"${metrics['margen_operacional']} USD")
            col3.metric("Pérdida Esperada", f"${metrics['perdida_esperada']} USD")
            
            rar_color = "green" if metrics["raroc_pct"] > 10 else "red"
            col4.metric("RAROC / RAR", f"{metrics['raroc_pct']}%")

            st.markdown("---")
            
            # Gráficos y Detalles Financieros
            col_left, col_right = st.columns([1, 1])
            
            with col_left:
                st.markdown("### 📊 Desglose del P&L (USD)")
                df_chart = pd.DataFrame({
                    "Concepto": ["Margen Intereses", "Costos Operativos", "Pérdida Esperada", "Margen Ajustado"],
                    "Monto": [metrics["margen_intereses"], -metrics["costos_operativos"], -metrics["perdida_esperada"], metrics["margen_operacional"] - metrics["perdida_esperada"]]
                })
                st.bar_chart(df_chart.set_index("Concepto"))

            with col_right:
                st.markdown("### 🤖 Diagnóstico & Next Best Action (Copilot)")
                st.info(analysis)