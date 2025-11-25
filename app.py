from flask import Flask, render_template, request
import pandas as pd
import matplotlib
# Configuración IMPORTANTE para servidores (evita errores de pantalla)
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import io
import base64
from scipy import optimize

# --- AQUÍ INICIAMOS LA APP WEB ---
app = Flask(__name__)

# --- FÓRMULA DE ANUALIDAD ANTICIPADA (ESTILO PROFESOR) ---
def funcion_interes(i, v0, a, n, vf_deseado):
    if i == 0: 
        return (v0 + a * n) - vf_deseado
    
    # El aporte gana interés desde el inicio del periodo (Anticipada)
    parte_v0 = v0 * (1 + i)**n
    parte_aportes = a * (((1 + i)**n - 1) / i) * (1 + i) 
    
    monto_calculado = parte_v0 + parte_aportes
    return monto_calculado - vf_deseado

# --- RUTA PRINCIPAL ---
@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    tabla_html = None
    imagen_grafica = None
    error = None

    if request.method == 'POST':
        try:
            v0 = float(request.form['v0'])
            a = float(request.form['aporte'])
            n = int(request.form['periodos'])
            vf = float(request.form['vf'])

            if v0 < 50:
                error = "El depósito inicial debe ser de al menos $50."
            elif a < 5:
                error = "El aporte periódico debe ser de al menos $5."
            else:
                # Calculamos tasa
                tasa = optimize.bisect(funcion_interes, 1e-6, 1, args=(v0, a, n, vf))
                tasa_porcentaje = round(tasa * 100, 4)

                # --- GENERACIÓN DE TABLA (TÍTULOS ORIGINALES) ---
                lista_datos = []
                saldo_actual = v0
                sin_int = v0 
                
                for t in range(1, n + 1):
                    # Lógica del profesor: Sumamos aporte AL INICIO
                    base_calculo = saldo_actual + a
                    
                    # El interés se calcula sobre (Saldo + Aporte)
                    interes = base_calculo * tasa
                    
                    # Saldo final
                    saldo_final = base_calculo + interes
                    
                    # Acumulado sin interés para la gráfica
                    sin_int += a

                    lista_datos.append({
                        'Periodo': t, 
                        'Saldo Inicial': saldo_actual,  # Mostramos lo que había al arrancar el mes
                        'Aporte': a,                    # Mostramos el aporte
                        'Interés': interes,             # Volvemos al nombre "Interés"
                        'Saldo Final': saldo_final      # Volvemos al nombre "Saldo Final"
                    })
                    
                    # El final de este mes es el inicial del siguiente
                    saldo_actual = saldo_final
                
                df = pd.DataFrame(lista_datos)
                
                # HTML
                tabla_html = df.to_html(classes='table table-striped table-hover', 
                                      float_format=lambda x: f"${x:,.2f}", index=False)

                # GRÁFICA
                plt.figure(figsize=(8, 4))
                plt.plot(df['Periodo'], df['Saldo Final'], label='Con Interés Compuesto', color='green')
                plt.plot(df['Periodo'], [v0 + (a * t) for t in df['Periodo']], '--', label='Sin Interés', color='gray')
                plt.title(f'Proyección a {n} periodos')
                plt.xlabel('Periodo')
                plt.ylabel('Monto Acumulado ($)')
                plt.legend()
                plt.grid(True, alpha=0.3)
                
                img = io.BytesIO()
                plt.savefig(img, format='png', bbox_inches='tight')
                img.seek(0)
                imagen_grafica = base64.b64encode(img.getvalue()).decode()
                plt.close()

                resultado = tasa_porcentaje

        except ValueError:
            error = "No es posible alcanzar esa meta con los valores dados."
        except Exception as e:
            error = f"Ocurrió un error: {e}"

    return render_template('index.html', 
                           tasa=resultado, 
                           tabla=tabla_html, 
                           grafica=imagen_grafica, 
                           error=error)

if __name__ == '__main__':
    app.run(debug=True)