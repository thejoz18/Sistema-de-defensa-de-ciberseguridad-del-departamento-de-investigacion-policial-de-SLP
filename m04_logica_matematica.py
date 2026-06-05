import math
import m01_servidores as srv

A1_REFRIGERANTE = 0.05
A2_REFRIGERANTE = 0.02
V1_REFRIGERANTE = 2.0
P1_REFRIGERANTE = 101325
RHO_REFRIGERANTE = 1000

def crear_estado_calculo():
    return {
        "paquetes_anteriores": 0,
        "temperatura_anterior": 0,
        "cpu_anterior": 0,
        "primera_derivada_sigmoide_anterior": 0
    }

def calcular_metricas_calculo(paquete, estado_calculo):
    tasa = calcular_tasa(paquete["paquetes"], estado_calculo["paquetes_anteriores"])
    primera_derivada_paquetes = calcular_derivada_discreta(
        paquete["paquetes"], estado_calculo["paquetes_anteriores"]
    )
    primera_derivada_sigmoide = aplicar_sigmoide_derivada(primera_derivada_paquetes, srv.U_TASA)
    segunda_derivada_sigmoide = calcular_segunda_derivada(
        primera_derivada_sigmoide, estado_calculo["primera_derivada_sigmoide_anterior"]
    )
    segunda_derivada_sigmoide = aplicar_sigmoide_derivada(
        segunda_derivada_sigmoide, srv.U_TASA
    )
    estado_calculo["paquetes_anteriores"] = paquete["paquetes"]
    estado_calculo["primera_derivada_sigmoide_anterior"] = primera_derivada_sigmoide

    return {
        "tasa": tasa,
        "primera_derivada_sigmoide": primera_derivada_sigmoide,
        "segunda_derivada_sigmoide": segunda_derivada_sigmoide,
        "primera_derivada_paquetes": primera_derivada_paquetes
    }

def calcular_derivadas_fisicas(paquete, estado_calculo):
    derivada_cpu = calcular_derivada_discreta(paquete["cpu"], estado_calculo["cpu_anterior"])
    derivada_temperatura = calcular_derivada_discreta(
        paquete["temperatura"], estado_calculo["temperatura_anterior"]
    )

    estado_calculo["cpu_anterior"] = paquete["cpu"]
    estado_calculo["temperatura_anterior"] = paquete["temperatura"]

    return derivada_cpu, derivada_temperatura

def calcular_tasa(actual, anterior):
    return actual - anterior

def calcular_derivada_discreta(actual, anterior, delta_t=1):
    if delta_t == 0:
        return 0
    return round((actual - anterior) / delta_t, 2)

def calcular_sigmoide(x):
    if x >= 0:
        z = math.exp(-x)
        return 1 / (1 + z)
    z = math.exp(x)
    return z / (1 + z)

def aplicar_sigmoide_derivada(valor, escala=srv.U_TASA, k=6):
    if escala == 0:
        escala = 1
    factor = calcular_sigmoide(k * valor / escala)
    return round(valor * factor, 2)

def calcular_segunda_derivada(derivada_actual, derivada_anterior, delta_t=1):
    if delta_t == 0:
        return 0
    return round((derivada_actual - derivada_anterior) / delta_t, 2)

def calcular_flujo_digital(paquetes, intentos_login, cambios_archivos, salida_datos):
    return round(paquetes * 0.45 + intentos_login * 0.25 +
                 cambios_archivos * 0.15 + salida_datos * 0.15, 2)

