import random
import m01_servidores as srv

TIPOS_ATAQUE = [
    "ATAQUE_TRAFICO",
    "FUERZA_BRUTA",
    "ACCESO_NO_AUTORIZADO",
    "COPIA_EXPEDIENTE",
    "MODIFICACION_EVIDENCIA",
    "ELIMINACION_ARCHIVO",
    "EXTRACCION_INFORMACION"
]

def inyectar_ataque(paquete, segundo):
    factor = segundo / 10
    tipo   = TIPOS_ATAQUE[random.randint(0, len(TIPOS_ATAQUE) - 1)]
    ip_ext = srv.ips_sospechosas[random.randint(0, len(srv.ips_sospechosas) - 1)]
    usr_ext = srv.usuarios_sospechosos[random.randint(0, len(srv.usuarios_sospechosos) - 1)]

    if tipo == "ATAQUE_TRAFICO":
        paquete["paquetes"]       = int(650 * factor)
        paquete["ip"]             = ip_ext

    elif tipo == "FUERZA_BRUTA":
        paquete["intentos_login"] = int(7 * factor)
        paquete["ip"]             = ip_ext
        paquete["usuario"]        = usr_ext

    elif tipo == "ACCESO_NO_AUTORIZADO":
        paquete["paquetes"]       = int(380 * factor)
        paquete["intentos_login"] = int(4 * factor)
        paquete["ip"]             = ip_ext
        paquete["usuario"]        = usr_ext

    elif tipo == "COPIA_EXPEDIENTE":
        paquete["salida_datos"]   = int(35 * factor)
        paquete["paquetes"]       = int(420 * factor)
        paquete["ip"]             = ip_ext

    elif tipo == "MODIFICACION_EVIDENCIA":
        paquete["cambios_archivos"] = int(7 * factor)
        paquete["expediente"]       = "evidencia_digital"
        paquete["usuario"]          = usr_ext

    elif tipo == "ELIMINACION_ARCHIVO":
        paquete["cambios_archivos"] = int(10 * factor)
        paquete["salida_datos"]     = int(18 * factor)
        paquete["usuario"]          = usr_ext

    else:
        paquete["paquetes"]       = int(550 * factor)
        paquete["salida_datos"]   = int(55 * factor)
        paquete["intentos_login"] = int(5 * factor)
        paquete["ip"]             = ip_ext

    paquete["incidente"]      = True
    paquete["tipo_incidente"] = tipo
    return paquete
