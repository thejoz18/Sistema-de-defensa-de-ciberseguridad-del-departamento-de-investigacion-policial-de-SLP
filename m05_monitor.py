def imprimir_inicio(centrales):
    print("")
    print("=" * 54)
    print("  PDI SLP - CYBER DEFENSE SYSTEM")
    print("  Departamento de Ciberseguridad")
    print("  Policia de Investigacion  |  San Luis Potosi")
    print("")
    print("  Centrales monitoreadas:")
    for c in centrales:
        print("    · " + c)
    print("")
    print("  Duracion: 60 ciclos  |  1 ciclo por segundo")
    print("=" * 54)
    print("")

def imprimir_ciclo(segundo, paquete, estado, inc_txt):
    print("  CICLO " + str(segundo).zfill(2) +
          "  " + paquete["central"] +
          "  [" + estado + "]" +
          "  paq=" + str(paquete["paquetes"]) +
          "  datos=" + str(paquete["salida_datos"]) + "MB" +
          "  cpu=" + str(paquete["cpu"]) + "%" +
          "  temp=" + str(paquete["temperatura"]) + "C" +
          "  dir=" + paquete["direccion_registro"] +
          inc_txt)

def imprimir_panel(segundo, paquete, estado, cifrado, refrig,
                   tasa, flujo, v2, P2, senal, indice_oscilatorio,
                   alertas, protecciones, ips_bloqueadas):
    minutos = segundo // 60
    segs    = segundo % 60
    reloj   = str(minutos).zfill(2) + ":" + str(segs).zfill(2)
    kelvin  = round(paquete["temperatura"] + 273.15, 2)
    if refrig:
        texto_refrigeracion = "ACTIVA"
    else:
        texto_refrigeracion = "INACTIVA"

    print("")
    print("=" * 54)
    print("  PDI SLP - CYBER DEFENSE SYSTEM")
    print("  Dept. de Ciberseguridad  |  San Luis Potosi")
    print("=" * 54)
    print("  Tiempo             : 00:" + reloj)
    print("  Estado operativo   : " + estado)
    print("  Cifrado activo     : " + cifrado)
    print("  Refrigeracion      : " + texto_refrigeracion)
    print("")
    print("  Central            : " + paquete["central"])
    print("  Expediente         : " + paquete["carpeta_id"])
    print("  Agente             : " + paquete["usuario"])
    print("  IP                 : " + paquete["ip"])
    print("")
    print("  Paquetes/s         : " + str(paquete["paquetes"]))
    print("  Intentos login     : " + str(paquete["intentos_login"]))
    print("  Cambios archivos   : " + str(paquete["cambios_archivos"]))
    print("  Salida datos       : " + str(paquete["salida_datos"]) + " MB")
    print("  Direccion registro : " + paquete["direccion_registro"])
    print("  CPU                : " + str(paquete["cpu"]) + " %")
    print("  Temperatura        : " + str(paquete["temperatura"]) + " C  /  " + str(kelvin) + " K")
    print("")
    print("  Tasa de cambio     : " + str(tasa))
    print("  Flujo digital      : " + str(flujo))
    print("  Vel. refrigerante  : " + str(v2) + " m/s")
    print("  Presion refrig.    : " + str(P2) + " Pa")
    print("  Senal periodica    : " + str(senal))
    print("  Indice oscilatorio : " + str(indice_oscilatorio))
    print("")
    if len(alertas) > 0:
        print("  -- ALERTAS OPERATIVAS --")
        for a in alertas:
            print("  [!] " + a)
        print("")
    if len(protecciones) > 0:
        print("  -- PROTECCIONES ACTIVADAS --")
        for p in protecciones:
            print("  [OK] " + p)
        print("")
    if len(ips_bloqueadas) > 0:
        print("  IPs bloqueadas     : " + str(len(ips_bloqueadas)))
    print("=" * 54)
    print("")

def imprimir_resumen(estado_actual, historial, total_incidentes, reporte_grafico, reporte_tabular=""):
    if estado_actual["login_bloqueado"]:
        texto_login = "CERRADO"
    else:
        texto_login = "ABIERTO"

    if estado_actual["refrigeracion"]:
        texto_refrigeracion = "ACTIVA"
    else:
        texto_refrigeracion = "INACTIVA"

    print("")
    print("=" * 54)
    print("  REPORTE FINAL  |  PDI SLP - CYBER DEFENSE SYSTEM")
    print("=" * 54)
    print("  Ciclos ejecutados  : " + str(len(historial)))
    print("  Incidentes detect. : " + str(total_incidentes))
    print("  IPs bloqueadas     : " + str(len(estado_actual["ips_bloqueadas"])))
    print("  Estado final       : " + estado_actual["estado"])
    print("  Cifrado activo     : " + estado_actual["cifrado"])
    print("  Login remoto       : " + texto_login)
    print("  Refrigeracion      : " + texto_refrigeracion)
    print("  Reporte grafico    : " + reporte_grafico)
    if reporte_tabular != "":
        print("  Reporte tabular    : " + reporte_tabular)
    if len(historial) > 0:
        suma_paquetes = 0
        suma_temperatura = 0
        suma_cpu = 0
        for h in historial:
            suma_paquetes = suma_paquetes + h["paquetes"]
            suma_temperatura = suma_temperatura + h["temperatura"]
            suma_cpu = suma_cpu + h["cpu"]

        paq_prom  = suma_paquetes / len(historial)
        temp_prom = suma_temperatura / len(historial)
        cpu_prom  = suma_cpu / len(historial)
        print("")
        print("  Paquetes/s prom.   : " + str(round(paq_prom,  1)))
        print("  Temperatura prom.  : " + str(round(temp_prom, 1)) + " C")
        print("  CPU prom.          : " + str(round(cpu_prom,  1)) + " %")
    print("")
    print("=" * 54)
    print("")
