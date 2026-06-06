# Analisis Fisica

## Energia, CPU y temperatura

En fisica el proyecto se justifica por el impacto energetico y termico de un sistema digital. Cuando aumenta la actividad del servidor, tambien aumenta el uso del CPU y eso se refleja en la temperatura.

El procedimiento usado es:

```text
Actividad del sistema -> uso de CPU -> aumento de temperatura
```

```python
def calcular_cpu(paquete):
    actividad = (paquete["paquetes"] +
                 paquete["intentos_login"] * 45 +
                 paquete["cambios_archivos"] * 28 +
                 paquete["salida_datos"] * 18)
    cpu = paquete["cpu_base"] + 0.005 * actividad
    if cpu > 100:
        cpu = 100
    return round(cpu, 1)
```

Este bloque calcula el CPU a partir de la actividad del paquete. Si hay muchos paquetes, intentos de login, cambios de archivos o salida de datos, el CPU sube.

## Modelo de temperatura

La temperatura se calcula como una relacion lineal entre temperatura ambiente y uso de CPU.

```text
Temperatura = Temperatura ambiente + k(CPU)
```

```python
def calcular_temperatura(cpu, temp_ambiente=28, k=0.58):
    return round(temp_ambiente + k * cpu, 1)
```

Aqui se usa una aproximacion fisica simple. Si el CPU aumenta, la temperatura tambien aumenta. No es un modelo completo de transferencia de calor, pero sirve para representar el efecto termico del trabajo del servidor.

## Enfriamiento pasivo

El enfriamiento pasivo representa una disminucion natural de temperatura cuando el sistema no esta en estado critico.

```text
Cada cierto intervalo:
Temperatura nueva = Temperatura actual - descenso
```

```python
def aplicar_enfriamiento_pasivo(temperatura, segundo, intervalo=5, descenso=1.0):
    if segundo % intervalo != 0:
        return temperatura
    nueva = temperatura - descenso
    if nueva < 28:
        nueva = 28
    return round(nueva, 1)
```

Este bloque baja la temperatura cada 5 segundos. Tambien evita que baje de 28 grados, que se toma como temperatura ambiente minima del sistema.

## Flujo del refrigerante

Para el enfriamiento activo se usa una idea relacionada con continuidad de fluidos. Si el area del conducto cambia, la velocidad del refrigerante tambien cambia.

```text
A1 * v1 = A2 * v2
v2 = (A1 * v1) / A2
```

```python
def calcular_velocidad_refrigerante(area_1, velocidad_1, area_2):
    if area_2 == 0:
        return 0.0
    return round((area_1 * velocidad_1) / area_2, 4)
```

Esta funcion calcula la velocidad final del refrigerante. Si el area final es menor, la velocidad aumenta.

## Presion y Bernoulli

El sistema tambien usa una aproximacion de Bernoulli para calcular la presion final del refrigerante.

```text
P1 + 1/2 rho v1^2 = P2 + 1/2 rho v2^2
```

Despejando:

```text
P2 = P1 + 1/2 rho v1^2 - 1/2 rho v2^2
```

```python
def calcular_presion_bernoulli(presion_1, densidad, velocidad_1, velocidad_2):
    return round(presion_1 + 0.5 * densidad * velocidad_1**2
                           - 0.5 * densidad * velocidad_2**2, 2)
```

Esta parte calcula como cambia la presion cuando cambia la velocidad del refrigerante. Es una forma simplificada de aplicar Bernoulli al sistema de enfriamiento.

## Descenso de temperatura por refrigeracion

El descenso activo se calcula usando la velocidad del refrigerante y la caida relativa de presion.

```text
Caida relativa = (P1 - P2) / P1
Descenso = coeficiente * velocidad * caida relativa
```

```python
def calcular_descenso_bernoulli(velocidad_refrigerante, presion_inicial, presion_final, coef=4.4):
    if presion_inicial <= 0:
        return 0
    caida_relativa = max((presion_inicial - presion_final) / presion_inicial, 0)
    return round(coef * velocidad_refrigerante * caida_relativa, 2)
```

