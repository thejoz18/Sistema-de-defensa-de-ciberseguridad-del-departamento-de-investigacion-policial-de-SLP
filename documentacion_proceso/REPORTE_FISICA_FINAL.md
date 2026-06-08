# Reporte final de Fisica

## 1. Introduccion

La ciberseguridad no depende solamente del software. Un sistema que protege expedientes, usuarios, direcciones IP y registros digitales tambien necesita servidores estables, energia electrica continua, ventilacion, sensores, UPS, cableado y sistemas de enfriamiento.

En este proyecto se simula un servidor que recibe trafico digital durante 60 segundos. El sistema analiza paquetes, intentos de login, cambios de archivos, salida de datos, uso de CPU, temperatura, refrigeracion y consumo electrico. Desde Fisica, el problema principal es explicar como una carga digital se convierte en trabajo del procesador, consumo de potencia, generacion de calor y necesidad de enfriamiento.

El modelo se simplifico para usar formulas claras:

```text
Flujo digital -> CPU -> Potencia electrica -> Temperatura -> Ventilador -> Refrigeracion -> Bernoulli critico
```

## 2. Objetivo

Analizar la relacion entre el funcionamiento digital del servidor y sus condiciones fisicas de operacion, aplicando conceptos de movimiento, velocidad, aceleracion, vibracion, potencia, energia, calor, transferencia termica, flujo de fluidos y presion.

## 3. Formula general

El modelo fisico general del proyecto se resume como una cadena de conversion:

```text
Flujo digital -> CPU -> Potencia electrica -> Temperatura -> Enfriamiento
```

Las formulas generales son:

```text
Potencia CPU = (CPU / 100) * Potencia maxima
Temperatura = Temperatura ambiente + Potencia CPU * factor termico
Velocidad = caudal / area
P1 = P2 - 0.5*rho*v1^2 + 0.5*rho*v2^2
```

Estas formulas permiten relacionar carga digital, consumo electrico, calor, movimiento del aire, flujo del refrigerante y presion en estado critico.

## 4. Planteamiento del problema

El servidor del sistema de defensa procesa informacion sensible. Cuando aumenta el trafico digital o aparece un ataque, el CPU trabaja mas. Ese aumento de carga incrementa la potencia electrica consumida y produce mas calor. Si el calor no se retira, el equipo puede reducir rendimiento, reiniciarse, danar componentes o perder disponibilidad.

La infraestructura fisica afecta directamente:

| Aspecto | Relacion con Fisica |
|---|---|
| Disponibilidad | si el servidor se sobrecalienta o pierde energia, el servicio se detiene |
| Seguridad | un apagado puede perder registros, dejar rutas incompletas o provocar fallas de cifrado |
| Continuidad | UPS, ventilacion, sensores y respaldo electrico mantienen el servicio activo |
| Rendimiento | la temperatura elevada puede reducir la velocidad efectiva del procesador |

Por eso la proteccion del sistema no se limita a detectar ataques: tambien debe mantener condiciones fisicas seguras.

## 5. Infraestructura de servidores

| Elemento fisico | Funcion |
|---|---|
| Servidores | ejecutan el programa, procesan trafico y guardan registros |
| Racks | ordenan servidores, switches, UPS y cableado |
| Centro de datos | espacio controlado para energia, ventilacion y seguridad fisica |
| Sistemas de enfriamiento | retiran calor del equipo |
| Fuentes de energia | alimentan CPU, ventiladores, discos y tarjetas |
| UPS | mantiene el sistema funcionando ante cortes breves de energia |
| Generador electrico | respaldo para interrupciones prolongadas |
| Cableado electrico | transporta energia a servidores y bombas |
| Cableado de red | conecta usuarios, sensores y sistemas de monitoreo |
| Sensores | miden temperatura, humedad, energia o flujo de aire |
| Ventiladores | generan movimiento de aire para disipar calor |
| Ventilacion y ductos | dirigen entrada de aire frio y salida de aire caliente |
| Refrigeracion por fluido | usa un fluido para extraer calor cuando el ventilador no basta |

## 6. Conceptos fisicos aplicados

### 6.1 CPU, potencia y temperatura

El programa calcula primero un flujo digital:

```text
Flujo = 0.45P + 0.25L + 0.15A + 0.15D
```

Donde `P` son paquetes, `L` intentos de login, `A` cambios de archivos y `D` salida de datos. Con ese flujo se calcula el CPU:

```text
CPU = CPU base + 0.035 * Flujo
```

Luego se convierte el CPU a potencia electrica:

```text
Potencia CPU = (CPU / 100) * 120 W
```

Finalmente se estima la temperatura:

```text
Temperatura = 28 C + Potencia CPU * 0.4833
```

Esta cadena muestra que un ataque digital puede transformarse en consumo electrico y calor.

### 6.2 Ventilador, movimiento y vibracion

El ventilador siempre esta activo. En estado normal baja aproximadamente 1 C por ciclo. Cuando entra refrigeracion, el ventilador aumenta 30 %. Esto permite usar velocidad y aceleracion:

```text
Velocidad del aire = caudal / area
```

El area de ventilacion usada es `0.3125 m2`. Si el caudal normal equivale a `1.0`, entonces:

