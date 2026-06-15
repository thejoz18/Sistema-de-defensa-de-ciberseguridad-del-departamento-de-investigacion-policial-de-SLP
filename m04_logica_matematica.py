##Este modulo concentra los calculos del proyecto.
##Aqui estan calculo, algebra, trigonometria, fundamentos matematicos y fisica.

# Importamos math para usar exponenciales, seno, coseno y formulas fisicas.
import math
# Importamos servidores para usar umbrales y listas autorizadas.
import m01_servidores as srv

##======================================================
##CALCULO
##======================================================
##En esta seccion se calculan tasas, derivadas y cambios
##entre un segundo y otro de la simulacion.
##Se usan derivadas discretas porque el tiempo avanza en
##pasos enteros (segundo a segundo), no de forma continua.

def crear_estado_calculo():
    ##Guarda los valores del segundo anterior para poder
    ##calcular como cambiaron en el siguiente ciclo.
    ##Solo se comenta el diccionario completo porque sus campos son valores iniciales.
    return {
        "paquetes_anteriores": 0,
        "temperatura_anterior": 0,
        "cpu_anterior": 0,
        "primera_derivada_sigmoide_anterior": 0
    }

def calcular_metricas_calculo(paquete, estado_calculo):
    ##Calcula cuanto cambiaron los paquetes respecto al segundo anterior.
    tasa = calcular_tasa(paquete["paquetes"], estado_calculo["paquetes_anteriores"])

    ##Derivada discreta: (f(t) - f(t-1)) / delta_t
    ##Mide la velocidad de cambio de los paquetes entre dos momentos.
    primera_derivada_paquetes = calcular_derivada_discreta(
        paquete["paquetes"], estado_calculo["paquetes_anteriores"]
    )

    ##Aplica sigmoide a la primera derivada para suavizarla entre 0 y 1,
    ##evitando que valores extremos distorsionen el analisis.
    primera_derivada_sigmoide = aplicar_sigmoide_derivada(primera_derivada_paquetes, srv.U_TASA)

    ##Segunda derivada: mide la aceleracion del cambio.
    ##Si la primera derivada sube rapido, la segunda lo detecta.
    segunda_derivada_sigmoide = calcular_segunda_derivada(
        primera_derivada_sigmoide, estado_calculo["primera_derivada_sigmoide_anterior"]
    )
    segunda_derivada_sigmoide = aplicar_sigmoide_derivada(
        segunda_derivada_sigmoide, srv.U_TASA
    )

    ##Actualiza el estado con los valores actuales para el proximo ciclo.
    estado_calculo["paquetes_anteriores"] = paquete["paquetes"]
    estado_calculo["primera_derivada_sigmoide_anterior"] = primera_derivada_sigmoide

    ##Regresamos todas las metricas en un diccionario para usarlas en m00.
    return {
        "tasa": tasa,
        "primera_derivada_sigmoide": primera_derivada_sigmoide,
        "segunda_derivada_sigmoide": segunda_derivada_sigmoide,
        "primera_derivada_paquetes": primera_derivada_paquetes
    }

def calcular_tasa(actual, anterior):
    ##Tasa de cambio simple: cuantos paquetes mas (o menos)
    ##llegaron en este segundo comparado con el anterior.
    ##Tasa = f(t) - f(t-1)
    return actual - anterior

def calcular_derivada_discreta(actual, anterior, delta_t=1):
    ##Aproximacion de la derivada para valores discretos (no continuos):
    ##f'(t) = (f(t) - f(t-1)) / delta_t
    ##Con delta_t = 1 segundo, equivale a la tasa de cambio por segundo.
    if delta_t == 0:
        return 0
    return round((actual - anterior) / delta_t, 2)

def calcular_sigmoide(x):
    ##Funcion sigmoide: S(x) = 1 / (1 + e^-x)
    ##Convierte cualquier numero real en un valor entre 0 y 1.
    ##Se divide en dos casos para evitar desbordamiento numerico
    ##con exponentes muy grandes o muy pequeños.
    if x >= 0:
        z = math.exp(-x)
        return 1 / (1 + z)
    z = math.exp(x)
    return z / (1 + z)