def evaluar_estado(paquete, flujo, temperatura, cifrado_actual, indice_oscilatorio):
    alertas      = []
    protecciones = []
    estado       = "NORMAL"
    cifrado      = cifrado_actual
    refrigeracion = False

    if paquete["usuario"] not in srv.agentes_autorizados:
        alertas.append("ACCESO NO AUTORIZADO: " + paquete["usuario"])
        estado = "ALERTA"

    if paquete["paquetes"] > srv.U_PAQUETES_ALERTA and paquete["intentos_login"] > srv.U_LOGIN_ALERTA:
        alertas.append("TRAFICO MASIVO + FUERZA BRUTA")
        estado = "ALERTA"
        if cifrado == "NINGUNO":
            cifrado = "CIFRADO"
            protecciones.append("CIFRADO ACTIVADO")

    if paquete["cambios_archivos"] > srv.U_CAMBIOS:
        alertas.append("MANIPULACION DE EXPEDIENTE DETECTADA")
        if estado != "CRITICO":
            estado = "ALERTA"

    if paquete["salida_datos"] > srv.U_SALIDA_DATOS:
        alertas.append("SALIDA DE DATOS ELEVADA: " + str(paquete["salida_datos"]) + " MB")
        if cifrado == "NINGUNO":
            cifrado = "CIFRADO"
            protecciones.append("CIFRADO POR SALIDA DE DATOS")

    if paquete["paquetes"] > srv.U_PAQUETES_CRIT or flujo > srv.U_FLUJO_CRITICO:
        estado  = "CRITICO"
        cifrado = "REFORZADO"
        alertas.append("FLUJO O TRAFICO CRITICO")
        protecciones.append("CIFRADO REFORZADO ACTIVADO")

    if indice_oscilatorio > srv.U_OSCILACION_CRIT:
        estado = "CRITICO"
        cifrado = "REFORZADO"
        alertas.append("DESVIACION OSCILATORIA CRITICA")
        protecciones.append("ANALISIS OSCILATORIO REGISTRADO")

    elif indice_oscilatorio > srv.U_OSCILACION_SOSP and estado == "NORMAL":
        estado = "SOSPECHOSO"

    if temperatura >= srv.U_TEMP_CRITICA:
        estado = "CRITICO"
        alertas.append("TEMPERATURA CRITICA: " + str(temperatura) + " C")
        refrigeracion = True
        protecciones.append("REFRIGERACION ACTIVADA")

    elif temperatura >= srv.U_TEMP_REFRIG and not refrigeracion:
        refrigeracion = True
        protecciones.append("REFRIGERACION PREVENTIVA ACTIVADA")

    if paquete["intentos_login"] > srv.U_LOGIN_CRIT:
        alertas.append("FUERZA BRUTA CRITICA")
        protecciones.append("LOGIN REMOTO CERRADO")

    if len(alertas) == 0:
        if (paquete["paquetes"] > srv.U_PAQUETES_SOSP or
                paquete["intentos_login"] > 4 or
                indice_oscilatorio > srv.U_OSCILACION_SOSP):
            estado = "SOSPECHOSO"

    return estado, alertas, protecciones, cifrado, refrigeracion

def cifrado_cesar(texto, d):
    resultado = ""
    for c in texto:
        if c.isalpha():
            if c.isupper():
                base = ord('A')
            else:
                base = ord('a')
            resultado = resultado + chr((ord(c) - base + d) % 26 + base)
        else:
            resultado = resultado + c
    return resultado

def obtener_inverso_modular(clave, modulo):
    for posible in range(1, modulo):
        if (clave * posible) % modulo == 1:
            return posible
    return None

def descifrado_cesar(texto, d):
    return cifrado_cesar(texto, -d)

def cifrado_multiplicativo(texto, clave_letras=5, clave_numeros=7, ajuste_numeros=3):
    resultado = ""
    for c in texto:
        if c.isalpha():
            if c.isupper():
                base = ord('A')
            else:
                base = ord('a')
            posicion = ord(c) - base
            nueva_posicion = (posicion * clave_letras) % 26
            resultado = resultado + chr(nueva_posicion + base)
        elif c.isdigit():
            posicion = int(c)
            nueva_posicion = (posicion * clave_numeros + ajuste_numeros) % 10
            resultado = resultado + str(nueva_posicion)
        else:
            resultado = resultado + c
    return resultado

def descifrado_multiplicativo(texto, clave_letras=5, clave_numeros=7, ajuste_numeros=3):
    resultado = ""
    inverso_letras = obtener_inverso_modular(clave_letras, 26)
    inverso_numeros = obtener_inverso_modular(clave_numeros, 10)
    for c in texto:
        if c.isalpha() and inverso_letras is not None:
            if c.isupper():
                base = ord('A')
            else:
                base = ord('a')
            posicion = ord(c) - base
            nueva_posicion = (posicion * inverso_letras) % 26
            resultado = resultado + chr(nueva_posicion + base)
        elif c.isdigit() and inverso_numeros is not None:
            posicion = int(c)
            nueva_posicion = ((posicion - ajuste_numeros) * inverso_numeros) % 10
            resultado = resultado + str(nueva_posicion)
        else:
            resultado = resultado + c
    return resultado

