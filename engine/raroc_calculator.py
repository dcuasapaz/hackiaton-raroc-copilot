import pandas as pd

def calculate_client_raroc(cif_id: int, df_clients: pd.DataFrame) -> dict:
    client = df_clients[df_clients['cif'] == cif_id]
    if client.empty:
        return {"error": f"Cliente con CIF {cif_id} no encontrado."}
    
    row = client.iloc[0]
    
    margen_intereses = (row['interes_ganado'] - row['costo_ftp']) - (row['interes_pagado'] - row['reconocimiento_ftp'])
    ingresos_operativos = margen_intereses + row['ingresos_comisiones'] + row['ingresos_servicios']
    costos_operativos = (row['costos_transaccionales'] + row['costos_fuerza_ventas'] + 
                        row['costos_mantenimiento'] + row['costos_indirectos'])
    
    margen_operacional = ingresos_operativos - costos_operativos
    margen_ajustado_riesgo = margen_operacional - row['perdida_esperada']
    raroc = (margen_ajustado_riesgo / row['capital_requerido']) * 100
    
    return {
        "cif": int(row['cif']),
        "nombre": str(row['nombre']),
        "tipo_cliente": str(row['tipo_cliente']),
        "cartera_vigente": float(row['cartera_vigente']),
        "interes_ganado": float(row['interes_ganado']),
        "costo_ftp": float(row['costo_ftp']),
        "interes_pagado": float(row['interes_pagado']),
        "reconocimiento_ftp": float(row['reconocimiento_ftp']),
        "ingresos_comisiones": float(row['ingresos_comisiones']),
        "ingresos_servicios": float(row['ingresos_servicios']),
        "costos_transaccionales": float(row['costos_transaccionales']),
        "costos_operativos": round(float(costos_operativos), 2),
        "margen_intereses": round(float(margen_intereses), 2),
        "ingresos_operativos": round(float(ingresos_operativos), 2),
        "margen_operacional": round(float(margen_operacional), 2),
        "perdida_esperada": round(float(row['perdida_esperada']), 2),
        "capital_requerido": round(float(row['capital_requerido']), 2),
        "raroc_pct": round(float(raroc), 2)
    }

def simulate_what_if(metrics: dict, pct_digital_migration: float, nuevo_deposito_ahorro: float) -> dict:
    """Calcula el escenario de simulación en caliente para el asesor comercial."""
    # Reducción de costos transaccionales por migración a canal digital
    ahorro_transaccional = metrics["costos_transaccionales"] * (pct_digital_migration / 100.0) * 0.8
    costos_operativos_sim = metrics["costos_operativos"] - ahorro_transaccional
    
    # Incremento en reconocimiento FTP por nuevos fondos de ahorro (tasa 4.5%)
    nuevo_reconocimiento_ftp = metrics["reconocimiento_ftp"] + (nuevo_deposito_ahorro * 0.045)
    
    margen_intereses_sim = (metrics['interes_ganado'] - metrics['costo_ftp']) - (metrics['interes_pagado'] - nuevo_reconocimiento_ftp)
    ingresos_operativos_sim = margen_intereses_sim + metrics['ingresos_comisiones'] + metrics['ingresos_servicios']
    
    margen_operacional_sim = ingresos_operativos_sim - costos_operativos_sim
    margen_ajustado_sim = margen_operacional_sim - metrics['perdida_esperada']
    raroc_sim = (margen_ajustado_sim / metrics['capital_requerido']) * 100
    
    return {
        "costos_operativos_sim": round(float(costos_operativos_sim), 2),
        "margen_operacional_sim": round(float(margen_operacional_sim), 2),
        "raroc_sim_pct": round(float(raroc_sim), 2),
        "delta_raroc": round(float(raroc_sim - metrics["raroc_pct"]), 2)
    }

def calculate_portfolio_summary(df_clients: pd.DataFrame) -> pd.DataFrame:
    """Calcula las métricas consolidadas del portafolio completo."""
    results = []
    for _, row in df_clients.iterrows():
        res = calculate_client_raroc(row['cif'], df_clients)
        results.append(res)
    return pd.DataFrame(results)