def aplicar_sigmoide_derivada(valor, escala=srv.U_TASA, k=6):
    ##Pondera el valor de la derivada usando la sigmoide como factor:
    ##resultado = valor * S(k * valor / escala)
    ##k controla que tan agresiva es la curva de suavizado.
    ##Cuando el valor es pequeno relativo a la escala, el factor es bajo
    ##y el resultado se reduce. Cuando es grande, el factor se acerca a 1.
    if escala == 0:
        escala = 1
    factor = calcular_sigmoide(k * valor / escala)
    return round(valor * factor, 2)

def calcular_segunda_derivada(derivada_actual, derivada_anterior, delta_t=1):
    ##Segunda derivada discreta: mide como cambia la primera derivada.
    ##f''(t) = (f'(t) - f'(t-1)) / delta_t
    ##Detecta aceleracion o desaceleracion en el trafico de paquetes.
    if delta_t == 0:
        return 0
    return round((derivada_actual - derivada_anterior) / delta_t, 2)

def calcular_derivadas_fisicas(paquete, estado_calculo):
    ##Aplica la derivada discreta a la CPU y temperatura del servidor.
    ##Permite detectar si la CPU esta subiendo rapido o si la temperatura
    ##esta escalando de forma peligrosa entre un segundo y otro.
    derivada_cpu = calcular_derivada_discreta(paquete["cpu"], estado_calculo["cpu_anterior"])
    derivada_temperatura = calcular_derivada_discreta(
        paquete["temperatura"], estado_calculo["temperatura_anterior"]
    )

    estado_calculo["cpu_anterior"] = paquete["cpu"]
    estado_calculo["temperatura_anterior"] = paquete["temperatura"]

    return derivada_cpu, derivada_temperatura


##======================================================
##ALGEBRA Y TRIGONOMETRIA
##======================================================
##En esta seccion se trabajan formulas numericas.

def calcular_flujo_digital(paquetes, intentos_login, cambios_archivos, salida_datos):
    ##Combina los cuatro indicadores de red en un solo indice de flujo.
    ##Cada indicador tiene un peso segun su importancia para detectar amenazas:
    ##  paquetes         45% -> principal indicador de volumen de trafico
    ##  intentos_login   25% -> señal directa de ataque de fuerza bruta
    ##  cambios_archivos 15% -> posible manipulacion de datos internos
    ##  salida_datos     15% -> posible exfiltracion de informacion
    ##flujo = 0.45*paquetes + 0.25*login + 0.15*archivos + 0.15*salida
    return round(paquetes * 0.45 + intentos_login * 0.25 +
                 cambios_archivos * 0.15 + salida_datos * 0.15, 2)

def senal_periodica(t, A=45, B=18, w=0.3):
    ##Modela el trafico normal del servidor como una onda combinada:
    ##f(t) = A * sin(w*t) + B * cos(w*t)
    ##A = amplitud del seno  (45): componente de carga ciclica principal
    ##B = amplitud del coseno (18): componente de carga secundaria desfasada
    ##w = frecuencia angular  (0.3): que tan rapido oscila el ciclo
    ##Juntos representan el patron esperado de paquetes en condiciones normales.
    return round(A * math.sin(w * t) + B * math.cos(w * t), 2)

def calcular_analisis_oscilatorio(paquetes, senal):
    ##Compara los paquetes reales contra la senal periodica esperada.
    ##Una desviacion alta indica que el trafico salio del patron normal,
    ##lo que puede señalar un ataque o anomalia en la red.
    ##desviacion = |paquetes_reales - senal_esperada|
    desviacion_periodica = round(abs(paquetes - senal), 2)
    indice_oscilatorio = desviacion_periodica
    return desviacion_periodica, indice_oscilatorio


##======================================================
##FUNDAMENTOS MATEMATICOS
##======================================================
##En esta seccion se trabajan cifrados y se decide el estado digital.

