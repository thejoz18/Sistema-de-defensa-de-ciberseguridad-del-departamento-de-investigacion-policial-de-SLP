##Este modulo solo imprime informacion en pantalla.
##No calcula datos nuevos, recibe valores ya preparados por los otros modulos.

##Esta funcion imprime la pantalla de inicio del sistema.
def imprimir_inicio(centrales):
    ##Imprimimos una linea vacia para separar visualmente.
    print("")
    ##Imprimimos una linea decorativa.
    print("=" * 54)
    ##Imprimimos el nombre del sistema.
    print("  PDI SLP - CYBER DEFENSE SYSTEM")
    ##Imprimimos el departamento.
    print("  Departamento de Ciberseguridad")
    ##Imprimimos la institucion del proyecto.
    print("  Policia de Investigacion  |  San Luis Potosi")
    ##Imprimimos una linea vacia para separar.
    print("")
    ##Imprimimos el titulo de las centrales.
    print("  Centrales monitoreadas:")
    ##Recorremos las centrales que llegan desde m01.
    for c in centrales:
        ##Imprimimos una central por renglon.
        print("    - " + c)
    ##Imprimimos una linea vacia.
    print("")
    ##Imprimimos la duracion de la simulacion.
    print("  Duracion: 60 ciclos  |  1 ciclo por segundo")
    ##Cerramos el recuadro de inicio.
    print("=" * 54)
    ##Dejamos otro espacio antes del input.
    print("")

##Esta funcion imprime la informacion de un segundo de la simulacion.
def imprimir_ciclo(segundo, paquete, estado, inc_txt):
    ##Obtenemos el tipo de cifrado del paquete, y si no existe usamos NINGUNO.
    cifrado = paquete.get("cifrado", "NINGUNO")
    ##Si el estado es critico o el cifrado es reforzado, la ruta se muestra como reforzada.
    if estado == "CRITICO" or cifrado == "REFORZADO":
        ##Guardamos la etiqueta para la ruta reforzada.
        nivel_registro = "Reforzado"
    ##Si el estado es alerta, sospechoso o cifrado, la ruta se muestra como cifrada.
    elif estado == "ALERTA" or estado == "SOSPECHOSO" or cifrado == "CIFRADO":
        ##Guardamos la etiqueta para la ruta cifrada.
        nivel_registro = "Cifrado"
    ##Si no hay riesgo, la ruta se muestra normal.
    else:
        ##Guardamos la etiqueta para la ruta normal.
        nivel_registro = "Normal"

    ##Dejamos un salto antes de imprimir el ciclo.
    print("")
    ##Imprimimos el resumen principal del ciclo actual.
    print("  CICLO " + str(segundo).zfill(2) +
          "  [" + estado + "]" +
          "  paq=" + str(paquete["paquetes"]) +
          "  datos=" + str(paquete["salida_datos"]) + "MB" +
          "  login=" + str(paquete["intentos_login"]) +
          "  cambios=" + str(paquete["cambios_archivos"]) +
          inc_txt)
    ##Imprimimos datos generales del paquete.
    print("    Central: " + paquete["central"] +
          "  |  Expediente: " + paquete["carpeta_id"] +
          "  |  Agente: " + paquete["usuario"] +
          "  |  IP: " + paquete["ip"])
    ##Imprimimos la ruta interna normal o cifrada.
    print("    " + nivel_registro + ": " + paquete["direccion_registro"])
    ##Imprimimos la ruta del servidor ya descifrada.
    print("    Servidor: " + paquete["direccion_servidor"])