```text
Velocidad normal = 1.0 / 0.3125 = 3.2 m/s
```

Cuando hay refrigeracion:

```text
Caudal = 1.0 * 1.30 = 1.30
Velocidad = 1.30 / 0.3125 = 4.16 m/s
```

El cambio de velocidad representa aceleracion del sistema de ventilacion. Tambien puede provocar mayor vibracion en ventiladores, soportes y racks, por lo que el equipo fisico debe estar bien instalado.

### 6.3 Calor y transferencia termica

El servidor produce calor por el trabajo electrico de sus componentes. Ese calor se retira por:

| Mecanismo | Aplicacion |
|---|---|
| Conduccion | el calor pasa de chips a disipadores |
| Conveccion | el aire o fluido se mueve y transporta calor |
| Radiacion | parte del calor se emite al ambiente |
| Disipacion termica | ventiladores y refrigerante reducen la temperatura |

Si la temperatura supera el umbral de refrigeracion, el programa activa enfriamiento por fluido. Si la temperatura antes de enfriar llega a nivel critico, se agregan protecciones.

### 6.4 Refrigeracion por fluido y Bernoulli

En refrigeracion normal, el sistema usa area y velocidad estandar. La entrada tiene el doble de area que la salida:

```text
Area salida = 0.02 m2
Area entrada = 0.04 m2
Velocidad entrada = 2.5 m/s
Velocidad refrigerante = (Area entrada * Velocidad entrada) / Area salida
Velocidad refrigerante = (0.04 * 2.5) / 0.02 = 5.0 m/s
```

El descenso normal se calcula con caudal:

```text
Caudal = Area salida * Velocidad
Descenso = Caudal * 22.8
```

En estado critico se usa Bernoulli para aumentar presion de entrada y velocidad del refrigerante:

```text
P1 + 0.5*rho*v1^2 = P2 + 0.5*rho*v2^2
P1 = P2 - 0.5*rho*v1^2 + 0.5*rho*v2^2
```

El objetivo es bajar la temperatura hasta quedar por debajo del umbral de refrigeracion. La presion de salida se mantiene como referencia y se calcula cuanta presion extra debe entregar la bomba.

## 7. Consumo energetico e impacto ambiental

El consumo total incluye:

```text
Consumo total = consumo base + potencia CPU + consumo ventilador + consumo refrigerante
```

El ventilador aumenta consumo cuando sube velocidad. El refrigerante consume mas porque necesita bomba. En estado critico el consumo puede crecer mucho por el incremento de presion, por eso el modo Bernoulli se justifica solo para emergencias.

Impactos ambientales:

| Factor | Impacto |
|---|---|
| Mayor CPU | mas energia electrica |
| Mayor calor | mas uso de ventilacion y refrigeracion |
| Bombas criticas | mayor consumo instantaneo |
| Enfriamiento continuo | emisiones indirectas si la energia viene de fuentes no renovables |

Estrategias de reduccion:

| Estrategia | Beneficio |
|---|---|
| sensores de temperatura | activan refrigeracion solo cuando hace falta |
| mantenimiento de ventiladores | reduce vibracion y mejora eficiencia |
| fuentes eficientes | reducen energia perdida como calor |
| pasillos frios y calientes | mejora flujo de aire |
| monitoreo de ataques | evita cargas anormales que elevan consumo |

## 8. Resultados de la simulacion

Ultima ejecucion registrada en el CSV:

| Resultado | Valor |
|---|---|
| ciclos ejecutados | 60 |
| incidentes detectados | 27 |
| ultimos 5 ciclos con ataque | 0 |
| CPU promedio | 39.3 % |
| CPU maximo | 78.0 % |
| temperatura promedio final | 48.6 C |
| temperatura maxima final | 57.0 C |
| temperatura maxima antes de enfriamiento | 73.2 C |
| ciclos con refrigeracion activa | 9 |
| velocidad maxima del ventilador | 4.16 m/s |
| velocidad maxima del refrigerante | 10.3 m/s |
| presion maxima de entrada | 151245 Pa |
| aumento maximo de presion | 49.27 % |
| consumo total acumulado | 16328.57 W |
| consumo maximo en un ciclo | 1755.25 W |

Interpretacion: aunque la temperatura antes de enfriamiento alcanzo 73.2 C, el sistema de ventilacion y refrigeracion logro que la temperatura final maxima fuera 57.0 C. Esto muestra que la infraestructura fisica ayuda a mantener continuidad operativa.

## 9. Conclusion

La infraestructura fisica es parte fundamental de la ciberseguridad. Un servidor no puede proteger informacion si se apaga, se sobrecalienta o pierde energia. El simulador muestra que el aumento de trafico digital incrementa CPU, potencia electrica y temperatura.

El ventilador mantiene una reduccion constante y acelera cuando entra refrigeracion. El fluido de enfriamiento trabaja con velocidad, caudal y area. En estado critico, Bernoulli permite justificar el aumento de presion de entrada para retirar calor con mayor rapidez.

La recomendacion principal es mantener monitoreo constante de CPU, temperatura, consumo y presion, ademas de contar con ventilacion, UPS y mantenimiento preventivo. Esto reduce riesgos fisicos y evita que un incidente digital se convierta en una falla de infraestructura.