Este modelo no dice que Bernoulli por si solo calcule directamente la temperatura. Lo que hace el codigo es usar Bernoulli para estimar una condicion del refrigerante, y con esa condicion calcular cuanto baja la temperatura.

## Activacion del enfriamiento

```python
if temperatura >= srv.U_TEMP_CRITICA:
    estado = "CRITICO"
    refrigeracion = True
    protecciones.append("REFRIGERACION ACTIVADA")
elif temperatura >= srv.U_TEMP_REFRIG and not refrigeracion:
    refrigeracion = True
    protecciones.append("REFRIGERACION PREVENTIVA ACTIVADA")
```

Esta regla activa el enfriamiento cuando la temperatura pasa ciertos umbrales. Si es muy alta, el estado se vuelve critico. Si solo pasa el nivel preventivo, se activa refrigeracion sin llegar necesariamente al peor estado.

```python
if estado_actual["refrigeracion"]:
    if estado_actual["estado"] == "CRITICO":
        v2, P2 = lm.calcular_refrigeracion_critica(
            paquete["temperatura"], srv.U_TEMP_REFRIG - 1
        )
    paquete["temperatura"] = lm.aplicar_enfriamiento(
        paquete["temperatura"], v2, lm.P1_REFRIGERANTE, P2
    )
```

Aqui se aplica el enfriamiento activo usando la velocidad y presion calculadas. En estado preventivo se usa la presion normal que sale de Bernoulli. En estado critico se recalcula una presion final menor solo para ese segundo, con la intencion de bajar la temperatura al objetivo seguro de 57 C.

La temperatura no se fuerza directamente a 57 C. El codigo usa ese objetivo para calcular cuanta caida de presion necesita el refrigerante, y despues la temperatura baja por la formula de descenso.

## Grafica de temperatura

**Grafica llamada:** `03_temperatura_vs_tiempo.png`

**Valores o parametros usados:**

| Valor | Significado |
|---|---|
| `t` | tiempo de la simulacion en segundos |
| `temperatura_sin_enfriamiento` | temperatura calculada antes de aplicar refrigeracion |
| `temperatura` | temperatura final despues del enfriamiento |
| `U_TEMP_REFRIG` | umbral donde se activa refrigeracion preventiva |
| `U_TEMP_CRITICA` | umbral donde la temperatura se considera critica |
| `refrigeracion_activa` | marca los momentos donde actuo el sistema de enfriamiento |
| `velocidad_refrigerante` | velocidad final del refrigerante |
| `presion_refrigerante` | presion usada en ese segundo; baja mas cuando el estado es critico |

**Explicacion:**

La grafica 3 compara la temperatura original contra la temperatura despues de enfriar. Esto muestra el efecto fisico del sistema de refrigeracion.

Si la temperatura sin enfriamiento sube demasiado y la temperatura final baja, se puede interpretar que el sistema de refrigeracion esta actuando. Esta grafica ayuda a justificar la relacion entre actividad digital, CPU, temperatura y enfriamiento.

## Resultados y analisis

El resultado principal de fisica es que el programa relaciona actividad digital con temperatura. Cuando sube la actividad, sube el CPU y despues sube la temperatura.

El modelo de enfriamiento permite justificar que el sistema no solo detecta ataques digitales, sino que tambien considera el impacto fisico en servidores o centros de datos.

La limitacion es que no se modela un servidor real con todas sus variables fisicas. Se usa una aproximacion para representar energia, temperatura, presion y refrigeracion de manera comprensible.

## Conclusiones

Fisica se justifica mediante el analisis termico del servidor, el uso de CPU, la temperatura, el enfriamiento pasivo, continuidad de fluidos y Bernoulli.

Este apartado puede conectarse con casos reales de empresas atacadas porque un incidente digital no solo afecta datos. Tambien puede aumentar carga de servidores, consumo energetico, necesidad de refrigeracion y riesgo operativo en infraestructura tecnologica.
