# Reporte final de Calculo

## 1. Introduccion

El calculo permite estudiar como cambian las cantidades con respecto al tiempo. En ciberseguridad esto es importante porque un ataque no siempre se detecta solo por un valor alto; tambien puede detectarse por un cambio rapido.

En el simulador, cada ciclo representa un segundo. Por eso se usan derivadas discretas para analizar paquetes, CPU y temperatura. El objetivo es identificar crecimiento abrupto, aceleracion del trafico y desviaciones que indiquen riesgo.

## 2. Planteamiento del problema

El sistema debe responder:

```text
Como saber si el comportamiento del servidor esta cambiando demasiado rapido?
```

Para responderlo se analizan cambios entre un segundo y el siguiente. Si los paquetes aumentan mucho, si la derivada sube o si la segunda derivada indica aceleracion, el sistema puede generar alertas.

Datos usados:

| Dato | Variable |
|---|---|
| paquetes actuales | `paquetes` |
| paquetes anteriores | `paquetes_anteriores` |
| CPU actual | `cpu` |
| CPU anterior | `cpu_anterior` |
| temperatura actual | `temperatura` |
| temperatura anterior | `temperatura_anterior` |
| tiempo | `segundo` |

## 3. Formula general

La formula general de cambio usada en el proyecto es:

```text
f'(t) = (f(t) - f(t-1)) / delta_t
```

Como cada ciclo dura 1 segundo:

```text
f'(t) = f(t) - f(t-1)
```

Para analizar aceleracion se usa:

```text
f''(t) = (f'(t) - f'(t-1)) / delta_t
```

Estas formulas permiten medir crecimiento abrupto, caida de actividad y aceleracion del trafico.

## 4. Conceptos de calculo aplicados

### 4.1 Tasa de cambio

La tasa de cambio simple se calcula como:

```text
Tasa = valor actual - valor anterior
```

En el programa:

```text
Tasa de paquetes = paquetes actuales - paquetes anteriores
```

Si la tasa es alta, significa que el trafico crecio de forma abrupta.

### 4.2 Derivada discreta

Como el programa avanza de segundo en segundo, se usa una aproximacion:

```text
f'(t) = (f(t) - f(t-1)) / delta_t
```

Con `delta_t = 1`:

```text
f'(t) = f(t) - f(t-1)
```

Esto se aplica a:

| Derivada | Uso |
|---|---|
| derivada de paquetes | detectar crecimiento de trafico |
| derivada de CPU | detectar aumento de carga |
| derivada de temperatura | detectar calentamiento rapido |

### 4.3 Segunda derivada

La segunda derivada mide si la velocidad de cambio esta aumentando o disminuyendo:

```text
f''(t) = (f'(t) - f'(t-1)) / delta_t
```

En ciberseguridad, una segunda derivada alta puede indicar que el ataque se esta acelerando.

### 4.4 Funcion sigmoide

El programa usa una sigmoide para suavizar cambios:

```text
S(x) = 1 / (1 + e^-x)
```

La sigmoide convierte valores extremos en una escala mas controlada. Despues se usa como factor para ponderar la derivada:

```text
derivada ajustada = derivada * S(k * derivada / escala)
```

Esto ayuda a reducir ruido cuando los cambios son pequenos y resaltar cambios importantes.

## 5. Procedimiento del programa

El proceso de calculo se concentra en `m04_logica_matematica.py`.

Primero se crea un estado para guardar valores anteriores:

```python
estado_calculo = lm.crear_estado_calculo()
```

El estado guarda:

| Clave | Funcion |
|---|---|
| `paquetes_anteriores` | comparar trafico actual contra el anterior |
| `temperatura_anterior` | calcular derivada de temperatura |
| `cpu_anterior` | calcular derivada de CPU |
| `primera_derivada_sigmoide_anterior` | calcular segunda derivada |

Luego en cada ciclo se calculan:

```text
tasa
primera derivada de paquetes
primera derivada con sigmoide
segunda derivada con sigmoide
derivada de CPU
derivada de temperatura
```

## 6. Ejemplo de calculo

Si en un segundo anterior se tienen 420 paquetes y en el segundo actual 900:

```text
f(t-1) = 420
f(t) = 900
delta_t = 1

f'(t) = (900 - 420) / 1
f'(t) = 480 paquetes/s
```

Como el umbral de tasa es 250:

```text
480 > 250
```

Entonces el programa puede imprimir crecimiento abrupto del trafico.

Si la derivada anterior era 100 y la actual es 480:

```text
f''(t) = (480 - 100) / 1
f''(t) = 380
```

Esto indica aceleracion del crecimiento.

## 7. Interpretacion de graficas

La grafica mas relacionada con Calculo es:

```text
06_derivadas_trafico_vs_tiempo.png
```

Esta grafica muestra:

| Elemento | Interpretacion |
|---|---|
| primera derivada con sigmoide | velocidad de cambio del trafico |
| segunda derivada con sigmoide | aceleracion del cambio |
| umbral positivo | limite para crecimiento abrupto |
| umbral negativo | limite para caida fuerte |

Tambien se relacionan:

| Grafica | Relacion con Calculo |
|---|---|
| paquetes vs tiempo | permite observar la funcion original |
| flujo digital | muestra variacion del indicador |
| temperatura | permite observar calentamiento y enfriamiento |
| estado del sistema | muestra consecuencias de los cambios |

## 8. Resultados

Resultados relevantes del CSV:

| Resultado | Valor |
|---|---|
| ciclos ejecutados | 60 |
| tasa maxima de paquetes | 2768 |
| tasa minima de paquetes | -2615 |
| flujo maximo | 1413.6 |
| CPU maximo | 78.0 % |
| temperatura maxima antes de enfriar | 73.2 C |
| temperatura maxima final | 57.0 C |
| ultimos 5 ciclos con ataque | 0 |

Analisis:

1. La tasa maxima de 2768 supera ampliamente el umbral de 250, lo cual indica crecimiento abrupto.
2. La tasa minima de -2615 muestra una caida fuerte, relacionada con la reduccion de actividad al final.
3. La temperatura baja despues del enfriamiento, lo que indica que el sistema fisico responde a los cambios de carga.
4. Los ultimos 5 ciclos sin ataques permiten que las graficas muestren estabilizacion.

## 9. Limitaciones

| Limitacion | Explicacion |
|---|---|
| derivadas discretas | no son derivadas continuas exactas |
| datos simulados | no provienen de una red real |
| umbrales fijos | no se adaptan automaticamente |
| tiempo uniforme | se asume un segundo exacto por ciclo |

Aun con estas limitaciones, el modelo es adecuado para explicar Calculo de forma aplicada.

## 10. Conclusiones

El proyecto muestra que Calculo ayuda a detectar anomalias porque estudia cambios, no solo valores absolutos. La primera derivada permite medir velocidad de cambio; la segunda derivada permite detectar aceleracion; y la sigmoide ayuda a suavizar la interpretacion de cambios.

En ciberseguridad, estas ideas son utiles porque un ataque puede iniciar como un cambio brusco antes de convertirse en un valor extremo. Por eso analizar tasas y derivadas puede mejorar la deteccion temprana.

Como mejora futura, el sistema podria usar ventanas moviles, promedios dinamicos o modelos predictivos para anticipar ataques antes de que lleguen al estado critico.