CLAVE_CESAR = 3                    ##Desplazamiento del cifrado Cesar
CLAVE_MULTIPLICATIVA_LETRAS = 5    ##Factor de cifrado para letras (debe ser coprimo con 26)
CLAVE_MULTIPLICATIVA_NUMEROS = 7   ##Factor de cifrado para digitos (debe ser coprimo con 10)
AJUSTE_MULTIPLICATIVO_NUMEROS = 3  ##Desplazamiento adicional para digitos

##--- Cifrado Cesar ---

def cifrado_cesar(texto, d):
    ##Desplaza cada letra d posiciones en el alfabeto (modulo 26).
    ##Formula: c_cifrado = (posicion + d) mod 26
    ##Respeta mayusculas/minusculas y deja intactos numeros y simbolos.
    resultado = ""
    for c in texto:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            resultado = resultado + chr((ord(c) - base + d) % 26 + base)
        else:
            resultado = resultado + c
    return resultado

def descifrado_cesar(texto, d):
    ##Descifra invirtiendo el desplazamiento: aplica Cesar con -d.
    ##Si cifrado fue con d=3, descifrado usa d=-3.
    return cifrado_cesar(texto, -d)

##--- Cifrado Multiplicativo ---

def obtener_inverso_modular(clave, modulo):
    ##Busca el inverso modular de la clave respecto al modulo.
    ##El inverso es el numero x tal que: (clave * x) mod modulo = 1
    ##Es necesario para el descifrado: sin el inverso no se puede revertir
    ##la multiplicacion modular. Si no existe (clave no coprima), devuelve None.
    for posible in range(1, modulo):
        if (clave * posible) % modulo == 1:
            return posible
    return None

def cifrado_multiplicativo(texto, clave_letras=CLAVE_MULTIPLICATIVA_LETRAS,
                           clave_numeros=CLAVE_MULTIPLICATIVA_NUMEROS,
                           ajuste_numeros=AJUSTE_MULTIPLICATIVO_NUMEROS):
    ##Cifra letras multiplicando su posicion en el alfabeto por la clave:
    ##  posicion_cifrada = (posicion * clave_letras) mod 26
    ##Cifra digitos con una formula afin (multiplicacion + desplazamiento):
    ##  digito_cifrado = (digito * clave_numeros + ajuste) mod 10
    ##Simbolos y espacios se copian sin cambio.
    resultado = ""
    for c in texto:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            nueva_posicion = ((ord(c) - base) * clave_letras) % 26
            resultado = resultado + chr(nueva_posicion + base)
        elif c.isdigit():
            nueva_posicion = (int(c) * clave_numeros + ajuste_numeros) % 10
            resultado = resultado + str(nueva_posicion)
        else:
            resultado = resultado + c
    return resultado

def descifrado_multiplicativo(texto, clave_letras=CLAVE_MULTIPLICATIVA_LETRAS,
                              clave_numeros=CLAVE_MULTIPLICATIVA_NUMEROS,
                              ajuste_numeros=AJUSTE_MULTIPLICATIVO_NUMEROS):
    ##Invierte el cifrado multiplicativo usando el inverso modular.
    ##Para letras:  posicion_original = (posicion_cifrada * inverso_letras) mod 26
    ##Para digitos: digito_original = ((digito_cifrado - ajuste) * inverso_numeros) mod 10
    ##Los inversos se calculan una sola vez antes del ciclo para no repetir trabajo.
    inverso_letras = obtener_inverso_modular(clave_letras, 26)
    inverso_numeros = obtener_inverso_modular(clave_numeros, 10)
    resultado = ""
    for c in texto:
        if c.isalpha() and inverso_letras is not None:
            base = ord('A') if c.isupper() else ord('a')
            nueva_posicion = ((ord(c) - base) * inverso_letras) % 26
            resultado = resultado + chr(nueva_posicion + base)
        elif c.isdigit() and inverso_numeros is not None:
            nueva_posicion = ((int(c) - ajuste_numeros) * inverso_numeros) % 10
            resultado = resultado + str(nueva_posicion)
        else:
            resultado = resultado + c
    return resultado