def cifrado_reforzado(texto):
    paso1 = cifrado_cesar(texto, 3)
    paso2 = cifrado_multiplicativo(paso1)
    return paso2

def descifrado_reforzado(texto):
    paso1 = descifrado_multiplicativo(texto)
    paso2 = descifrado_cesar(paso1, 3)
    return paso2

def generar_direccion_registro(paquete, estado, cifrado, segundo):
    central = paquete["central"].lower()
    carpeta = paquete["carpeta_id"].lower()
    nombre_base = "datos_" + str(segundo).zfill(2) + ".log"

    if estado == "CRITICO" or cifrado == "REFORZADO":
        nombre_seguro = cifrado_reforzado(nombre_base)
        return "registro_reforzado://" + central + "/" + carpeta + "/" + nombre_seguro

    if estado == "ALERTA" or estado == "SOSPECHOSO" or cifrado == "CIFRADO":
        nombre_seguro = cifrado_cesar(nombre_base, 3)
        return "registro_seguro://" + central + "/" + carpeta + "/" + nombre_seguro

    return "registro_local://" + central + "/" + carpeta + "/" + nombre_base

def descifrar_direccion_registro(direccion, cifrado):
    partes = direccion.split("/")
    nombre = partes[len(partes) - 1]

    if cifrado == "REFORZADO":
        nombre = descifrado_reforzado(nombre)
    elif cifrado == "CIFRADO":
        nombre = descifrado_cesar(nombre, 3)

    partes[len(partes) - 1] = nombre
    return "/".join(partes)

def calcular_cpu(paquete):
    actividad = (paquete["paquetes"]         +
                 paquete["intentos_login"]    * 45 +
                 paquete["cambios_archivos"]  * 28 +
                 paquete["salida_datos"]      * 18)
    cpu = paquete["cpu_base"] + 0.005 * actividad
    if cpu > 100:
        cpu = 100
    return round(cpu, 1)

def calcular_temperatura(cpu, temp_ambiente=28, k=0.58):
    return round(temp_ambiente + k * cpu, 1)

def calcular_velocidad_refrigerante(area_1, velocidad_1, area_2):
    if area_2 == 0:
        return 0.0
    return round((area_1 * velocidad_1) / area_2, 4)

def calcular_presion_bernoulli(presion_1, densidad, velocidad_1, velocidad_2):
    return round(presion_1 + 0.5 * densidad * velocidad_1**2
                           - 0.5 * densidad * velocidad_2**2, 2)

def calcular_refrigeracion():
    v2 = calcular_velocidad_refrigerante(A1_REFRIGERANTE, V1_REFRIGERANTE, A2_REFRIGERANTE)
    P2 = calcular_presion_bernoulli(P1_REFRIGERANTE, RHO_REFRIGERANTE, V1_REFRIGERANTE, v2)
    return v2, P2

def calcular_descenso_bernoulli(velocidad_refrigerante, presion_inicial, presion_final, coef=4.4):
    if presion_inicial <= 0:
        return 0
    caida_relativa = max((presion_inicial - presion_final) / presion_inicial, 0)
    return round(coef * velocidad_refrigerante * caida_relativa, 2)

def aplicar_enfriamiento_pasivo(temperatura, segundo, intervalo=5, descenso=1.0):
    if segundo % intervalo != 0:
        return temperatura
    nueva = temperatura - descenso
    if nueva < 28:
        nueva = 28
    return round(nueva, 1)

def aplicar_enfriamiento(temperatura, velocidad_refrigerante, presion_inicial, presion_final,
                         objetivo=None):
    descenso = calcular_descenso_bernoulli(
        velocidad_refrigerante, presion_inicial, presion_final
    )
    if objetivo is not None and temperatura - descenso > objetivo:
        descenso = temperatura - objetivo
    nueva = temperatura - descenso
    if nueva < 28:
        nueva = 28
    return round(nueva, 1)

def senal_periodica(t, A=45, B=18, w=0.3):
    return round(A * math.sin(w * t) + B * math.cos(w * t), 2)

def calcular_analisis_oscilatorio(paquetes, senal):
    desviacion_periodica = round(abs(paquetes - senal), 2)
    indice_oscilatorio = desviacion_periodica
    return desviacion_periodica, indice_oscilatorio
