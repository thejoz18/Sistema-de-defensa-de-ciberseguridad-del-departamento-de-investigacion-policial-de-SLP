# Importamos csv para poder crear el archivo de tabla.
import csv
# Importamos os para crear la carpeta del reporte si no existe.
import os

# Esta funcion recibe el historial y lo guarda en un archivo CSV.
def generar_reporte_tabla(historial, ruta="reportes_tabla/pdi_slp_reporte_tabla.csv"):
    # Obtenemos solo la carpeta donde se guardara el archivo.
    carpeta = os.path.dirname(ruta)
    # Revisamos que la ruta si tenga una carpeta.
    if carpeta != "":
        # Creamos la carpeta si todavia no existe.
        os.makedirs(carpeta, exist_ok=True)

    # Esta lista define el orden de las columnas del CSV.
    columnas = [
        # Segundo de la simulacion.
        "segundo",
        # Central que genero el paquete.
        "central",
        # Usuario del paquete.
        "usuario",
        # IP del paquete.
        "ip",
        # Tipo de expediente.
        "expediente",
        # Identificador de carpeta.
        "carpeta_id",
        # Cantidad de paquetes.
        "paquetes",
        # Intentos de login.
        "intentos_login",
        # Cambios en archivos.
        "cambios_archivos",
        # Salida de datos.
        "salida_datos",
        # Porcentaje de CPU.
        "cpu",
        # Potencia del CPU en watts.
        "potencia_cpu_watts",
        # Temperatura final.
        "temperatura",
        # Temperatura antes de enfriar.
        "temperatura_sin_enfriamiento",
        # Indica si hubo refrigeracion activa.
        "refrigeracion_activa",
        # Velocidad del ventilador.
        "velocidad_ventilador",
        # Velocidad del refrigerante.
        "velocidad_refrigerante",
        # Presion de entrada del refrigerante.
        "presion_entrada_refrigerante",
        # Presion de salida del refrigerante.
        "presion_salida_refrigerante",
        # Presion usada como dato general.
        "presion_refrigerante",
        # Aumento de presion en porcentaje.
        "incremento_presion_porcentaje",
        # Consumo del enfriamiento.
        "consumo_enfriamiento_watts",
        # Consumo total.
        "consumo_total_watts",
        # Flujo digital.
        "flujo",
        # Cambio de paquetes entre segundos.
        "primera_derivada_paquetes",
        # Derivada suavizada.
        "primera_derivada_sigmoide",
        # Segunda derivada suavizada.
        "segunda_derivada_sigmoide",
        # Cambio de CPU.
        "derivada_cpu",
        # Cambio de temperatura.
        "derivada_temperatura",
        # Senal periodica esperada.
        "senal_periodica",
        # Diferencia contra la senal esperada.
        "desviacion_periodica",
        # Indice de oscilacion.
        "indice_oscilatorio",
        # Indica si hubo incidente.
        "incidente",
        # Tipo de incidente.
        "tipo_incidente",
        # Estado del sistema.
        "estado",
        # Estado del cifrado.
        "cifrado",
        # Direccion interna normal o cifrada.
        "direccion",
        # Direccion final del servidor.
        "direccion_servidor",
    ]

    # Abrimos el archivo CSV en modo escritura.
    with open(ruta, "w", newline="", encoding="utf-8-sig") as archivo:
        # Creamos el escritor del CSV usando las columnas definidas.
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        # Escribimos la primera fila con los nombres de columnas.
        escritor.writeheader()
        # Recorremos cada fila del historial.
        for fila in historial:
            # Creamos un diccionario limpio para guardar solo las columnas que queremos.
            fila_reporte = {}
            # Recorremos cada columna del reporte.
            for columna in columnas:
                # Guardamos el valor si existe, y si no existe dejamos vacio.
                fila_reporte[columna] = fila.get(columna, "")
            # Escribimos la fila completa en el CSV.
            escritor.writerow(fila_reporte)

    # Regresamos la ruta donde se guardo el reporte.
    return ruta