##--- Cifrado Reforzado (Cesar + Multiplicativo) ---

def cifrado_reforzado(texto):
    ##Aplica dos capas de cifrado en secuencia:
    ##Paso 1: Cesar  -> desplaza cada letra d posiciones
    ##Paso 2: Multiplicativo -> multiplica la posicion resultante por la clave
    ##Combinarlos hace el cifrado mas resistente que cada uno por separado.
    return cifrado_multiplicativo(cifrado_cesar(texto, CLAVE_CESAR))

def descifrado_reforzado(texto):
    ##Invierte el cifrado reforzado en orden opuesto al cifrado:
    ##Paso 1: Descifrado multiplicativo -> deshace la multiplicacion
    ##Paso 2: Descifrado Cesar          -> deshace el desplazamiento
    return descifrado_cesar(descifrado_multiplicativo(texto), CLAVE_CESAR)

##--- Estado y Registro ---

def evaluar_estado(paquete, flujo, cifrado_actual, indice_oscilatorio):
    ##Analiza los indicadores del paquete y determina el nivel de amenaza.
    ##El estado escala de NORMAL -> SOSPECHOSO -> ALERTA -> CRITICO
    ##segun cuantas condiciones se activen y que tan graves sean.
    ##El cifrado escala de NINGUNO -> CIFRADO -> REFORZADO en paralelo.
    ##Estas listas guardan mensajes que luego se imprimen en consola.
    alertas      = []
    protecciones = []
    ##Iniciamos en NORMAL y solo se cambia si alguna regla se activa.
    estado       = "NORMAL"
    ##Conservamos el cifrado que venia activo del ciclo anterior.
    cifrado      = cifrado_actual

    ##Acceso de usuario no registrado en la lista de agentes autorizados.
    if paquete["usuario"] not in srv.agentes_autorizados:
        alertas.append("ACCESO NO AUTORIZADO: " + paquete["usuario"])
        estado = "ALERTA"

    ##Combinacion de trafico alto + muchos intentos de login: posible ataque coordinado.
    if paquete["paquetes"] > srv.U_PAQUETES_ALERTA and paquete["intentos_login"] > srv.U_LOGIN_ALERTA:
        alertas.append("TRAFICO MASIVO + FUERZA BRUTA")
        estado = "ALERTA"
        if cifrado == "NINGUNO":
            cifrado = "CIFRADO"
            protecciones.append("CIFRADO ACTIVADO")

    ##Muchos cambios en archivos en poco tiempo: posible manipulacion de expedientes.
    if paquete["cambios_archivos"] > srv.U_CAMBIOS:
        alertas.append("MANIPULACION DE EXPEDIENTE DETECTADA")
        if estado != "CRITICO":
            estado = "ALERTA"

    ##Salida de datos excesiva: posible exfiltracion de informacion sensible.
    if paquete["salida_datos"] > srv.U_SALIDA_DATOS:
        alertas.append("SALIDA DE DATOS ELEVADA: " + str(paquete["salida_datos"]) + " MB")
        if cifrado == "NINGUNO":
            cifrado = "CIFRADO"
            protecciones.append("CIFRADO POR SALIDA DE DATOS")

    ##Trafico o flujo en nivel critico: se activa el cifrado mas fuerte.
    if paquete["paquetes"] > srv.U_PAQUETES_CRIT or flujo > srv.U_FLUJO_CRITICO:
        estado  = "CRITICO"
        cifrado = "REFORZADO"
        alertas.append("FLUJO O TRAFICO CRITICO")
        protecciones.append("CIFRADO REFORZADO ACTIVADO")

    ##El trafico real se alejo demasiado del patron periodico esperado.
    if indice_oscilatorio > srv.U_OSCILACION_CRIT:
        estado  = "CRITICO"
        cifrado = "REFORZADO"
        alertas.append("DESVIACION OSCILATORIA CRITICA")
        protecciones.append("ANALISIS OSCILATORIO REGISTRADO")
    elif indice_oscilatorio > srv.U_OSCILACION_SOSP and estado == "NORMAL":
        ##Desviacion moderada: no es critica pero tampoco es normal.
        estado = "SOSPECHOSO"

    ##Intentos de login en nivel critico: posible ataque de fuerza bruta activo.
    if paquete["intentos_login"] > srv.U_LOGIN_CRIT:
        alertas.append("FUERZA BRUTA CRITICA")
        protecciones.append("LOGIN REMOTO CERRADO")

    ##Si no se activo ninguna alerta pero algunos valores estan elevados,
    ##se marca como sospechoso para seguimiento sin escalar a alerta.
    if len(alertas) == 0:
        if (paquete["paquetes"] > srv.U_PAQUETES_SOSP or
                paquete["intentos_login"] > 4 or
                indice_oscilatorio > srv.U_OSCILACION_SOSP):
            estado = "SOSPECHOSO"

    return estado, alertas, protecciones, cifrado

