# Escuela Politécnica Nacional  
# Facultad de Ingeniería en Sistemas  
# Carrera de Computación

# Informe del Proyecto  
## Calculadora de Ahorro con Interés Compuesto y Aportes Periódicos

---

## 1. Introducción
Este informe presenta el desarrollo de una calculadora financiera solicitada por un banco para analizar escenarios de ahorro y estudiar cómo varía el capital con el paso del tiempo. La herramienta implementada permite trabajar con depósitos iniciales, aportes periódicos y distintos tipos de periodicidad, lo que resulta útil para estudiar estrategias de inversión o ahorro a mediano y largo plazo.

El banco estableció dos reglas mínimas para el funcionamiento del programa:
- Un depósito inicial de al menos **50 dólares**.  
- Aportes periódicos de al menos **5 dólares**.

El crecimiento del dinero sigue el principio del interés compuesto, cuya fórmula base proporcionada por los técnicos del banco es:

$$
V_f = V_0(1 + i)^n
$$

donde:
- $V_f$ es el valor final,  
- $V_0$ el depósito inicial,  
- $i$ la tasa de interés por periodo,  
- $n$ la cantidad de periodos.

Sin embargo, esta fórmula solo describe el crecimiento del depósito inicial. El banco necesitaba integrar los aportes periódicos en el cálculo, y ese fue el principal reto. Para ilustrar la situación, los técnicos compartieron un ejemplo con depósito inicial de 100 USD, aportes semanales de 5 USD y tasa anual del 8 %, cuya tabla parcial luce así:

| Semana | Aporte ($) | Capital ($) | Ganancia ($) | Total ($) |
|--------|-----------:|-------------:|--------------:|-----------:|
| 1      | 100        | 100.00       | 0.15          | 100.15     |
| 2      | 5          | 105.15       | 0.16          | 105.31     |
| 3      | 5          | 110.31       | 0.17          | 110.48     |
| 4      | 5          | 115.48       | 0.18          | 115.66     |
| ...    | ...        | ...          | ...           | ...        |
| 52     | 5          | 373.22       | 0.57          | 373.79     |

A partir de este ejemplo se diseñó un sistema flexible capaz de adaptarse si el banco cambia de opinión sobre la periodicidad (semanal, mensual, bimestral o trimestral) y permitir tanto cálculos directos como el cálculo inverso de la tasa requerida.

---

## 2. Requerimientos funcionales (implementados)

- Permitir depósito inicial y aportes periódicos con validaciones de mínimos.  
- Soporte de periodicidad configurable: **semanal**, **mensual**, **bimestral** y **trimestral**.  
- Cálculo del valor final con aportes **anticipados** o **vencidos**.  
- Cálculo automático de la **tasa necesaria** para alcanzar un valor final deseado.  
- Tabla detallada del cálculo por periodo: aporte, capital previo, interés, total acumulado.  
- Generación de una **gráfica** de la evolución del capital.  
- Interfaz gráfica en html para ingreso de parámetros.  
- Implementación del método de **bisección** cuando se requiere hallar la tasa.  

---

## 3. Desarrollo matemático

### 3.1 Conversión de tasas y periodos
Para una tasa anual $r$, si los aportes se realizan $m$ veces al año, la tasa por periodo es:

$$
i = \frac{r}{m}
$$

y el número total de periodos:

$$
n = m \cdot T
$$

donde $T$ es el tiempo en años.

Periodicidades utilizadas:
- Semanal: $m = 52$  
- Mensual: $m = 12$  
- Bimestral: $m = 6$  
- Trimestral: $m = 4$

---

### 3.2 Fórmula del valor final con aportes periódicos (aportes anticipados)

Para aportes **anticipados** (se suman al inicio del periodo), el valor final es:

$$
V_f = V_0(1 + i)^n + A \cdot \left(\frac{(1 + i)^{n-1} - 1}{i}\right)(1 + i)
$$

donde:
- $V_0$ es el depósito inicial,
- $A$ es el aporte periódico,
- $i$ es la tasa por periodo,
- $n$ el número total de periodos.

Si los aportes son **vencidos**, la contribución es:

$$
A \left(\frac{(1 + i)^n - 1}{i}\right)
$$

---

### 3.3 Cálculo de la tasa requerida

Cuando se desea una tasa que permita alcanzar un valor final objetivo $V_f$, se define:

$$
f(i) = V_0(1 + i)^n + A\left(\frac{(1 + i)^{n-1}-1}{i}\right)(1+i) - V_f
$$

La tasa se obtiene buscando la raíz de $f(i)$ mediante el método de **bisección**, controlando la tolerancia del error.

---

## 4. Implementación 

- Lenguaje: **Python 3**.  
- GUI: **Tkinter**, con campos para depósitos, aportes, periodicidad, duración y tasa conocida o desconocida.  
- Métodos numéricos: implementación propia de bisección para evitar dependencias adicionales.  
- Tabla: generada con listas y renderizada en la GUI o exportable a CSV.  
- Gráfica: generada con Matplotlib.  
- Validaciones: mínimos, tipos de datos, coherencia entre valores ingresados.  

---

## 5. Ejemplo de tabla generada

| Periodo | Aporte ($) | Capital antes ($) | Interés ($) | Total ($) |
|--------:|-----------:|------------------:|------------:|----------:|
| 1       | 0          | 100.00            | 0.15        | 100.15    |
| 2       | 5          | 105.15            | 0.16        | 105.31    |
| 3       | 5          | 110.31            | 0.17        | 110.48    |
| ...     | ...        | ...               | ...         | ...       |

---

## 6. Análisis de complejidad y recursos

### 6.1 Complejidad temporal
- Método de bisección:  

$$
\mathcal{O}\!\left(\log\!\left(\frac{1}{\varepsilon}\right)\right)
$$

- Generación de tabla:  

$$
\mathcal{O}(n)
$$

- Gráfica:  

$$
\mathcal{O}(n)
$$


### 6.2 Complejidad espacial
- Tabla completa:  
  $$
  \mathcal{O}(n)
  $$  

### 6.3 Recursos computacionales
- CPU: operaciones ligeras, apropiado para equipos modestos.  
- Memoria: uso lineal según número de periodos.  
- I/O: exportación a CSV y generación de gráfica en PNG.  

---

## 7. Uso de la aplicación (procedimiento)

1. Abrir la interfaz gráfica de html en el siguiente link.  
2. Ingresar depósito inicial (mínimo 50).  
3. Ingresar aporte periódico (mínimo 5).  
4. Seleccionar periodicidad: semanal, mensual, bimestral o trimestral.  
5. Especificar duración.  
6. Elegir si se desea calcular la tasa o usar una tasa conocida.  
7. Seleccionar si los aportes son anticipados o vencidos.  
8. Presionar **Calcular**.  
9. Revisar la tabla y la gráfica generada.  

---

## 8. Resultados y validación

El programa fue probado con distintos casos:  
- Escenarios con tasa alta y periodos largos.  
- Casos límite con tasa baja y aportes mínimos.  
- Comparación con cálculos manuales para comprobar consistencia.  

Los resultados mostraron que el sistema replica correctamente el ejemplo proporcionado por el banco y permite ampliar los escenarios manteniendo precisión y estabilidad en el cálculo.

