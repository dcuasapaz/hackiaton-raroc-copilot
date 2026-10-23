import os
import pandas as pd
from engine.raroc_calculator import calculate_client_raroc, simulate_what_if

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/clients_sample.csv")

def run_raroc_analysis(cif_id: int):
    df_data = pd.read_csv(DATA_PATH)
    financial_data = calculate_client_raroc(cif_id, df_data)
    if "error" in financial_data:
        return financial_data, financial_data["error"]
    
    margen_op = financial_data["margen_operacional"]
    costos_op = financial_data["costos_operativos"]
    raroc_val = financial_data["raroc_pct"]
    nombre_cli = financial_data["nombre"]
    
    if raroc_val < 0:
        analysis = (
            f"⚠️ **Diagnóstico de Inteligencia Artificial:**\n\n"
            f"El cliente **{nombre_cli}** presenta un RAROC negativo del **{raroc_val}%**[cite: 2].\n"
            f"- **Causa Principal:** Elevada carga de costos operacionales (${costos_op} USD) "
            f"que absorben el margen financiero y generan un déficit operacional de **${margen_op} USD**.\n\n"
            f"🚀 **Estrategia Recomendada (Next Best Action):**\n"
            f"1. **Migración a canales digitales:** Reducir transacciones físicas en ventanilla para bajar el costo de servir.\n"
            f"2. **Captación de pasivos:** Promover cuentas de ahorro/plazo fijo con tasa del 4.5% para elevar el reconocimiento por FTP[cite: 1, 2]."
        )
    else:
        analysis = (
            f"✅ **Diagnóstico de Inteligencia Artificial:**\n\n"
            f"El cliente **{nombre_cli}** genera un retorno saludable sobre el capital del **{raroc_val}%**[cite: 2].\n"
            f"- **Fortaleza:** Alto rendimiento financiero con un margen operacional positivo de **${margen_op} USD** "
            f"que absorbe holgadamente la Pérdida Esperada de ${financial_data['perdida_esperada']} USD[cite: 1, 2].\n\n"
            f"🚀 **Estrategia Recomendada (Next Best Action):**\n"
            f"1. **Venta Cruzada:** Colocación de créditos de consumo pre-aprobados o tarjetas corporativas[cite: 1, 2].\n"
            f"2. **Fidelización:** Asignación al segmento de Banca Preferencial[cite: 1, 2]."
        )
    
    return financial_data, analysis

def generate_commercial_script(nombre: str, raroc_sim: float, digital_pct: float, deposito: float) -> str:
    """Genera el guion comercial que el asesor puede leerle al cliente."""
    return (
        f"🗣️ **Script Sugerido para el Asesor:**\n\n"
        f"\"Estimado/a {nombre}, analizando su cuenta en Banco Guayaquil, queremos ofrecerle una optimización de sus costos. "
        f"Si realiza el {digital_pct}% de sus operaciones a través de nuestra App Móvil y canaliza un depósito de ahorro de "
        f"${deposito:,.2f} USD al 4.5% de interés, accederá a beneficios preferenciales de tasa y exoneración de comisiones.\""
    )