##Esta funcion imprime un panel mas grande cada 5 segundos.
def imprimir_panel(segundo, paquete, estado, cifrado, refrig,
                   primera_derivada_sigmoide, segunda_derivada_sigmoide,
                   flujo, v2, P1, P2, senal, indice_oscilatorio,
                   alertas, protecciones, ips_bloqueadas):
    ##Aqui preparamos textos y conversiones antes de imprimir el panel.
    ##Convertimos los segundos a minutos.
    minutos = segundo // 60
    ##Obtenemos los segundos sobrantes.
    segs    = segundo % 60
    ##Formamos el reloj en formato 00:00.
    reloj   = str(minutos).zfill(2) + ":" + str(segs).zfill(2)
    ##Convertimos la temperatura de Celsius a Kelvin.
    kelvin  = round(paquete["temperatura"] + 273.15, 2)
    ##Revisamos si la refrigeracion esta activa.
    if refrig:
        ##Guardamos el texto cuando la refrigeracion esta activa.
        texto_refrigeracion = "ACTIVA"
    ##Si no esta activa, guardamos el texto contrario.
    else:
        ##Guardamos el texto cuando la refrigeracion esta inactiva.
        texto_refrigeracion = "INACTIVA"

    ##Dejamos un espacio antes del panel.
    print("")
    ##Abrimos el panel con una linea decorativa.
    print("=" * 54)
    ##Imprimimos el nombre del sistema.
    print("  PDI SLP - CYBER DEFENSE SYSTEM")
    ##Imprimimos el departamento.
    print("  Dept. de Ciberseguridad  |  San Luis Potosi")
    ##Cerramos el encabezado del panel.
    print("=" * 54)
    ##Imprimimos el titulo de datos globales.
    print("  -- DATOS GLOBALES --")
    ##Imprimimos el tiempo actual.
    print("  Tiempo             : 00:" + reloj)
    ##Imprimimos el estado operativo actual.
    print("  Estado operativo   : " + estado)
    ##Imprimimos el cifrado activo.
    print("  Cifrado activo     : " + cifrado)
    ##Imprimimos si la refrigeracion esta activa o no.
    print("  Refrigeracion      : " + texto_refrigeracion)
    ##Imprimimos paquetes acumulados hasta el momento.
    print("  Paquetes total     : " + str(paquete.get("total_paquetes_acumulado", paquete["paquetes"])))
    ##Imprimimos logins acumulados hasta el momento.
    print("  Login total        : " + str(paquete.get("total_login_acumulado", paquete["intentos_login"])))
    ##Imprimimos cambios acumulados hasta el momento.
    print("  Cambios total      : " + str(paquete.get("total_cambios_acumulado", paquete["cambios_archivos"])))
    ##Imprimimos salida de datos acumulada hasta el momento.
    print("  Salida total       : " + str(paquete.get("total_salida_acumulado", paquete["salida_datos"])) + " MB")
    ##Imprimimos el promedio acumulado de CPU.
    print("  CPU prom. acum.    : " + str(paquete.get("cpu_promedio_acumulado", paquete["cpu"])) + " %")
    ##Imprimimos cuantas IPs se han bloqueado.
    print("  IPs bloqueadas     : " + str(len(ips_bloqueadas)))
    ##Imprimimos el consumo total del ciclo.
    print("  Consumo total      : " + str(paquete.get("consumo_total_watts", 0)) + " W watts")
    ##Dejamos un espacio antes del estado del sistema.
    print("")
    ##Imprimimos el titulo del estado del sistema.
    print("  -- ESTADO DEL SISTEMA --")
    ##Imprimimos el promedio de la primera derivada sigmoide de los ultimos ciclos.
    print("  Tasa cambio P'(t)  : " + str(paquete.get("prom_primera_derivada_5", primera_derivada_sigmoide)))
    ##Imprimimos el promedio de la segunda derivada sigmoide de los ultimos ciclos.
    print("  Aceleracion P''(t) : " + str(paquete.get("prom_segunda_derivada_5", segunda_derivada_sigmoide)))
    ##Imprimimos el promedio de flujo digital.
    print("  Prom. flujo digital: " + str(paquete.get("prom_flujo_5", flujo)))
    ##Imprimimos el promedio de la senal periodica.
    print("  Prom. senal period.: " + str(paquete.get("prom_senal_5", senal)))
    ##Imprimimos el promedio del indice oscilatorio.
    print("  Prom. oscilatorio  : " + str(paquete.get("prom_indice_5", indice_oscilatorio)))
    ##Dejamos un espacio antes del estado fisico.
    print("")
    ##Imprimimos el titulo del estado fisico.
    print("  -- ESTADO FISICO DEL HARDWARE --")
    ##Imprimimos el CPU actual.
    print("  CPU                : " + str(paquete["cpu"]) + " %")
    ##Imprimimos la potencia del CPU.
    print("  Potencia CPU       : " + str(paquete.get("potencia_cpu_watts", 0)) + " W")
    ##Imprimimos la temperatura en Celsius y Kelvin.
    print("  Temperatura        : " + str(paquete["temperatura"]) + " C  /  " + str(kelvin) + " K")
    ##Si hay refrigeracion, mostramos velocidad del refrigerante.
    if refrig:
        ##Imprimimos la velocidad de refrigeracion.
        print("  Vel. refrigeracion : " + str(v2) + " m/s")
    ##Si no hay refrigeracion, mostramos velocidad del ventilador.
    else:
        ##Imprimimos la velocidad del ventilador.
        print("  Vel. ventilador    : " + str(paquete.get("velocidad_ventilador", 0)) + " m/s")
    ##Imprimimos la presion de entrada.
    print("  Presion entrada    : " + str(P1) + " Pa")
    ##Imprimimos la presion de salida.
    print("  Presion salida     : " + str(P2) + " Pa")
    ##Imprimimos el aumento de presion acumulado en los ultimos cinco ciclos.
    print("  Aum. presion 5 cic.: " + str(paquete.get("aumento_presion_5", paquete.get("incremento_presion_porcentaje", 0))) + " %")
    ##Dejamos un espacio antes de alertas.
    print("")
    ##Revisamos si existen alertas para imprimirlas.
    if len(alertas) > 0:
        ##Imprimimos el titulo de alertas.
        print("  -- ALERTAS OPERATIVAS --")
        ##Recorremos cada alerta.
        for a in alertas:
            ##Imprimimos la alerta.
            print("  [!] " + a)
        ##Dejamos un espacio despues de alertas.
        print("")
    ##Revisamos si existen protecciones para imprimirlas.
    if len(protecciones) > 0:
        ##Imprimimos el titulo de protecciones.
        print("  -- PROTECCIONES ACTIVADAS --")
        ##Recorremos cada proteccion.
        for p in protecciones:
            ##Imprimimos la proteccion.
            print("  [OK] " + p)
        ##Dejamos un espacio despues de protecciones.
        print("")
    ##Cerramos el panel.
    print("=" * 54)
    ##Dejamos un espacio final.
    print("")

