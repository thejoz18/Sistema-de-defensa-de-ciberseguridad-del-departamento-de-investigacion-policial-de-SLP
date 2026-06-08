# Reporte final de Algebra y Trigonometria

## 1. Objetivo general

Aplicar modelos algebraicos y trigonometricos para analizar el comportamiento de un sistema de ciberseguridad, construir indicadores numericos, interpretar graficas y detectar desviaciones entre trafico esperado y trafico observado.

## 2. Introduccion

La ciberseguridad requiere analizar grandes cantidades de datos. Un servidor puede recibir trafico normal, pero tambien trafico anormal provocado por ataques, intentos de acceso, modificaciones de archivos o salida excesiva de informacion.

El proyecto resuelve este problema mediante un simulador en Python. Cada segundo se generan datos de red y se transforman en indicadores matematicos. Algebra permite combinar variables mediante ecuaciones; trigonometria permite modelar un comportamiento periodico esperado; y las graficas permiten observar visualmente cambios, picos y desviaciones.

Objetivos del trabajo:

1. Representar datos de ciberseguridad con ecuaciones.
2. Construir un indice de flujo digital.
3. Usar una funcion trigonometrica como patron esperado.
4. Comparar datos reales contra el patron.
5. Interpretar resultados mediante graficas.

## 3. Formula general

El modelo algebraico general usa una combinacion ponderada:

```text
F = aP + bL + cA + dD
```

En el simulador:

```text
Flujo = 0.45P + 0.25L + 0.15A + 0.15D
```

La parte trigonometrica usa una senal periodica general:

```text
S(t) = A sen(wt) + B cos(wt)
```

Estas formulas permiten combinar datos de seguridad y compararlos contra un patron esperado.

## 4. Planteamiento del problema

Se quiere responder la siguiente pregunta:

```text
Como puede modelarse matematicamente el comportamiento de un servidor para detectar trafico sospechoso o critico?
```

Datos iniciales del simulador:

| Dato | Simbolo | Descripcion |
|---|---|---|
| paquetes | `P` | cantidad de paquetes recibidos |
| intentos de login | `L` | accesos intentados |
| cambios de archivos | `A` | modificaciones internas |
| salida de datos | `D` | informacion enviada fuera del sistema |
| tiempo | `t` | segundo del ciclo |

Suposiciones y simplificaciones:

| Suposicion | Justificacion |
|---|---|
| cada ciclo dura 1 segundo | facilita analizar el tiempo |
| el trafico normal puede aproximarse con una onda | muchos sistemas tienen patrones repetitivos |
| los indicadores se combinan con pesos fijos | simplifica la clasificacion |
| los umbrales son constantes | permite tomar decisiones claras |
| los ultimos 5 ciclos no reciben ataques | representa estabilizacion del sistema |

## 5. Desarrollo: procedimiento y solucion

### 5.1 Modelado algebraico del flujo digital

El primer modelo algebraico combina cuatro variables:

```text
Flujo = 0.45P + 0.25L + 0.15A + 0.15D
```

Los pesos suman 1:

```text
0.45 + 0.25 + 0.15 + 0.15 = 1.00
```

Esto significa que el flujo digital es una combinacion ponderada. Paquetes tiene mayor peso porque representa volumen de red. Login tiene segundo peso porque representa intentos de acceso. Cambios y salida de datos tienen menor peso, pero siguen siendo importantes para detectar manipulacion o fuga.

Ejemplo numerico:

```text
P = 900
L = 8
A = 5
D = 40

Flujo = 0.45(900) + 0.25(8) + 0.15(5) + 0.15(40)
Flujo = 405 + 2 + 0.75 + 6
Flujo = 413.75
```

### 5.2 Clasificacion por umbrales

El flujo se compara con umbrales:

| Umbral | Valor | Interpretacion |
|---|---|---|
| flujo elevado | 350 | actividad alta |
| flujo en riesgo | 700 | posible ataque |
| flujo critico | 1100 | riesgo fuerte |

