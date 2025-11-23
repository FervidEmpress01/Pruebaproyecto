import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize

# Definicion de la función de interés

def funcion_interes(i, v0, a, n, vf_deseado):
    # Función objetivo para encontrar el interés
    if i == 0: 
        return (v0 + a * n) - vf_deseado
    monto_calculado = (v0 * (1 + i)**n) + (a * (((1 + i)**n - 1) / i))
    return monto_calculado - vf_deseado

def generar_reportes(v0, a, n, tasa, nombre_archivo="grafica.png"):

    # Genera la tabla y guarda la imagen de la gráfica
    
    # Generar Tabla 
    lista_datos = []
    saldo_actual = v0
    sin_interes = v0
    
    for t in range(1, n + 1):
        interes_ganado = saldo_actual * tasa
        saldo_final = saldo_actual + interes_ganado + a
        sin_interes += a
        
        lista_datos.append({
            'Periodo': t,
            'Saldo Inicial': saldo_actual,
            'Interés Ganado': interes_ganado,
            'Aporte': a,
            'Saldo Final': saldo_final,
            'Sin Interés': sin_interes
        })
        saldo_actual = saldo_final

    df = pd.DataFrame(lista_datos)
    
    # Exportar a HTML
    html = df.to_html(classes='table table-striped', index=False, float_format=lambda x: '${:,.2f}'.format(x))
    with open("tabla_resultados.html", "w") as f:
        f.write(html)
        
    # Generar Gráfica 
    plt.figure(figsize=(10, 6))
    plt.plot(df['Periodo'], df['Saldo Final'], 'g-o', label='Con Interés')
    plt.plot(df['Periodo'], df['Sin Interés'], 'k--', label='Sin Interés')
    plt.title(f'Proyección de Ahorro ({n} periodos)')
    plt.xlabel('Periodo')
    plt.ylabel('Monto ($)')
    plt.legend()
    plt.grid(True)
    plt.savefig(nombre_archivo)
    plt.close() # Cierra la figura para liberar memoria
    
    return df

# --- 2. BLOQUE PRINCIPAL (EJECUCIÓN) ---

if __name__ == "__main__":
    print("--- CALCULADORA DE INTERÉS REAL ---")
    
    # Aquí podrías cambiar estos valores por inputs: float(input("Ingrese monto..."))
    V0 = 1000.0
    A = 100.0
    N = 12
    VF = 2500.0
    
    print("Calculando...")
    inicio = time.time()
    
    try:
        # Lógica de Scipy
        tasa_periodica = optimize.bisect(funcion_interes, 1e-6, 1.0, args=(V0, A, N, VF))
        tiempo_total = time.time() - inicio
        
        # Resultados
        print(f"\nResultados encontrados en {tiempo_total:.6f} segundos.")
        print(f"Tasa periódica necesaria: {tasa_periodica * 100:.4f}%")
        
        # Generar archivos
        df_resultados = generar_reportes(V0, A, N, tasa_periodica)
        print("-> Se ha generado 'tabla_resultados.html' y 'grafica.png'")
        
    except ValueError:
        print("Error: No es posible alcanzar esa meta con los valores dados.")