##Esta funcion imprime el reporte final en consola.
def imprimir_resumen(estado_actual, historial, total_incidentes, reporte_grafico, reporte_tabular=""):
    ##Revisamos si el login remoto quedo bloqueado.
    if estado_actual["login_bloqueado"]:
        ##Guardamos texto de login cerrado.
        texto_login = "CERRADO"
    ##Si no esta bloqueado, queda abierto.
    else:
        ##Guardamos texto de login abierto.
        texto_login = "ABIERTO"

    ##Revisamos si la refrigeracion termino activa.
    if estado_actual["refrigeracion"]:
        ##Guardamos texto de refrigeracion activa.
        texto_refrigeracion = "ACTIVA"
    ##Si no termino activa, se muestra inactiva.
    else:
        ##Guardamos texto de refrigeracion inactiva.
        texto_refrigeracion = "INACTIVA"

    ##Dejamos un espacio antes del resumen.
    print("")
    ##Abrimos el resumen final.
    print("=" * 54)
    ##Imprimimos titulo del reporte final.
    print("  REPORTE FINAL  |  PDI SLP - CYBER DEFENSE SYSTEM")
    ##Cerramos encabezado.
    print("=" * 54)
    ##Imprimimos cantidad de ciclos ejecutados.
    print("  Ciclos ejecutados  : " + str(len(historial)))
    ##Imprimimos total de incidentes.
    print("  Incidentes detect. : " + str(total_incidentes))
    ##Imprimimos total de IPs bloqueadas.
    print("  IPs bloqueadas     : " + str(len(estado_actual["ips_bloqueadas"])))
    ##Imprimimos estado final.
    print("  Estado final       : " + estado_actual["estado"])
    ##Imprimimos cifrado activo.
    print("  Cifrado activo     : " + estado_actual["cifrado"])
    ##Imprimimos estado del login remoto.
    print("  Login remoto       : " + texto_login)
    ##Imprimimos estado de refrigeracion.
    print("  Refrigeracion      : " + texto_refrigeracion)
    ##Dejamos un espacio antes del cierre.
    print("")
    ##Imprimimos mensaje de simulacion terminada.
    print("  SIMULACION TERMINADA")
    ##Revisamos que el historial tenga datos para calcular totales.
    if len(historial) > 0:
        ##Iniciamos total de paquetes.
        suma_paquetes = 0
        ##Iniciamos total de login.
        suma_login = 0
        ##Iniciamos total de cambios.
        suma_cambios = 0
        ##Iniciamos total de salida de datos.
        suma_salida = 0
        ##Iniciamos total de consumo.
        suma_consumo = 0
        ##Iniciamos suma de CPU para calcular promedio.
        suma_cpu = 0
        ##Recorremos cada segundo guardado en el historial.
        for h in historial:
            ##Sumamos paquetes.
            suma_paquetes = suma_paquetes + h["paquetes"]
            ##Sumamos intentos de login.
            suma_login = suma_login + h["intentos_login"]
            ##Sumamos cambios de archivos.
            suma_cambios = suma_cambios + h["cambios_archivos"]
            ##Sumamos salida de datos.
            suma_salida = suma_salida + h["salida_datos"]
            ##Sumamos consumo total.
            suma_consumo = suma_consumo + h["consumo_total_watts"]
            ##Sumamos CPU.
            suma_cpu = suma_cpu + h["cpu"]

        ##Calculamos el promedio de CPU.
        cpu_prom  = suma_cpu / len(historial)
        ##Dejamos un espacio antes de los totales.
        print("")
        ##Imprimimos paquetes totales.
        print("  Paquetes totales   : " + str(suma_paquetes))
        ##Imprimimos login totales.
        print("  Login totales      : " + str(suma_login))
        ##Imprimimos cambios totales.
        print("  Cambios totales    : " + str(suma_cambios))
        ##Imprimimos salidas totales.
        print("  Salidas totales    : " + str(suma_salida) + " MB")
        ##Imprimimos IPs bloqueadas totales.
        print("  IPs bloq. totales  : " + str(len(estado_actual["ips_bloqueadas"])))
        ##Imprimimos consumo total.
        print("  Consumo total      : " + str(round(suma_consumo, 2)) + " W")
        ##Imprimimos CPU promedio.
        print("  CPU prom.          : " + str(round(cpu_prom,  1)) + " %")
    ##Dejamos un espacio antes de rutas de salida.
    print("")
    ##Imprimimos la carpeta de graficas.
    print("  Reporte grafico    : " + reporte_grafico)
    ##Revisamos si hay reporte tabular.
    if reporte_tabular != "":
        ##Imprimimos la ruta del reporte tabular.
        print("  Reporte tabular    : " + reporte_tabular)
    ##Dejamos un espacio antes del cierre.
    print("")
    ##Cerramos el resumen final.
    print("=" * 54)
    ##Dejamos un espacio final.
    print("")
