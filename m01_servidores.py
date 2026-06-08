# Aqui guardamos los nombres de las centrales que se van a monitorear.
centrales = ["CENTRAL_NORTE", "CENTRAL_CENTRO", "CENTRAL_SUR"]

# Aqui se guardan los agentes autorizados de la central norte.
agentes_norte  = ["agente_norte_01",  "analista_forense",    "investigador_norte"]
# Aqui se guardan los agentes autorizados de la central centro.
agentes_centro = ["agente_centro_01", "analista_centro",     "perito_centro"]
# Aqui se guardan los agentes autorizados de la central sur.
agentes_sur    = ["agente_sur_01",    "analista_criminalistica", "investigador_sur"]

# Creamos una lista vacia donde despues juntamos todos los agentes validos.
agentes_autorizados = []
# Recorremos cada agente del norte para agregarlo a la lista general.
for a in agentes_norte:
    # Guardamos el agente del norte como usuario autorizado.
    agentes_autorizados.append(a)
# Recorremos cada agente del centro para agregarlo a la lista general.
for a in agentes_centro:
    # Guardamos el agente del centro como usuario autorizado.
    agentes_autorizados.append(a)
# Recorremos cada agente del sur para agregarlo a la lista general.
for a in agentes_sur:
    # Guardamos el agente del sur como usuario autorizado.
    agentes_autorizados.append(a)

# Estos usuarios se usan para simular personas sospechosas o no autorizadas.
usuarios_sospechosos = ["ext_user", "anonymous", "root_hack", "ghost_agent", "admin_ext"]

# Creamos una lista vacia para guardar direcciones IP internas.
ips_internas = []
# Recorremos tres redes internas, como 192.168.1, 192.168.2 y 192.168.3.
for red in range(1, 4):
    # Recorremos varios equipos dentro de cada red.
    for host in range(10, 18):
        # Armamos la IP interna y la guardamos en la lista.
        ips_internas.append("192.168." + str(red) + "." + str(host))

# Estas IPs se usan cuando queremos simular ataques externos.
ips_sospechosas = ["10.0.0.5", "10.0.1.12", "10.0.2.7", "10.0.3.99", "172.16.0.44"]

# Esta lista contiene los tipos de documentos o registros que puede manejar el sistema.
tipos_expediente = [
    # Carpeta principal de una investigacion.
    "carpeta_investigacion",
    # Evidencia que viene de archivos o medios digitales.
    "evidencia_digital",
    # Documento tecnico de peritos.
    "dictamen_pericial",
    # Oficio generado para el ministerio publico.
    "oficio_ministerial",
    # Acta que registra hechos importantes.
    "acta_circunstanciada",
    # Registro relacionado con una detencion.
    "registro_detencion"
]

# Umbral para decir que los paquetes ya se ven sospechosos.
U_PAQUETES_SOSP   = 500
# Umbral para decir que los paquetes ya generan alerta.
U_PAQUETES_ALERTA = 900
# Umbral para decir que los paquetes ya son criticos.
U_PAQUETES_CRIT   = 1600
# Umbral para intentos de login en alerta.
U_LOGIN_ALERTA    = 8
# Umbral para intentos de login criticos.
U_LOGIN_CRIT      = 20
# Umbral para cambios de archivos sospechosos.
U_CAMBIOS         = 8
# Umbral para salida de datos elevada.
U_SALIDA_DATOS    = 40
# Umbral de CPU alto, se conserva como referencia.
U_CPU_ALTO        = 80
# Temperatura donde se activa la refrigeracion.
U_TEMP_REFRIG     = 58
# Temperatura donde se considera riesgo critico.
U_TEMP_CRITICA    = 68
# Nivel de flujo digital elevado.
U_FLUJO_ELEVADO   = 350
# Nivel de flujo digital en riesgo.
U_FLUJO_RIESGO    = 700
# Nivel de flujo digital critico.
U_FLUJO_CRITICO   = 1100
# Umbral para detectar cambio brusco entre segundos.
U_TASA            = 250
# Umbral para detectar oscilacion sospechosa.
U_OSCILACION_SOSP = 650
# Umbral para detectar oscilacion critica.
U_OSCILACION_CRIT = 1200