def generar_direccion_registro(paquete, estado, cifrado, segundo):
    ##Construye la ruta interna y la cifra segun el nivel de amenaza.
    ##El enlace completo solo se muestra en la direccion del servidor.
    central = paquete["central"].lower()
    carpeta = paquete["carpeta_id"].lower()
    nombre_base = "datos_" + str(segundo).zfill(2) + ".log"
    ruta_base = central + "/" + carpeta + "/" + nombre_base

    if estado == "CRITICO" or cifrado == "REFORZADO":
        return cifrado_reforzado(ruta_base)

    if estado == "ALERTA" or estado == "SOSPECHOSO" or cifrado == "CIFRADO":
        return cifrado_cesar(ruta_base, CLAVE_CESAR)

    return ruta_base

def descifrar_direccion_registro(direccion, cifrado, estado="NORMAL"):
    ##Descifra la ruta interna y agrega el enlace completo del servidor.
    if estado == "CRITICO" or cifrado == "REFORZADO":
        ruta = descifrado_reforzado(direccion)
        return "http://servidor/" + ruta

    if estado == "ALERTA" or estado == "SOSPECHOSO" or cifrado == "CIFRADO":
        ruta = descifrado_cesar(direccion, CLAVE_CESAR)
        return "http://servidor/" + ruta

    return "http://servidor/" + direccion


##======================================================
##FISICA
##======================================================
##En esta seccion se calculan consecuencias fisicas
##del estado del servidor: temperatura, refrigeracion y consumo.

AREA_SALIDA_REFRIGERANTE = 0.02       ##m²  - seccion de salida del refrigerante
COEFICIENTE_REFRIGERANTE_MS = 2.5     ##m/s - velocidad base del refrigerante en la entrada
AREA_VENTILACION = 0.3125             ##m²  - area del ducto de ventilacion
P1_REFRIGERANTE = 101325              ##Pa  - presion atmosferica de referencia (1 atm)
RHO_REFRIGERANTE = 1000               ##kg/m³ - densidad del refrigerante (agua)
DESCENSO_VENTILADOR = 1.0             ##°C  - enfriamiento base del ventilador por ciclo
FACTOR_VENTILADOR_REFRIGERACION = 1.30 ##sin unidad - incremento del 30% al activar refrigeracion
POTENCIA_CPU_MAX_WATTS = 120          ##W   - potencia maxima de la CPU al 100%
FACTOR_TEMP_WATT = 0.4833             ##°C/W - cuanto sube la temperatura por cada watt de la CPU
CONSUMO_BASE_SISTEMA_WATTS = 80       ##W   - consumo fijo del sistema sin carga adicional
COSTO_VENTILADOR_WATTS = 35           ##W   - consumo del ventilador a velocidad normal
COSTO_REFRIGERANTE_WATTS = 180        ##W   - consumo de la bomba de refrigerante a velocidad base
FACTOR_REFRIGERACION = 22.8           ##°C·s/m³ - constante de enfriamiento del refrigerante normal

