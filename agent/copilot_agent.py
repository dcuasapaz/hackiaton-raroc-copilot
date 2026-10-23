import os
import pandas as pd
from engine.raroc_calculator import calculate_client_raroc

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/clients_sample.csv")
df_data = pd.read_csv(DATA_PATH)

def run_raroc_analysis(cif_id: int):
    financial_data = calculate_client_raroc(cif_id, df_data)
    if "error" in financial_data:
        return financial_data, financial_data["error"]
    
    # Generación de diagnóstico mock para evitar el error de API
    if financial_data["raroc_pct"] < 0:
        analysis = (
            f"⚠️ **Diagnóstico de Inteligencia Artificial (Modo Demo):**\n\n"
            f"El cliente **{financial_data['nombre']}** presenta un RAROC negativo del **{financial_data['raroc_pct']}%**[cite: 1].\n"
            f"- **Causa Principal:** Altosa costos operacionales (${financial_data['costos_operativos']} USD) y baja captación de fondos[cite: 1].\n\n"
            f"🚀 **Estrategia Recomendada (Next Best Action):**\n"
            f"1. Migración a canales digitales para reducir el costo de servir por transacción[cite: 1].\n"
            f"2. Oferta de cuenta de ahorros/plazo fijo con tasa del 4.5% para mejorar el reconocimiento FTP[cite: 1]."
        )
    else:
        analysis = (
            f"✅ **Diagnóstico de Inteligencia Artificial (Modo Demo):**\n\n"
            f"El cliente **{financial_data['nombre']}** genera un retorno altamente saludable del **{financial_data['raroc_pct']}%**[cite: 1].\n"
            f"- **Fortaleza:** Excelente margen de intereses (${financial_data['margen_intereses']} USD) que cubre holgadamente su pérdida esperada[cite: 1].\n\n"
            f"🚀 **Estrategia Recomendada (Next Best Action):**\n"
            f"1. Ofrecer línea de crédito preferencial o tarjeta Platinum[cite: 1].\n"
            f"2. Fidelización mediante programa de recompensas[cite: 1]."
        )
    
    return financial_data, analysis