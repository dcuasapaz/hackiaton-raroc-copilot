import os
import pandas as pd

# Crear directorio si no existe
os.makedirs("data", exist_ok=True)

# Dataset sintético diseñado para la HackIAtón (Banco Guayaquil)
clients_data = [
    {
        "cif": 1001,
        "nombre": "Corporación Alfa S.A.",
        "tipo_cliente": "Corporativo",
        "cartera_vigente": 250000.0,
        "interes_ganado": 32500.0,
        "costo_ftp": 7500.0,
        "interes_pagado": 2000.0,
        "reconocimiento_ftp": 5100.0,
        "ingresos_comisiones": 4500.0,
        "ingresos_servicios": 3200.0,
        "costos_transaccionales": 1500.0,
        "costos_fuerza_ventas": 1200.0,
        "costos_mantenimiento": 2100.0,
        "costos_indirectos": 900.0,
        "perdida_esperada": 2500.0,
        "capital_requerido": 30000.0
    },
    {
        "cif": 1002,
        "nombre": "Diego Cuasapaz",
        "tipo_cliente": "Persona Natural",
        "cartera_vigente": 2500.0,
        "interes_ganado": 325.0,
        "costo_ftp": 75.0,
        "interes_pagado": 0.0,
        "reconocimiento_ftp": 50.0,
        "ingresos_comisiones": 0.0,
        "ingresos_servicios": 120.0,
        "costos_transaccionales": 550.0,
        "costos_fuerza_ventas": 150.0,
        "costos_mantenimiento": 200.0,
        "costos_indirectos": 100.0,
        "perdida_esperada": 85.0,
        "capital_requerido": 300.0
    },
    {
        "cif": 1003,
        "nombre": "Tech Innovation Ecuador Cía. Ltda.",
        "tipo_cliente": "Pyme",
        "cartera_vigente": 80000.0,
        "interes_ganado": 11200.0,
        "costo_ftp": 2400.0,
        "interes_pagado": 800.0,
        "reconocimiento_ftp": 1800.0,
        "ingresos_comisiones": 1500.0,
        "ingresos_servicios": 900.0,
        "costos_transaccionales": 800.0,
        "costos_fuerza_ventas": 600.0,
        "costos_mantenimiento": 700.0,
        "costos_indirectos": 400.0,
        "perdida_esperada": 1200.0,
        "capital_requerido": 9600.0
    },
    {
        "cif": 1004,
        "nombre": "Comercializadora del Pacífico",
        "tipo_cliente": "Empresarial",
        "cartera_vigente": 500000.0,
        "interes_ganado": 65000.0,
        "costo_ftp": 15000.0,
        "interes_pagado": 12000.0,
        "reconocimiento_ftp": 18000.0,
        "ingresos_comisiones": 12000.0,
        "ingresos_servicios": 8500.0,
        "costos_transaccionales": 4500.0,
        "costos_fuerza_ventas": 3000.0,
        "costos_mantenimiento": 4000.0,
        "costos_indirectos": 2000.0,
        "perdida_esperada": 8000.0,
        "capital_requerido": 60000.0
    },
    {
        "cif": 1005,
        "nombre": "María José Andrade",
        "tipo_cliente": "Persona Natural Preferencial",
        "cartera_vigente": 15000.0,
        "interes_ganado": 1950.0,
        "costo_ftp": 450.0,
        "interes_pagado": 350.0,
        "reconocimiento_ftp": 800.0,
        "ingresos_comisiones": 200.0,
        "ingresos_servicios": 450.0,
        "costos_transaccionales": 120.0,
        "costos_fuerza_ventas": 80.0,
        "costos_mantenimiento": 150.0,
        "costos_indirectos": 90.0,
        "perdida_esperada": 210.0,
        "capital_requerido": 1800.0
    }
]

df = pd.DataFrame(clients_data)
df.to_csv("data/clients_sample.csv", index=False)
print("✅ Archivo 'data/clients_sample.csv' generado exitosamente con 5 registros.")