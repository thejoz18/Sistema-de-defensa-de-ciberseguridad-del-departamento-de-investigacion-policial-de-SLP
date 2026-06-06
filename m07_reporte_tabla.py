import csv
import os

def generar_reporte_tabla(historial, ruta="reportes_tabla/pdi_slp_reporte_tabla.csv"):
    carpeta = os.path.dirname(ruta)
    if carpeta != "":
        os.makedirs(carpeta, exist_ok=True)

    columnas = [
        "segundo",
        "central",
        "usuario",
        "ip",
        "expediente",
        "carpeta_id",
        "paquetes",
        "intentos_login",
        "cambios_archivos",
        "salida_datos",
        "cpu",
        "temperatura",
        "temperatura_sin_enfriamiento",
        "refrigeracion_activa",
        "velocidad_refrigerante",
        "presion_refrigerante",
        "flujo",
        "primera_derivada_paquetes",
        "primera_derivada_sigmoide",
        "segunda_derivada_sigmoide",
        "derivada_cpu",
        "derivada_temperatura",
        "senal_periodica",
        "desviacion_periodica",
        "indice_oscilatorio",
        "incidente",
        "tipo_incidente",
        "estado",
        "cifrado",
        "direccion",
        "direccion_servidor",
    ]

    with open(ruta, "w", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        escritor.writeheader()
        for fila in historial:
            fila_reporte = {}
            for columna in columnas:
                fila_reporte[columna] = fila.get(columna, "")
            escritor.writerow(fila_reporte)

    print("[ PDI SLP ] Reporte tabular guardado: " + ruta)
    return ruta
