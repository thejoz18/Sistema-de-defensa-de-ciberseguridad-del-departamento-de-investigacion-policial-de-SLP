import random
import time

import m01_servidores       as srv
import m02_trafico_normal   as trafico
import m03_atacante         as atk
import m04_logica_matematica as lm
import m05_monitor          as mon
import m06_graficas         as graf
import m07_reporte_tabla    as tabla

## Se genera el estado inicial sin ningun dato en el sistema, nadamas se genera el dicionario inicial no se imprime
estado_actual = {
    "estado"          : "NORMAL",
    "cifrado"         : "NINGUNO",
    "refrigeracion"   : False,
    "login_bloqueado" : False,
    "ips_bloqueadas"  : [],
    "historial"       : []
}

## Creamos un variable que igual el valor con m04 donde importamos la funcion de crear estado de calculo donde basicamente tenemos un dicionario en 0
estado_calculo = lm.crear_estado_calculo()
## Definimos la total incidentes en 0 para inicializar
total_incidentes    = 0
## En consola se imprime el mensaje de inicio del programa de m05 con el mensaje de inicio
mon.imprimir_inicio(srv.centrales)
## Esta libreria basicamente genera en el sistema un segundo de intervalo para el cambio en ciclo
## Esto para que se espere antes de pasar a la siguiente instruccion, podrimoas decir que es el tiempo de espera de inicio
## Si cambiamos el valor cambia el tiempo de espera
time.sleep(1)
## Creamos la variable segundo que va a recorrer un rango de 0 a 60, podriamos aqui modificar la duracion de
## de lo que queremos simular, una vez termiando el ciclo al final del for hay un time.sleep para retrsar el ciclo un nuevo ciclo
for segundo in range(1, 61):
    ## Aqui basicamente generamos un dicionario que llamamos paquetes con datos para la simulacion, se contiene como variable
    paquete = trafico.generar_trafico_normal(segundo)
    ## En este ciclo lo que vamoas a hacer es que en base a valor del segundo de ciclo que estamos comparamos para
    ## generar un coeficiente de probabilidad para iniciar un ataque segun el rango en el ciclo
    if segundo == 1:
        prob = 0.00
    elif segundo <= 20:
        prob = 0.20
    elif segundo <= 40:
        prob = 0.40
    else:
        prob = 0.60
    ## El coeficiente se compara con un numero a lazar, si es menor, los datos de paquete se alteran con una
    ## inyeccion maliciosa al paquete
    if random.random() < prob:
        paquete          = atk.inyectar_ataque(paquete, segundo)
        ## Cada que sucede un ataque generarmos un contador para almacenar los ataques
        total_incidentes = total_incidentes + 1
    ## Suceda o no el ataque se inicia los calculos de variables para analizar los paquetes y detectar anomalias en el flujo
    metricas_calculo = lm.calcular_metricas_calculo(paquete, estado_calculo)
    ## De m04 importamos el diccionario de metricas
    ## cada calculo por separado para poder usarlo en el ciclo
    ## La tasa  mide cuanto cambiaron  los paquetes comparado con el segundo anterior
    tasa = metricas_calculo["tasa"]
    ## La primer derivada sigmoide suaviza el cambio de paquetes para analizarlo mejor
    primera_derivada_sigmoide = metricas_calculo["primera_derivada_sigmoide"]
    ## La segunda derivada sigmoide mide si el cambio se esta acelerando o frenando
    segunda_derivada_sigmoide = metricas_calculo["segunda_derivada_sigmoide"]
    ## La primera derivada guarda los el cambio de paquetes sin suavizar
    primera_derivada_paquetes = metricas_calculo["primera_derivada_paquetes"]
    ## El condicional compara el valor de tasa con el umbral de la tasa que importa desde m01, si se requiere un umbral mas o menos sensible se cambia el valor
    if tasa > srv.U_TASA:
        ## Si tasa sobre pasa el umbral en la consola se imprime una alerta
        print("  [!!] CRECIMIENTO ABRUPTO DEL TRAFICO  tasa=" + str(tasa))
    ## El condicional compara el valor de la segunda derivada con su umbral de la segunda derivada sigmoide  que importa desde m01, si se requiere un umbral mas o menos sensible se cambia el valor
    if segunda_derivada_sigmoide > srv.U_TASA:
        ## Si segunda derivada sigmoide pasa el ubmral en la consola se imprime una alerta
        print("  [!!] ACELERACION DEL TRAFICO DETECTADA  d2=" + str(segunda_derivada_sigmoide))
    ## De m04 se importa la funcion para calcular el flujo digital con paquetes, intentos login, cambios archivos, salida datos
    flujo = lm.calcular_flujo_digital(
        ## Se cargan los coeficientes a la funcion en base al diccionario
        paquete["paquetes"], paquete["intentos_login"],
        paquete["cambios_archivos"], paquete["salida_datos"]
    )

    paquete["cpu"] = lm.calcular_cpu(paquete)

    paquete["temperatura"] = lm.calcular_temperatura(paquete["cpu"])
    paquete["temperatura_sin_enfriamiento"] = paquete["temperatura"]

    senal    = lm.senal_periodica(segundo)
    desviacion_periodica, indice_oscilatorio = (
        lm.calcular_analisis_oscilatorio(
            paquete["paquetes"], senal
        )
    )

    est, alertas, protecciones, cifrado, refrig = lm.evaluar_estado(
        paquete, flujo, paquete["temperatura"], estado_actual["cifrado"],
        indice_oscilatorio
    )
    estado_actual["estado"]        = est
    estado_actual["cifrado"]       = cifrado
    estado_actual["refrigeracion"] = refrig
    paquete["direccion_registro"] = lm.generar_direccion_registro(
        paquete, estado_actual["estado"], estado_actual["cifrado"], segundo
    )
    paquete["direccion_servidor"] = lm.descifrar_direccion_registro(
        paquete["direccion_registro"], estado_actual["cifrado"]
    )

    if paquete["usuario"] not in srv.agentes_autorizados:
        if paquete["ip"] not in estado_actual["ips_bloqueadas"]:
            estado_actual["ips_bloqueadas"].append(paquete["ip"])

    if paquete["intentos_login"] > srv.U_LOGIN_CRIT:
        estado_actual["login_bloqueado"] = True

    v2, P2 = lm.calcular_refrigeracion()

    if estado_actual["refrigeracion"]:
        objetivo_termico = None
        if estado_actual["estado"] == "CRITICO":
            objetivo_termico = srv.U_TEMP_REFRIG - 1
        paquete["temperatura"] = lm.aplicar_enfriamiento(
            paquete["temperatura"], v2, lm.P1_REFRIGERANTE, P2, objetivo_termico
        )
    else:
        paquete["temperatura"] = lm.aplicar_enfriamiento_pasivo(
            paquete["temperatura"], segundo
        )
    paquete["refrigeracion_activa"] = estado_actual["refrigeracion"]
    derivada_cpu, derivada_temperatura = lm.calcular_derivadas_fisicas(
        paquete, estado_calculo
    )

    if paquete["refrigeracion_activa"]:
        refrigeracion_valor = 1
    else:
        refrigeracion_valor = 0

    if paquete["incidente"]:
        incidente_valor = 1
    else:
        incidente_valor = 0

    estado_actual["historial"].append({
        "segundo"     : segundo,
        "central"     : paquete["central"],
        "usuario"     : paquete["usuario"],
        "ip"          : paquete["ip"],
        "expediente"  : paquete["expediente"],
        "carpeta_id"  : paquete["carpeta_id"],
        "paquetes"    : paquete["paquetes"],
        "intentos_login": paquete["intentos_login"],
        "cambios_archivos": paquete["cambios_archivos"],
        "salida_datos": paquete["salida_datos"],
        "temperatura" : paquete["temperatura"],
        "temperatura_sin_enfriamiento": paquete["temperatura_sin_enfriamiento"],
        "refrigeracion_activa": refrigeracion_valor,
        "cpu"         : paquete["cpu"],
        "flujo"       : flujo,
        "primera_derivada_paquetes": primera_derivada_paquetes,
        "primera_derivada_sigmoide": primera_derivada_sigmoide,
        "segunda_derivada_sigmoide": segunda_derivada_sigmoide,
        "derivada_cpu": derivada_cpu,
        "derivada_temperatura": derivada_temperatura,
        "senal_periodica": senal,
        "desviacion_periodica": desviacion_periodica,
        "indice_oscilatorio": indice_oscilatorio,
        "incidente"   : incidente_valor,
        "tipo_incidente": paquete["tipo_incidente"],
        "estado"      : estado_actual["estado"],
        "cifrado"     : estado_actual["cifrado"],
        "direccion"   : paquete["direccion_registro"],
        "direccion_servidor": paquete["direccion_servidor"]
    })

    inc_txt = ""
    if paquete["incidente"]:
        inc_txt = "  | " + paquete["tipo_incidente"]
    mon.imprimir_ciclo(segundo, paquete, estado_actual["estado"], inc_txt)

    if segundo % 5 == 0:
        mon.imprimir_panel(
            segundo, paquete, estado_actual["estado"], estado_actual["cifrado"],
            estado_actual["refrigeracion"], tasa, flujo, v2, P2,
            senal, indice_oscilatorio, alertas, protecciones, estado_actual["ips_bloqueadas"]
        )

    time.sleep(1)

reporte_grafico = graf.generar_graficas(estado_actual["historial"])
reporte_tabular = tabla.generar_reporte_tabla(estado_actual["historial"])
mon.imprimir_resumen(
    estado_actual, estado_actual["historial"], total_incidentes,
    reporte_grafico, reporte_tabular
)
