import random
import m01_servidores as srv

def generar_trafico_normal(segundo):
    central = srv.centrales[random.randint(0, 2)]

    if central == "CENTRAL_NORTE":
        agentes = srv.agentes_norte
    elif central == "CENTRAL_CENTRO":
        agentes = srv.agentes_centro
    else:
        agentes = srv.agentes_sur

    usuario     = agentes[random.randint(0, len(agentes) - 1)]
    ip          = srv.ips_internas[random.randint(0, len(srv.ips_internas) - 1)]
    expediente  = srv.tipos_expediente[random.randint(0, len(srv.tipos_expediente) - 1)]
    carpeta_id  = "CI-2026-" + str(random.randint(100000, 999999))

    paquete = {
        "segundo"          : segundo,
        "central"          : central,
        "usuario"          : usuario,
        "ip"               : ip,
        "expediente"       : expediente,
        "carpeta_id"       : carpeta_id,
        "paquetes"         : random.randint(80,  420),
        "intentos_login"   : random.randint(0,   2),
        "cambios_archivos" : random.randint(0,   3),
        "salida_datos"     : random.randint(1,   12),
        "cpu_base"         : random.randint(18,  38),
        "temperatura_base" : random.randint(34,  46),
        "cpu"              : 0,
        "temperatura"      : 0,
        "incidente"        : False,
        "tipo_incidente"   : "NINGUNO"
    }
    return paquete
