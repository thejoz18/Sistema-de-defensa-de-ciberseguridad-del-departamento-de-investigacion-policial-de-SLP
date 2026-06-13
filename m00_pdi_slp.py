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
    # Guarda el ultimo estado importante por si al final no se desactivan protecciones
    "estado_arrastrado": "NORMAL",
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
## En consola se imprime el mensaje de inicio del programa de m05 con el mensaje de inicio con los datos del sistema
mon.imprimir_inicio(srv.centrales)
## En consola se solicita iniciar si o no para iniciar el sistema automatico
respuesta_inicio = input("Desea iniciar el programa? (si/no): ").strip().lower()
## para la respuesta si o s correra el sistema caso contrario termina el progrma
if respuesta_inicio == "si" or respuesta_inicio == "s":

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
        elif segundo >= 56:
            # En los ultimos 5 segundos bajamos ataques a cero para mostrar estabilizacion
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
        ## De m04 se importa la funcion para calcular el flujo digital con
        ## paquetes, intentos login, cambios archivos, salida datos mediante Flujo digital = 0.45P + 0.25L + 0.15A + 0.15D
        flujo = lm.calcular_flujo_digital(
            ## Se cargan los coeficientes a la funcion en base al diccionario
            paquete["paquetes"], paquete["intentos_login"],
            paquete["cambios_archivos"], paquete["salida_datos"]
        )
        ## Crea las claves de CPU, watts y temperatura con base en el flujo digital
        paquete["cpu"], paquete["potencia_cpu_watts"], paquete["temperatura"] = lm.calcular_cpu_temperatura(
            flujo, paquete["cpu_base"]
        )
    
        paquete["temperatura_sin_enfriamiento"] = paquete["temperatura"]
    
        senal    = lm.senal_periodica(segundo)
        desviacion_periodica, indice_oscilatorio = (
            lm.calcular_analisis_oscilatorio(
                paquete["paquetes"], senal
            )
        )
    
        est, alertas, protecciones, cifrado = lm.evaluar_estado(
            paquete, flujo, estado_actual["cifrado"], indice_oscilatorio
        )
        estado_actual["estado"]        = est
        if est != "NORMAL":
            # Guardamos el estado no normal para recordarlo al final
            estado_actual["estado_arrastrado"] = est
        estado_actual["cifrado"]       = cifrado
        paquete["cifrado"] = estado_actual["cifrado"]

        paquete["direccion_registro"] = lm.generar_direccion_registro(
            paquete, estado_actual["estado"], estado_actual["cifrado"], segundo
        )
        paquete["direccion_servidor"] = lm.descifrar_direccion_registro(
            paquete["direccion_registro"], estado_actual["cifrado"], estado_actual["estado"]
        )
    
        if paquete["usuario"] not in srv.agentes_autorizados:
            if paquete["ip"] not in estado_actual["ips_bloqueadas"]:
                estado_actual["ips_bloqueadas"].append(paquete["ip"])
    
        if paquete["intentos_login"] > srv.U_LOGIN_CRIT:
            estado_actual["login_bloqueado"] = True
    
        refrigeracion_activa = paquete["temperatura"] >= srv.U_TEMP_REFRIG
        velocidad_ventilador, descenso_ventilador = lm.calcular_ventilador(paquete["temperatura"], refrigeracion_activa)
        paquete["temperatura"] = round(max(paquete["temperatura"] - descenso_ventilador, 28), 1)

        v2, P1, P2, descenso_refrigerante = 0, lm.P1_REFRIGERANTE, lm.P1_REFRIGERANTE, 0
        if refrigeracion_activa:
            v2, P1, P2, descenso_refrigerante = lm.calcular_refrigeracion(paquete["temperatura"],
                                                                          estado_actual["estado"])
            paquete["temperatura"] = round(max(paquete["temperatura"] - descenso_refrigerante, 28), 1)

        estado_actual["refrigeracion"] = refrigeracion_activa

        if paquete["temperatura_sin_enfriamiento"] >= srv.U_TEMP_CRITICA:
            alertas.append("TEMPERATURA CRITICA: " + str(paquete["temperatura_sin_enfriamiento"]) + " C")
            protecciones.append("REFRIGERACION ACTIVADA")
        if refrigeracion_activa:
            protecciones.append("REFRIGERACION PREVENTIVA ACTIVADA")
            if estado_actual["estado"] == "CRITICO":
                protecciones.append("BOMBAS CRITICAS PREPARADAS")
        paquete["velocidad_ventilador"] = velocidad_ventilador
        paquete["descenso_ventilador"] = descenso_ventilador
        consumo_enfriamiento_watts = lm.calcular_consumo_watts(
            paquete["potencia_cpu_watts"], velocidad_ventilador, v2, P1
        )
        incremento_presion_porcentaje = round(
            ((P1 - lm.P1_REFRIGERANTE) / lm.P1_REFRIGERANTE) * 100, 2
        )
        paquete["consumo_enfriamiento_watts"] = consumo_enfriamiento_watts
        paquete["consumo_total_watts"] = consumo_enfriamiento_watts
        paquete["incremento_presion_porcentaje"] = incremento_presion_porcentaje
        paquete["descenso_refrigerante"] = descenso_refrigerante
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
            "velocidad_ventilador": velocidad_ventilador,
            "velocidad_refrigerante": v2,
            "presion_entrada_refrigerante": P1,
            "presion_salida_refrigerante": P2,
            "presion_refrigerante": P1,
            "incremento_presion_porcentaje": incremento_presion_porcentaje,
            "potencia_cpu_watts": paquete["potencia_cpu_watts"],
            "consumo_enfriamiento_watts": consumo_enfriamiento_watts,
            "consumo_total_watts": consumo_enfriamiento_watts,
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
            "tipo_incidente": paquete.get("tipo_incidente", "NINGUNO"),
            "estado"      : estado_actual["estado"],
            "cifrado"     : estado_actual["cifrado"],
            "direccion"   : paquete["direccion_registro"],
            "direccion_servidor": paquete["direccion_servidor"]
        })
    
        inc_txt = ""
        if paquete["incidente"]:
            inc_txt = "  | " + paquete.get("tipo_incidente", "NINGUNO")
        mon.imprimir_ciclo(segundo, paquete, estado_actual["estado"], inc_txt)
    
        if segundo % 5 == 0:
            ultimos_cinco = estado_actual["historial"][-5:]
            total_paquetes = 0
            total_login = 0
            total_cambios = 0
            total_salida = 0
            total_cpu = 0
            suma_primera_derivada = 0
            suma_segunda_derivada = 0
            suma_flujo = 0
            suma_senal = 0
            suma_indice = 0
            suma_aumento_presion = 0

            for h in estado_actual["historial"]:
                total_paquetes = total_paquetes + h["paquetes"]
                total_login = total_login + h["intentos_login"]
                total_cambios = total_cambios + h["cambios_archivos"]
                total_salida = total_salida + h["salida_datos"]
                total_cpu = total_cpu + h["cpu"]

            for h in ultimos_cinco:
                suma_primera_derivada = suma_primera_derivada + h["primera_derivada_sigmoide"]
                suma_segunda_derivada = suma_segunda_derivada + h["segunda_derivada_sigmoide"]
                suma_flujo = suma_flujo + h["flujo"]
                suma_senal = suma_senal + h["senal_periodica"]
                suma_indice = suma_indice + h["indice_oscilatorio"]
                suma_aumento_presion = suma_aumento_presion + h["incremento_presion_porcentaje"]

            cantidad_promedio = len(ultimos_cinco)
            if cantidad_promedio == 0:
                cantidad_promedio = 1
            cantidad_total = len(estado_actual["historial"])
            if cantidad_total == 0:
                cantidad_total = 1

            paquete["total_paquetes_acumulado"] = total_paquetes
            paquete["total_login_acumulado"] = total_login
            paquete["total_cambios_acumulado"] = total_cambios
            paquete["total_salida_acumulado"] = total_salida
            paquete["cpu_promedio_acumulado"] = round(total_cpu / cantidad_total, 1)
            paquete["prom_primera_derivada_5"] = round(suma_primera_derivada / cantidad_promedio, 2)
            paquete["prom_segunda_derivada_5"] = round(suma_segunda_derivada / cantidad_promedio, 2)
            paquete["prom_flujo_5"] = round(suma_flujo / cantidad_promedio, 2)
            paquete["prom_senal_5"] = round(suma_senal / cantidad_promedio, 2)
            paquete["prom_indice_5"] = round(suma_indice / cantidad_promedio, 2)
            paquete["aumento_presion_5"] = round(suma_aumento_presion, 2)

            mon.imprimir_panel(
                segundo, paquete, estado_actual["estado"], estado_actual["cifrado"],
                estado_actual["refrigeracion"], primera_derivada_sigmoide,
                segunda_derivada_sigmoide, flujo, v2, P1, P2,
                senal, indice_oscilatorio, alertas, protecciones, estado_actual["ips_bloqueadas"]
            )
    
        time.sleep(1)

    # Preguntamos si al final se quieren apagar las protecciones y dejar normal
    respuesta_estabilizar = input("Sistema estabilizado. Quiere desactivar las protecciones? (si/no): ").strip().lower()
    # Si responde si o s, dejamos el estado final como normal
    if respuesta_estabilizar == "si" or respuesta_estabilizar == "s":
        estado_actual["estado"] = "NORMAL"
        estado_actual["refrigeracion"] = False
    # Si responde cualquier otra cosa, se queda el estado que venia arrastrando
    else:
        estado_actual["estado"] = estado_actual["estado_arrastrado"]

    reporte_grafico = graf.generar_graficas(estado_actual["historial"])
    reporte_tabular = tabla.generar_reporte_tabla(estado_actual["historial"])
    mon.imprimir_resumen(
        estado_actual, estado_actual["historial"], total_incidentes,
        reporte_grafico, reporte_tabular
    )
else:
    print("Programa finalizado")
