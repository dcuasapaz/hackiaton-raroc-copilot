import pandas as pd

def calculate_client_raroc(cif_id: int, df_clients: pd.DataFrame) -> dict:
    client = df_clients[df_clients['cif'] == cif_id]
    if client.empty:
        return {"error": f"Cliente con CIF {cif_id} no encontrado."}
    
    row = client.iloc[0]
    
    # 1. Margen de Intereses (NII)
    margen_intereses = (row['interes_ganado'] - row['costo_ftp']) - (row['interes_pagado'] - row['reconocimiento_ftp'])
    
    # 2. Ingresos Operativos Totales
    ingresos_operativos = margen_intereses + row['ingresos_comisiones'] + row['ingresos_servicios']
    
    # 3. Costos Operativos Totales
    costos_operativos = (row['costos_transaccionales'] + row['costos_fuerza_ventas'] + 
                        row['costos_mantenimiento'] + row['costos_indirectos'])
    
    # 4. Margen Operacional
    margen_operacional = ingresos_operativos - costos_operativos
    
    # 5. Margen Ajustado por Riesgo (Deduciendo Pérdida Esperada)
    margen_ajustado_riesgo = margen_operacional - row['perdida_esperada']
    
    # 6. Cálculo RAROC / RAR (%)
    raroc = (margen_ajustado_riesgo / row['capital_requerido']) * 100
    
    return {
        "cif": int(row['cif']),
        "nombre": str(row['nombre']),
        "cartera_vigente": float(row['cartera_vigente']),
        "margen_intereses": round(float(margen_intereses), 2),
        "ingresos_operativos": round(float(ingresos_operativos), 2),
        "costos_operativos": round(float(costos_operativos), 2),
        "margen_operacional": round(float(margen_operacional), 2),
        "perdida_esperada": round(float(row['perdida_esperada']), 2),
        "capital_requerido": round(float(row['capital_requerido']), 2),
        "raroc_pct": round(float(raroc), 2)
    }