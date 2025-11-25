from flask import Flask, render_template, request
import pandas as pd
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import io
import base64
from scipy import optimize

app = Flask(__name__)

# --- FÓRMULA CORREGIDA
def funcion_interes(i, v0, a, n, vf_deseado):
    if i == 0: 
        # Si i es 0, es v0 + (n-1) aportes, porque el primero no se hace
        return (v0 + a * (n - 1)) - vf_deseado
    
    # 1. El Valor Inicial crece por n periodos
    parte_v0 = v0 * (1 + i)**n
    
    # 2. Los aportes son UNA MENOS (n - 1) porque en la semana 1 no hubo aporte.
    #    Siguen siendo "anticipados" (generan interés en su periodo), 
    #    por eso multiplicamos por (1+i) al final.
    periodos_aportes = n - 1
    if periodos_aportes > 0:
        parte_aportes = a * (((1 + i)**periodos_aportes - 1) / i) * (1 + i)
    else:
        parte_aportes = 0
    
    monto_calculado = parte_v0 + parte_aportes
    return monto_calculado - vf_deseado


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

                # --- TABLA (Mantenemos la lógica visual que ya arreglamos) ---
                lista_datos = []
                saldo_actual = v0
                sin_int = v0 
                
                for t in range(1, n + 1):
                    # Semana 1: Aporte 0. Semana 2 en adelante: Aporte A.
                    if t == 1:
                        aporte_real = 0
                    else:
                        aporte_real = a
                    
                    # Lógica Anticipada: Sumamos aporte antes de calcular interés
                    base_calculo = saldo_actual + aporte_real
                    
                    interes = base_calculo * tasa
                    saldo_final = base_calculo + interes
                    
                    sin_int += aporte_real

                    lista_datos.append({
                        'Periodo': t, 
                        'Saldo Inicial': saldo_actual,
                        'Aporte': a if t > 1 else 0, # Visualmente mostramos 0 en la primera
                        'Interés': interes,
                        'Saldo Final': saldo_final
                    })
                    saldo_actual = saldo_final
                
                df = pd.DataFrame(lista_datos)
                tabla_html = df.to_html(classes='table table-striped table-hover', 
                                      float_format=lambda x: f"${x:,.2f}", index=False)

                # GRÁFICA
                plt.figure(figsize=(8, 4))
                plt.plot(df['Periodo'], df['Saldo Final'], label='Con Interés Compuesto', color='green')
                plt.plot(df['Periodo'], [v0 + (a * (t-1) if t>0 else 0) for t in df['Periodo']], '--', label='Sin Interés', color='gray')
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