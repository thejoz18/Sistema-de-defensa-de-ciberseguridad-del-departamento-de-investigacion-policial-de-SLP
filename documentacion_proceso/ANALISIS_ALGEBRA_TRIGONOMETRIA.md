# Analisis Algebra y Trigonometria

## Modelado algebraico del trafico digital

En este apartado se usa algebra para representar el comportamiento del sistema mediante variables numericas. El objetivo no es resolver una ecuacion unica, sino construir un modelo que combine datos del trafico digital para obtener un indice de actividad.

```text
Flujo digital = 0.45P + 0.25L + 0.15A + 0.15D
```

Donde:

```text
P = paquetes por segundo
L = intentos de login
A = cambios en archivos
D = salida de datos
```

```python
def calcular_flujo_digital(paquetes, intentos_login, cambios_archivos, salida_datos):
    return round(paquetes * 0.45 + intentos_login * 0.25 +
                 cambios_archivos * 0.15 + salida_datos * 0.15, 2)
```

Este bloque construye una expresion algebraica ponderada. Cada variable aporta una parte al resultado final. Los paquetes pesan mas porque representan el movimiento principal de la red, mientras que los login, archivos y salida de datos ayudan a detectar actividad sospechosa.

## Sustitucion de valores

El procedimiento algebraico consiste en tomar los valores de un paquete y sustituirlos en la formula del flujo digital.

```text
Si:
P = 800
L = 10
A = 4
D = 30

Flujo digital = 0.45(800) + 0.25(10) + 0.15(4) + 0.15(30)
Flujo digital = 360 + 2.5 + 0.6 + 4.5
Flujo digital = 367.6
```

```python
flujo = lm.calcular_flujo_digital(
    paquete["paquetes"], paquete["intentos_login"],
    paquete["cambios_archivos"], paquete["salida_datos"]
)
```

Aqui el programa no escribe la sustitucion a mano, pero hace el mismo proceso. Toma los valores reales del paquete y los manda a la funcion que calcula el flujo.

## Comparacion algebraica con umbrales

Despues de calcular el flujo, el sistema compara el resultado contra valores limite. Esto se puede representar con desigualdades.

```text
Flujo > U_FLUJO_CRITICO -> CRITICO
Paquetes > U_PAQUETES_ALERTA -> posible alerta
```

```python
if paquete["paquetes"] > srv.U_PAQUETES_CRIT or flujo > srv.U_FLUJO_CRITICO:
    estado = "CRITICO"
    cifrado = "REFORZADO"
```

Esta parte usa algebra mediante comparaciones. El resultado numerico del modelo se compara contra umbrales para decidir si el sistema sigue normal o si debe subir a estado critico.

## Modelado trigonometrico del comportamiento regular

En trigonometria se usa una senal periodica para representar un comportamiento de referencia. Esto permite comparar si los paquetes se parecen a una oscilacion regular o si se separan mucho de ella.

```text
S(t) = A sen(wt) + B cos(wt)
```

Donde:

```text
A = amplitud del seno
B = amplitud del coseno
w = frecuencia angular
t = tiempo en segundos
```

```python
def senal_periodica(t, A=45, B=18, w=0.3):
    return round(A * math.sin(w * t) + B * math.cos(w * t), 2)
```

Esta funcion usa seno y coseno para crear una onda. La onda no controla el sistema directamente, pero sirve para analisis posterior del comportamiento del trafico.

## Desviacion respecto al patron

Una vez calculada la senal periodica, el sistema compara esa senal contra los paquetes reales.

```text
Desviacion = |Paquetes reales - Senal periodica|
```

```python
def calcular_analisis_oscilatorio(paquetes, senal):
    desviacion_periodica = round(abs(paquetes - senal), 2)
    indice_oscilatorio = desviacion_periodica
    return desviacion_periodica, indice_oscilatorio
```

Este calculo ayuda a medir que tanto se separa el trafico real de un comportamiento de referencia. Si la desviacion es muy grande, puede indicar actividad irregular.

## Grafica de apoyo

**Grafica llamada:** `07_analisis_oscilatorio_vs_tiempo.png`

**Valores o parametros usados:**

| Valor | Significado |
|---|---|
| `t` | tiempo de la simulacion en segundos |
| `paquetes` | comportamiento real del trafico |
| `onda_envio` | onda regular generada como referencia |
| `intervalo = 5` | tamaño del intervalo usado para formar la onda |
| `max_regular = 500` | limite usado para representar trafico regular |

**Explicacion:**

Esta grafica permite observar visualmente cuando el trafico se mantiene cerca de un comportamiento regular y cuando se separa. En algebra y trigonometria se justifica como una comparacion entre un modelo construido y los datos reales generados por la simulacion.

La onda regular representa un comportamiento esperado de envio. La linea de paquetes representa lo que realmente paso. Si ambas se parecen, el trafico puede interpretarse como mas estable. Si los paquetes se separan demasiado de la onda, se puede interpretar como una desviacion o actividad irregular.

## Resultados y analisis

El resultado algebraico principal es el indice de flujo digital. Este indice resume varias variables en un solo numero y permite clasificar el comportamiento del sistema.

El resultado trigonometrico principal es la comparacion entre el trafico real y una onda de referencia. Si los paquetes se alejan demasiado del patron, el sistema puede interpretarlo como una desviacion.

La limitacion del modelo es que la onda no predice ataques reales; funciona como herramienta de analisis. Tambien los pesos del flujo digital son seleccionados por el proyecto, por lo que pueden ajustarse si se trabaja con datos reales.

## Conclusiones

El codigo permite justificar algebra mediante formulas ponderadas, sustitucion de valores y comparacion con umbrales. Tambien permite justificar trigonometria mediante el uso de seno y coseno para representar un comportamiento periodico.

Este enfoque puede ampliarse si se agregan datos reales de empresas atacadas, como numero de incidentes, costos o frecuencia de ataques. Con esos datos se podrian ajustar modelos algebraicos y trigonometrico-estadisticos mas cercanos a un caso real.
