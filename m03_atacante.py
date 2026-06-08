# Importamos random para elegir ataques al azar.
import random
# Importamos listas de usuarios e IPs sospechosas.
import m01_servidores as srv

# Esta lista guarda los tipos de ataques que puede simular el programa.
TIPOS_ATAQUE = [
    # Ataque donde sube mucho el trafico.
    "ATAQUE_TRAFICO",
    # Ataque donde hay muchos intentos de entrar.
    "FUERZA_BRUTA",
    # Ataque donde aparece un usuario no autorizado.
    "ACCESO_NO_AUTORIZADO",
    # Ataque donde se copia informacion.
    "COPIA_EXPEDIENTE",
    # Ataque donde se modifican archivos.
    "MODIFICACION_EVIDENCIA",
    # Ataque donde se eliminan archivos.
    "ELIMINACION_ARCHIVO",
    # Ataque donde se extrae informacion del sistema.
    "EXTRACCION_INFORMACION"
]

# Esta funcion recibe un paquete normal y lo altera para simular un ataque.
def inyectar_ataque(paquete, segundo):
    # El factor hace que el ataque crezca conforme avanzan los segundos.
    factor = segundo / 10
    # Elegimos un tipo de ataque al azar.
    tipo   = TIPOS_ATAQUE[random.randint(0, len(TIPOS_ATAQUE) - 1)]
    # Elegimos una IP sospechosa para simular el origen del ataque.
    ip_ext = srv.ips_sospechosas[random.randint(0, len(srv.ips_sospechosas) - 1)]
    # Elegimos un usuario sospechoso para simular acceso no autorizado.
    usr_ext = srv.usuarios_sospechosos[random.randint(0, len(srv.usuarios_sospechosos) - 1)]

    # Si el ataque es de trafico, aumentamos mucho los paquetes.
    if tipo == "ATAQUE_TRAFICO":
        # Cambiamos los paquetes para que se note el ataque.
        paquete["paquetes"]       = int(650 * factor)
        # Cambiamos la IP por una IP sospechosa.
        paquete["ip"]             = ip_ext

    # Si el ataque es de fuerza bruta, aumentamos los intentos de login.
    elif tipo == "FUERZA_BRUTA":
        # Aumentamos los intentos de login.
        paquete["intentos_login"] = int(7 * factor)
        # Cambiamos la IP por una externa sospechosa.
        paquete["ip"]             = ip_ext
        # Cambiamos el usuario por uno sospechoso.
        paquete["usuario"]        = usr_ext

    # Si el ataque es acceso no autorizado, alteramos usuario, IP y trafico.
    elif tipo == "ACCESO_NO_AUTORIZADO":
        # Aumentamos paquetes para que se note actividad rara.
        paquete["paquetes"]       = int(380 * factor)
        # Aumentamos intentos de login.
        paquete["intentos_login"] = int(4 * factor)
        # Cambiamos la IP.
        paquete["ip"]             = ip_ext
        # Cambiamos el usuario.
        paquete["usuario"]        = usr_ext

    # Si el ataque es copia de expediente, aumenta la salida de datos.
    elif tipo == "COPIA_EXPEDIENTE":
        # Aumentamos los datos que salen del sistema.
        paquete["salida_datos"]   = int(35 * factor)
        # Aumentamos paquetes porque se esta transfiriendo informacion.
        paquete["paquetes"]       = int(420 * factor)
        # Cambiamos la IP por una sospechosa.
        paquete["ip"]             = ip_ext

    # Si se modifica evidencia, aumentamos cambios de archivos.
    elif tipo == "MODIFICACION_EVIDENCIA":
        # Aumentamos el numero de cambios.
        paquete["cambios_archivos"] = int(7 * factor)
        # Cambiamos el expediente para indicar evidencia digital.
        paquete["expediente"]       = "evidencia_digital"
        # Cambiamos el usuario por uno sospechoso.
        paquete["usuario"]          = usr_ext

    # Si se elimina un archivo, hay cambios y tambien salida de datos.
    elif tipo == "ELIMINACION_ARCHIVO":
        # Aumentamos cambios de archivos.
        paquete["cambios_archivos"] = int(10 * factor)
        # Aumentamos salida de datos.
        paquete["salida_datos"]     = int(18 * factor)
        # Cambiamos el usuario.
        paquete["usuario"]          = usr_ext

    # Si no fue ningun caso anterior, usamos extraccion de informacion.
    else:
        # Aumentamos paquetes.
        paquete["paquetes"]       = int(550 * factor)
        # Aumentamos salida de datos.
        paquete["salida_datos"]   = int(55 * factor)
        # Aumentamos intentos de login.
        paquete["intentos_login"] = int(5 * factor)
        # Cambiamos la IP.
        paquete["ip"]             = ip_ext

    # Marcamos que el paquete ya tiene un incidente.
    paquete["incidente"]      = True
    # Guardamos el tipo de incidente que se aplico.
    paquete["tipo_incidente"] = tipo
    # Regresamos el paquete alterado para que m00 lo analice.
    return paquete
