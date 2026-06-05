# Analisis Calculo

## Funcion de trafico en el tiempo

En calculo se analiza como cambia una variable respecto al tiempo. En este proyecto la variable principal es el numero de paquetes o solicitudes por segundo.

```text
T(t) = paquetes registrados en el segundo t
```

Como los datos son simulados y se generan por segundo, no se trabaja con una funcion continua exacta. Se trabaja con una funcion discreta, formada por valores registrados en cada ciclo.

```python
for segundo in range(1, 61):
    paquete = trafico.generar_trafico_normal(segundo)
```

Aqui `segundo` funciona como la variable de tiempo. Cada vuelta del ciclo produce un nuevo valor de trafico.

## Primera derivada discreta

La primera derivada sirve para medir la velocidad de cambio. En este caso mide cuanto cambio el numero de paquetes entre un segundo y el anterior.

```text
T'(t) aproximada = (T(t) - T(t - 1)) / Delta t
```

Como la simulacion avanza de segundo en segundo:

```text
Delta t = 1
T'(t) aproximada = T(t) - T(t - 1)
```

```python
def calcular_derivada_discreta(actual, anterior, delta_t=1):
    if delta_t == 0:
        return 0
    return round((actual - anterior) / delta_t, 2)
```

Esta funcion hace la derivada discreta. Si el trafico actual es mayor que el anterior, el resultado es positivo. Si baja, el resultado es negativo.

## Tasa de cambio

La tasa de cambio se usa como forma directa de detectar subidas fuertes.

```text
Delta T = T(t) - T(t - 1)
```

```python
def calcular_tasa(actual, anterior):
    return actual - anterior
```

La tasa y la derivada discreta son muy parecidas en este proyecto porque el tiempo entre ciclos vale 1 segundo. La diferencia es que `tasa` se usa como lectura directa del crecimiento abrupto.

## Suavizado con sigmoide

El proyecto usa una funcion sigmoide para suavizar las derivadas. La sigmoide convierte un valor en un factor entre 0 y 1.

```text
sigmoide(x) = 1 / (1 + e^(-x))
```

En el codigo se usa asi:

```python
def calcular_sigmoide(x):
    if x >= 0:
        z = math.exp(-x)
        return 1 / (1 + z)
    z = math.exp(x)
    return z / (1 + z)
```

Esta forma evita errores cuando el exponente es muy grande. Matematicamente sigue siendo la funcion sigmoide.

```python
def aplicar_sigmoide_derivada(valor, escala=srv.U_TASA, k=6):
    if escala == 0:
        escala = 1
    factor = calcular_sigmoide(k * valor / escala)
    return round(valor * factor, 2)
```

Aqui se toma la derivada y se multiplica por el factor sigmoide. Si el cambio es positivo, el factor se acerca mas a 1. Si el cambio es negativo, el factor baja y suaviza mas la caida.

## Segunda derivada

La segunda derivada mide si el cambio se esta acelerando o frenando.

```text
T''(t) aproximada = T'(t) - T'(t - 1)
```

```python
def calcular_segunda_derivada(derivada_actual, derivada_anterior, delta_t=1):
    if delta_t == 0:
        return 0
    return round((derivada_actual - derivada_anterior) / delta_t, 2)
```

Si la segunda derivada es alta, significa que el trafico no solo subio, sino que su crecimiento se acelero. Eso puede relacionarse con ataques o cambios bruscos.

## Uso en alertas

```python
if tasa > srv.U_TASA:
    print("  [!!] CRECIMIENTO ABRUPTO DEL TRAFICO  tasa=" + str(tasa))
if segunda_derivada_sigmoide > srv.U_TASA:
    print("  [!!] ACELERACION DEL TRAFICO DETECTADA  d2=" + str(segunda_derivada_sigmoide))
```

Aqui calculo se vuelve parte del sistema de deteccion. Si la tasa o la aceleracion pasan el umbral, el programa marca una alerta.

## Grafica de derivadas

**Grafica llamada:** `06_derivadas_trafico_vs_tiempo.png`

**Valores o parametros usados:**

| Valor | Significado |
|---|---|
| `t` | tiempo de la simulacion en segundos |
| `primera_derivada_sigmoide` | cambio del trafico suavizado con sigmoide |
| `segunda_derivada_sigmoide` | aceleracion o frenado del cambio |
| `U_TASA` | umbral usado para marcar cambios importantes |
| `0` | linea base para separar subidas y bajadas |

**Explicacion:**

La grafica 6 muestra el comportamiento de las derivadas. La primera derivada indica si el trafico sube o baja respecto al segundo anterior. La segunda derivada muestra si ese cambio se acelera o se frena.

Esta grafica es importante para calculo porque permite interpretar visualmente la tasa de cambio y la aceleracion del trafico. Si la curva se eleva mucho, puede relacionarse con crecimiento abrupto o ataque.

## Resultados y analisis

El resultado principal de calculo es que el sistema puede detectar cambios abruptos. No solo ve cuantos paquetes hay, sino como cambian en el tiempo.

La limitacion es que las derivadas son discretas, no continuas. Esto es normal porque el programa trabaja con datos por segundo. Aun asi, el metodo sirve para analizar tendencias, subidas fuertes y aceleraciones del trafico.

## Conclusiones

Calculo se justifica con la funcion de trafico, tasa de cambio, primera derivada, segunda derivada y suavizado con sigmoide. Esto permite transformar datos simples en indicadores de comportamiento anomalo.

Si se quisiera ampliar, se podrian usar datos reales de incidentes o perdidas economicas para analizar crecimiento de ataques, tiempo de recuperacion o evolucion del impacto en una empresa.
