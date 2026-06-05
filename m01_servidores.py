centrales = ["CENTRAL_NORTE", "CENTRAL_CENTRO", "CENTRAL_SUR"]

agentes_norte  = ["agente_norte_01",  "analista_forense",    "investigador_norte"]
agentes_centro = ["agente_centro_01", "analista_centro",     "perito_centro"]
agentes_sur    = ["agente_sur_01",    "analista_criminalistica", "investigador_sur"]

agentes_autorizados = []
for a in agentes_norte:
    agentes_autorizados.append(a)
for a in agentes_centro:
    agentes_autorizados.append(a)
for a in agentes_sur:
    agentes_autorizados.append(a)

usuarios_sospechosos = ["ext_user", "anonymous", "root_hack", "ghost_agent", "admin_ext"]

ips_internas = []
for red in range(1, 4):
    for host in range(10, 18):
        ips_internas.append("192.168." + str(red) + "." + str(host))

ips_sospechosas = ["10.0.0.5", "10.0.1.12", "10.0.2.7", "10.0.3.99", "172.16.0.44"]

tipos_expediente = [
    "carpeta_investigacion",
    "evidencia_digital",
    "dictamen_pericial",
    "oficio_ministerial",
    "acta_circunstanciada",
    "registro_detencion"
]

U_PAQUETES_SOSP   = 500
U_PAQUETES_ALERTA = 900
U_PAQUETES_CRIT   = 1600
U_LOGIN_ALERTA    = 8
U_LOGIN_CRIT      = 20
U_CAMBIOS         = 8
U_SALIDA_DATOS    = 40
U_CPU_ALTO        = 80
U_TEMP_REFRIG     = 58
U_TEMP_CRITICA    = 68
U_FLUJO_ELEVADO   = 350
U_FLUJO_RIESGO    = 700
U_FLUJO_CRITICO   = 1100
U_TASA            = 250
U_OSCILACION_SOSP = 650
U_OSCILACION_CRIT = 1200