##1. CARGA Y TEMPERATURA DE CPU
def calcular_cpu_temperatura(flujo, cpu_base, temp_ambiente=28):
    ##Calcula el uso de CPU escalando linealmente con el flujo digital:
    ##  cpu = cpu_base + 0.035 * flujo  (limitado a 100%)
    ##Luego obtiene la potencia en watts segun el porcentaje de uso:
    ##  potencia = (cpu / 100) * POTENCIA_CPU_MAX_WATTS
    ##Y la temperatura como calor generado sobre la temperatura ambiente:
    ##  temperatura = temp_ambiente + potencia * FACTOR_TEMP_WATT
    cpu = cpu_base + 0.035 * flujo
    if cpu > 100:
        cpu = 100
    cpu = round(cpu, 1)
    potencia_cpu = round((cpu / 100) * POTENCIA_CPU_MAX_WATTS, 2)
    temperatura = round(temp_ambiente + potencia_cpu * FACTOR_TEMP_WATT, 1)
    return cpu, potencia_cpu, temperatura

##2. VENTILADOR (siempre activo, sube 30% si hay refrigeracion)
def calcular_ventilador(temperatura, hay_refrigeracion):
    ##El ventilador siempre corre y baja la temperatura en DESCENSO_VENTILADOR grados.
    ##Si el sistema de refrigeracion esta activo, el caudal sube un 30%:
    ##  caudal = DESCENSO_VENTILADOR * 1.30
    ##La velocidad del aire se calcula con la ecuacion de continuidad:
    ##  velocidad = caudal / area_ventilacion  (Q = v * A  ->  v = Q / A)
    if hay_refrigeracion:
        caudal = DESCENSO_VENTILADOR * FACTOR_VENTILADOR_REFRIGERACION
    else:
        caudal = DESCENSO_VENTILADOR
    velocidad = round(caudal / AREA_VENTILACION, 2)
    descenso = round(caudal, 2)
    return velocidad, descenso

