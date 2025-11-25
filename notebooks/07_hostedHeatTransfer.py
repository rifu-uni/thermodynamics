# -*- coding: utf-8 -*-
"""

Heat transfer analysis.
Written by Luis Felipe Ramírez.
Hosted on this repository for ease of access.

A few changes were performed by rifusaki to adapt it to local needs.

Original file is located at
    https://colab.research.google.com/drive/1XX_V6w0iw6d1I0G_ThPVQ8gfQx-1gyQq
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path

os.chdir(Path.cwd().parent)
print("Working directory set to:", Path.cwd())

# --- CONFIGURACIÓN INICIAL ---
# Constantes físicas
MASA_AGUA_G = 150.0       # 150 ml de agua = 150 g (aprox)
C_AGUA = 4.186            # Calor específico del agua (J/g°C)
TITULO_INTENTOS = ['1', '2', '3'] # Nombres de las hojas en el Excel

# Crear carpeta para guardar gráficas si no existe
CARPETA_SALIDA = "graficas_lab"
if not os.path.exists(CARPETA_SALIDA):
    os.makedirs(CARPETA_SALIDA)

def analizar_intento(nombre_hoja):
    print(f"\n{'='*20} ANALIZANDO INTENTO {nombre_hoja} {'='*20}")

    # 1. Cargar datos
    try:
        df = pd.read_excel('data/07_heatTransfer/hostedData.xlsx', sheet_name=nombre_hoja)
    except Exception as e:
        print(f"Error leyendo la hoja '{nombre_hoja}': {e}")
        return

    # Asegurarnos de que los nombres de columnas estén limpios
    # Asumo columnas: Tiempo_s, T1 (Frio), T2 (Caliente)
    cols = df.columns
    t_col = cols[0]  # Tiempo
    t1_col = cols[1] # Frio
    t2_col = cols[2] # Caliente

    # Filtrar datos vacíos si los hay
    df = df.dropna()

    # 2. Cálculos de Energía (Q = m * c * deltaT)
    # T1 es Frío (Gana energía), T2 es Caliente (Pierde energía)

    # Temperaturas iniciales
    t1_inicial = df[t1_col].iloc[0]
    t2_inicial = df[t2_col].iloc[0]

    # Delta T acumulado respecto al inicio
    df['DeltaT_Frio'] = df[t1_col] - t1_inicial
    df['DeltaT_Caliente'] = t2_inicial - df[t2_col] # Positivo para facilitar gráfica de magnitud

    # Energía (Joules)
    df['Q_Ganado'] = MASA_AGUA_G * C_AGUA * df['DeltaT_Frio']
    df['Q_Cedido'] = MASA_AGUA_G * C_AGUA * df['DeltaT_Caliente']

    # Diferencia de energía (Pérdidas al ambiente + calor absorbido por el vaso/barra)
    df['Q_Perdido_Sistema'] = df['Q_Cedido'] - df['Q_Ganado']

    # 3. Cálculo de Tasas de Transferencia (dT/dt)
    # Usamos gradiente de numpy que maneja pasos de tiempo irregulares
    gradiente_frio = np.gradient(df[t1_col], df[t_col])
    gradiente_caliente = np.gradient(df[t2_col], df[t_col])

    df['Tasa_Frio'] = gradiente_frio
    df['Tasa_Caliente'] = gradiente_caliente # Será negativa

    # Diferencia de temperatura entre vasos (Driving force)
    df['DeltaT_Vasos'] = df[t2_col] - df[t1_col]

    # --- RESULTADOS NUMÉRICOS PARA CONSOLA ---
    q_ganado_total = df['Q_Ganado'].iloc[-1]
    q_cedido_total = df['Q_Cedido'].iloc[-1]
    eficiencia = (q_ganado_total / q_cedido_total) * 100 if q_cedido_total != 0 else 0

    print(f"--- Resumen Estadístico Intento {nombre_hoja} ---")
    print(f"Temp Inicial Frío: {t1_inicial:.2f} °C | Final: {df[t1_col].iloc[-1]:.2f} °C")
    print(f"Temp Inicial Caliente: {t2_inicial:.2f} °C | Final: {df[t2_col].iloc[-1]:.2f} °C")
    print(f"Energía Total Cedida (Caliente): {q_cedido_total:.2f} J")
    print(f"Energía Total Absorbida (Frío): {q_ganado_total:.2f} J")
    print(f"Energía 'Perdida' (Ambiente/Materiales): {q_cedido_total - q_ganado_total:.2f} J")
    print(f"Eficiencia del sistema (Q_ganado / Q_cedido): {eficiencia:.2f} %")

    # Tasa máxima de enfriamiento
    min_rate = df['Tasa_Caliente'].min()
    print(f"Tasa máxima de enfriamiento: {min_rate:.4f} °C/s (ocurre al inicio)")

    # --- GENERACIÓN DE GRÁFICAS ---

    # Gráfica 1: Perfil de Temperaturas
    plt.figure(figsize=(10, 6))
    plt.plot(df[t_col], df[t2_col], 'r-o', label='Caliente (T2)', markersize=4)
    plt.plot(df[t_col], df[t1_col], 'b-o', label='Frío (T1)', markersize=4)
    plt.title(f'Perfil de Temperatura vs Tiempo - Intento {nombre_hoja}')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Temperatura (°C)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    filename1 = f"perfil_temp_intento_{nombre_hoja}.png"
    plt.savefig(os.path.join(CARPETA_SALIDA, filename1))
    plt.close()
    print(f"Gráfica guardada: {filename1}")

    # Gráfica 2: Calorimetría (Energía)
    plt.figure(figsize=(10, 6))
    plt.plot(df[t_col], df['Q_Cedido'], 'r--', label='Energía Cedida (Caliente)')
    plt.plot(df[t_col], df['Q_Ganado'], 'b-', label='Energía Absorbida (Frío)')
    plt.fill_between(df[t_col], df['Q_Cedido'], df['Q_Ganado'], color='gray', alpha=0.2, label='Pérdidas')
    plt.title(f'Transferencia de Energía Acumulada - Intento {nombre_hoja}')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Energía (Joules)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    filename2 = f"energia_intento_{nombre_hoja}.png"
    plt.savefig(os.path.join(CARPETA_SALIDA, filename2))
    plt.close()
    print(f"Gráfica guardada: {filename2}")

    # Gráfica 3: Tasa de Cambio vs Diferencia de Temp (Ley de Enfriamiento)
    # Filtramos un poco el ruido si es necesario, pero graficamos directo
    plt.figure(figsize=(10, 6))
    plt.scatter(df['DeltaT_Vasos'], -df['Tasa_Caliente'], color='purple', alpha=0.6, s=20)
    plt.title(f'Velocidad de Enfriamiento vs Diferencia de Temperatura - Intento {nombre_hoja}')
    plt.xlabel('Diferencia de Temperatura (T_caliente - T_frio) [°C]')
    plt.ylabel('Tasa de Enfriamiento (-dT/dt) [°C/s]')

    # Añadir linea de tendencia simple para ver linealidad
    z = np.polyfit(df['DeltaT_Vasos'], -df['Tasa_Caliente'], 1)
    p = np.poly1d(z)
    plt.plot(df['DeltaT_Vasos'], p(df['DeltaT_Vasos']), "k--", alpha=0.5, label=f'Tendencia: {z[0]:.4f}x + {z[1]:.4f}')

    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.gca().invert_xaxis() # Invertimos X porque el tiempo avanza mientras la diferencia disminuye
    filename3 = f"tasa_enfriamiento_intento_{nombre_hoja}.png"
    plt.savefig(os.path.join(CARPETA_SALIDA, filename3))
    plt.close()
    print(f"Gráfica guardada: {filename3}")

# --- EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    for hoja in TITULO_INTENTOS:
        analizar_intento(hoja)
    print("\nAnálisis completado. Copia los resultados de arriba.")

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# --- CONFIGURACIÓN INICIAL ---
MASA_AGUA_G = 150.0
C_AGUA = 4.186
TITULO_INTENTOS = ['1', '2']

# --- ERRORES INSTRUMENTALES ---
ERROR_TEMP = 0.1  # Grados Celsius
ERROR_TIEMPO = 0.1 # Segundos

CARPETA_SALIDA = "graficas_lab"
if not os.path.exists(CARPETA_SALIDA):
    os.makedirs(CARPETA_SALIDA)

def analizar_intento_con_error(nombre_hoja):
    print(f"\n{'='*20} ANALIZANDO INTENTO {nombre_hoja} (CON ERRORES) {'='*20}")

    try:
        df = pd.read_excel('datos.xlsx', sheet_name=nombre_hoja)
    except Exception as e:
        print(f"Error leyendo la hoja '{nombre_hoja}': {e}")
        return

    cols = df.columns
    t_col, t1_col, t2_col = cols[0], cols[1], cols[2]
    df = df.dropna()

    # --- CÁLCULOS BÁSICOS ---
    t1_inicial = df[t1_col].iloc[0]
    t2_inicial = df[t2_col].iloc[0]
    t1_final = df[t1_col].iloc[-1]
    t2_final = df[t2_col].iloc[-1]

    # Delta T absolutos
    delta_T_frio = t1_final - t1_inicial
    delta_T_caliente = t2_inicial - t2_final # (Positivo para cálculo de magnitud)

    # Energías
    q_ganado_total = MASA_AGUA_G * C_AGUA * delta_T_frio
    q_cedido_total = MASA_AGUA_G * C_AGUA * delta_T_caliente

    # Eficiencia
    eficiencia = (q_ganado_total / q_cedido_total) * 100 if q_cedido_total != 0 else 0

    # --- PROPAGACIÓN DE ERRORES ---

    # 1. Incertidumbre en Delta T (Resta: sqrt(err1^2 + err2^2))
    # Error instrumental se aplica a T_final y T_inicial
    u_delta_T = np.sqrt(ERROR_TEMP**2 + ERROR_TEMP**2)

    # 2. Incertidumbre en Q (Multiplicación por constantes exactas m y c)
    # u_Q = m * c * u_delta_T
    u_Q = MASA_AGUA_G * C_AGUA * u_delta_T

    # 3. Incertidumbre en Eficiencia (División: Q_in / Q_out)
    # u_eta / eta = sqrt( (u_Q_in/Q_in)^2 + (u_Q_out/Q_out)^2 )
    if q_ganado_total > 0 and q_cedido_total > 0:
        frac_ganado = (u_Q / q_ganado_total)**2
        frac_cedido = (u_Q / q_cedido_total)**2
        u_eficiencia = eficiencia * np.sqrt(frac_ganado + frac_cedido)
    else:
        u_eficiencia = 0

    # --- IMPRESIÓN DE RESULTADOS FORMATEADOS ---
    print(f"--- Datos con Incertidumbre Intento {nombre_hoja} ---")
    print(f"Delta T Frio: {delta_T_frio:.1f} +/- {u_delta_T:.2f} °C")
    print(f"Delta T Caliente: {delta_T_caliente:.1f} +/- {u_delta_T:.2f} °C")
    print("-" * 30)
    # Nota: Imprimimos con varios decimales para que luego podamos redondear bien en LaTeX
    print(f"Energía Cedida (Q_out): {q_cedido_total:.2f} +/- {u_Q:.2f} J")
    print(f"Energía Absorbida (Q_in): {q_ganado_total:.2f} +/- {u_Q:.2f} J")
    print(f"Pérdidas (Q_lost): {q_cedido_total - q_ganado_total:.2f} +/- {np.sqrt(u_Q**2 + u_Q**2):.2f} J")
    print("-" * 30)
    print(f"Eficiencia: {eficiencia:.2f} +/- {u_eficiencia:.2f} %")

    # (Las gráficas se mantienen igual, el código anterior ya las generaba bien,
    # aquí solo nos interesan los números para la tabla)

# --- EJECUCIÓN ---
if __name__ == "__main__":
    for hoja in TITULO_INTENTOS:
        analizar_intento_con_error(hoja)
    print("\nCopia estos resultados para ajustar las cifras significativas en el LaTeX.")