Si el flujo supera 1100, el sistema puede pasar a `CRITICO` y activar cifrado reforzado.

### 5.3 Modelo trigonometrico del comportamiento esperado

El programa usa una senal periodica:

```text
S(t) = 45 sen(0.3t) + 18 cos(0.3t)
```

Donde:

| Elemento | Significado |
|---|---|
| `45` | amplitud principal |
| `18` | componente secundaria |
| `0.3` | frecuencia angular |
| `t` | segundo del ciclo |

Esta funcion representa un comportamiento regular esperado. No significa que el trafico real deba ser igual, sino que sirve como referencia para medir desviaciones.

Ejemplo para `t = 10`:

```text
S(10) = 45 sen(3) + 18 cos(3)
S(10) = 45(0.1411) + 18(-0.9900)
S(10) = 6.3495 - 17.82
S(10) = -11.47
```

### 5.4 Desviacion periodica

La desviacion se calcula como:

```text
Desviacion = |paquetes reales - senal esperada|
```

Si la desviacion es alta, el trafico observado se aleja del patron esperado. El programa usa:

| Umbral | Valor |
|---|---|
| oscilacion sospechosa | 650 |
| oscilacion critica | 1200 |

### 5.5 Construccion de graficas

Las graficas apoyan la solucion:

| Grafica | Uso algebraico o trigonometrico |
|---|---|
| paquetes vs tiempo | observa crecimiento o caida de trafico |
| flujo digital | muestra resultado de la ecuacion ponderada |
| estado del sistema | muestra clasificacion por umbrales |
| analisis oscilatorio | compara datos contra onda esperada |

La grafica 07 usa una onda de envio regular para contrastar el comportamiento lineal real.

## 6. Resultados y analisis

Resultados principales del CSV:

| Resultado | Valor |
|---|---|
| ciclos ejecutados | 60 |
| paquetes totales | 34513 |
| flujo promedio | 266.38 |
| flujo maximo | 1413.6 |
| indice oscilatorio maximo | 3069.67 |
| ciclos normales | 34 |
| ciclos sospechosos | 2 |
| ciclos en alerta | 15 |
| ciclos criticos | 9 |
| ultimos 5 ciclos con ataque | 0 |

Interpretacion:

1. El flujo maximo de 1413.6 supera el umbral critico de 1100, por eso aparecen ciclos `CRITICO`.
2. El indice oscilatorio maximo de 3069.67 supera el umbral critico de 1200, lo que confirma desviaciones fuertes.
3. Los ultimos 5 ciclos no tienen ataques, por eso las graficas deben mostrar una caida al final.
4. El cifrado puede permanecer reforzado aunque los ultimos ciclos sean normales, porque el sistema conserva protecciones hasta que el usuario decida estabilizar.

Limitaciones del modelo:

| Limitacion | Explicacion |
|---|---|
| pesos fijos | en un sistema real podrian calibrarse con datos historicos |
| onda ideal | el trafico real no siempre es periodico |
| umbrales constantes | podrian adaptarse automaticamente |
| simulacion aleatoria | cada ejecucion puede cambiar resultados |

## 7. Conclusiones

El proyecto demuestra que Algebra y Trigonometria pueden aplicarse a ciberseguridad. Algebra permite construir el flujo digital mediante una ecuacion ponderada y comparar resultados contra umbrales. Trigonometria permite proponer una senal esperada y medir desviaciones.

La combinacion de ecuaciones, umbrales y graficas permite detectar comportamientos anormales. En el contexto de Ingenieria en Inteligencia Artificial, estos modelos son importantes porque muchos algoritmos usan funciones, pesos, patrones, series temporales y comparacion de datos para clasificar eventos.

Como mejora futura, se podria reemplazar los pesos fijos por pesos aprendidos automaticamente a partir de datos reales, lo cual acercaria el sistema a un detector inteligente de anomalias.