##3. REFRIGERACION LIQUIDA (normal o critica con Bernoulli)
def calcular_refrigeracion(temperatura, estado):
    ##Calcula la velocidad y el descenso de temperatura del sistema de refrigeracion liquida.
    ##Primero obtiene la velocidad base usando la ecuacion de continuidad:
    ##  A_entrada * v_entrada = A_salida * v_salida
    ##  v_base = (area_entrada * velocidad_entrada) / area_salida
    area_entrada = AREA_SALIDA_REFRIGERANTE * 2
    velocidad_entrada = COEFICIENTE_REFRIGERANTE_MS
    velocidad_base = (area_entrada * velocidad_entrada) / AREA_SALIDA_REFRIGERANTE

    presion_entrada = P1_REFRIGERANTE
    presion_salida = P1_REFRIGERANTE
    velocidad_refrigerante = 0
    descenso_refrigerante = 0

    if estado == "CRITICO":
        ##En estado CRITICO se usa el principio de Bernoulli para aumentar
        ##la velocidad del refrigerante hasta bajar la temperatura al umbral - 1 grado.
        ##Ecuacion de Bernoulli entre dos puntos del flujo:
        ##  P1 + 0.5*rho*v1² = P2 + 0.5*rho*v2²
        ##Despejando P1:
        ##  P1 = P2 - 0.5*rho*v_entrada² + 0.5*rho*v_refrigerante²
        ##La caida relativa de presion estima el efecto de enfriamiento:
        ##  caida_relativa = (P1 - P2) / P1
        ##  descenso = 4.4 * velocidad * caida_relativa
        ##El ciclo incrementa la velocidad de 0.1 en 0.1 hasta alcanzar el descenso necesario
        ##o llegar al limite mecanico de 14.0 m/s.
        objetivo = srv.U_TEMP_REFRIG - 1
        descenso_necesario = temperatura - objetivo
        velocidad_refrigerante = velocidad_base

        while velocidad_refrigerante <= 14.0:
            presion_entrada = round(
                presion_salida
                - 0.5 * RHO_REFRIGERANTE * velocidad_entrada ** 2
                + 0.5 * RHO_REFRIGERANTE * velocidad_refrigerante ** 2, 2
            )
            caida_relativa = max((presion_entrada - presion_salida) / presion_entrada, 0)
            descenso_refrigerante = round(4.4 * velocidad_refrigerante * caida_relativa, 2)
            if descenso_refrigerante >= descenso_necesario:
                break
            velocidad_refrigerante = velocidad_refrigerante + 0.1

        ##Si se llego al limite sin alcanzar el objetivo, se usa el maximo disponible.
        if velocidad_refrigerante > 14.0:
            velocidad_refrigerante = 14.0
            presion_entrada = round(
                presion_salida
                - 0.5 * RHO_REFRIGERANTE * velocidad_entrada ** 2
                + 0.5 * RHO_REFRIGERANTE * velocidad_refrigerante ** 2, 2
            )
            caida_relativa = max((presion_entrada - presion_salida) / presion_entrada, 0)
            descenso_refrigerante = round(4.4 * velocidad_refrigerante * caida_relativa, 2)
    else:
        ##En estado de refrigeracion normal la velocidad es la base (sin ajuste Bernoulli).
        ##El descenso se calcula con el caudal volumetrico y una constante de enfriamiento:
        ##  caudal = area_salida * velocidad
        ##  descenso = caudal * FACTOR_REFRIGERACION
        velocidad_refrigerante = velocidad_base
        caudal_refrigerante = AREA_SALIDA_REFRIGERANTE * velocidad_refrigerante
        descenso_refrigerante = round(caudal_refrigerante * FACTOR_REFRIGERACION, 2)

    return round(velocidad_refrigerante, 2), presion_entrada, presion_salida, round(descenso_refrigerante, 2)

##4. CONSUMO TOTAL EN WATTS
def calcular_consumo_watts(potencia_cpu, velocidad_ventilador,
                           velocidad_refrigerante=0, presion_entrada=P1_REFRIGERANTE):
    ##Suma todos los consumos del sistema en un total en watts.
    #
    ##Consumo del ventilador: escala con el cuadrado de la velocidad
    ##(ley de potencia de ventiladores: P ~ v²):
    ##  consumo_ventilador = COSTO_BASE * (v_actual / v_normal)²
    velocidad_ventilador_normal = DESCENSO_VENTILADOR / AREA_VENTILACION
    consumo_ventilador = COSTO_VENTILADOR_WATTS * (velocidad_ventilador / velocidad_ventilador_normal) ** 2

    consumo_refrigerante = 0
    if velocidad_refrigerante > 0:
        ##Consumo de la bomba de refrigerante: tambien escala con el cuadrado
        ##de la velocidad relativa a la velocidad de referencia (5 m/s):
        ##  consumo_refrigerante = COSTO_BASE * (v / 5)²
        consumo_refrigerante = COSTO_REFRIGERANTE_WATTS * (velocidad_refrigerante / 5) ** 2

        ##Si la presion de entrada supera la atmosferica, la bomba trabaja mas.
        ##Se aplica un factor exponencial proporcional al incremento de presion:
        ##  incremento = (P_entrada - P_atm) / P_atm
        ##  consumo_refrigerante = consumo * e^(incremento * 1.4)
        if presion_entrada > P1_REFRIGERANTE:
            incremento_presion = (presion_entrada - P1_REFRIGERANTE) / P1_REFRIGERANTE
            consumo_refrigerante = consumo_refrigerante * math.exp(incremento_presion * 1.4)

    ##Total: consumo fijo del sistema + CPU + ventilador + refrigerante (si aplica)
    total = CONSUMO_BASE_SISTEMA_WATTS + potencia_cpu + consumo_ventilador + consumo_refrigerante
    return round(total, 2)
