# Importamos random para generar datos diferentes en cada ciclo.
import random
# Importamos los datos base del servidor, como centrales, agentes e IPs.
import m01_servidores as srv

# Esta funcion crea el paquete normal que se usa en cada segundo.
def generar_trafico_normal(segundo):
    # Elegimos una central al azar de la lista de centrales.
    central = srv.centrales[random.randint(0, 2)]

    # Si la central elegida es norte, usamos sus agentes.
    if central == "CENTRAL_NORTE":
        # Guardamos la lista de agentes del norte.
        agentes = srv.agentes_norte
    # Si la central elegida es centro, usamos sus agentes.
    elif central == "CENTRAL_CENTRO":
        # Guardamos la lista de agentes del centro.
        agentes = srv.agentes_centro
    # Si no fue norte ni centro, entonces usamos los agentes del sur.
    else:
        # Guardamos la lista de agentes del sur.
        agentes = srv.agentes_sur

    # Elegimos un usuario autorizado al azar.
    usuario     = agentes[random.randint(0, len(agentes) - 1)]
    # Elegimos una IP interna al azar.
    ip          = srv.ips_internas[random.randint(0, len(srv.ips_internas) - 1)]
    # Elegimos un tipo de expediente al azar.
    expediente  = srv.tipos_expediente[random.randint(0, len(srv.tipos_expediente) - 1)]
    # Creamos una clave de carpeta con un numero aleatorio.
    carpeta_id  = "CI-2026-" + str(random.randint(100000, 999999))

    # Creamos un diccionario llamado paquete con todos los datos del segundo.
    paquete = {
        # Guardamos el segundo actual de la simulacion.
        "segundo"          : segundo,
        # Guardamos la central que se eligio.
        "central"          : central,
        # Guardamos el usuario que va a trabajar en el paquete.
        "usuario"          : usuario,
        # Guardamos la IP que se usara como origen.
        "ip"               : ip,
        # Guardamos el tipo de expediente.
        "expediente"       : expediente,
        # Guardamos el identificador de la carpeta.
        "carpeta_id"       : carpeta_id,
        # Generamos una cantidad normal de paquetes.
        "paquetes"         : random.randint(80,  420),
        # Generamos pocos intentos de login porque es trafico normal.
        "intentos_login"   : random.randint(0,   2),
        # Generamos pocos cambios de archivos porque es actividad normal.
        "cambios_archivos" : random.randint(0,   3),
        # Generamos una salida de datos pequena.
        "salida_datos"     : random.randint(1,   12),
        # Generamos una base inicial de CPU.
        "cpu_base"         : random.randint(18,  38),
        # Guardamos una temperatura base como dato de referencia.
        "temperatura_base" : random.randint(34,  46),
        # Iniciamos CPU en cero porque despues se calcula en m04.
        "cpu"              : 0,
        # Iniciamos temperatura en cero porque despues se calcula en m04.
        "temperatura"      : 0,
        # Indicamos que al inicio no hay incidente.
        "incidente"        : False,
        # Indicamos que al inicio no hay tipo de incidente.
        "tipo_incidente"   : "NINGUNO"
    }
    # Regresamos el paquete para que m00 lo use en el ciclo.
    return paquete
