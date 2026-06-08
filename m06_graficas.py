# Importamos os para crear carpetas y formar rutas de archivos.
import os
# Importamos math para usar funciones matematicas como seno.
import math

# Importamos matplotlib para generar imagenes sin abrir ventanas.
import matplotlib
# Indicamos que matplotlib trabajara en modo archivo, no en pantalla.
matplotlib.use("Agg")
# Importamos pyplot para crear las graficas.
import matplotlib.pyplot as plt

# Importamos los umbrales del sistema.
import m01_servidores as srv

# Esta funcion recibe el historial completo y genera las graficas.
def generar_graficas(historial, carpeta="pdi_slp_graficas"):
    # Creamos la carpeta de graficas si no existe.
    os.makedirs(carpeta, exist_ok=True)

    # Esta lista guardara los estados convertidos a numeros.
    estados_num = []
    # Recorremos cada fila del historial.
    for h in historial:
        # Si el estado es normal, lo representamos con 0.
        if h["estado"] == "NORMAL":
            # Guardamos 0 para NORMAL.
            estados_num.append(0)
        # Si el estado es sospechoso, lo representamos con 1.
        elif h["estado"] == "SOSPECHOSO":
            # Guardamos 1 para SOSPECHOSO.
            estados_num.append(1)
        # Si el estado es alerta, lo representamos con 2.
        elif h["estado"] == "ALERTA":
            # Guardamos 2 para ALERTA.
            estados_num.append(2)
        # Si no fue ninguno anterior, se toma como critico.
        else:
            # Guardamos 3 para CRITICO.
            estados_num.append(3)

    # Lista para guardar los segundos.
    t = []
    # Lista para guardar paquetes.
    paquetes = []
    # Lista para guardar intentos de login.
    intentos = []
    # Lista para guardar temperatura final.
    temperatura = []
    # Lista para guardar temperatura antes de enfriar.
    temperatura_sin_enfriamiento = []
    # Lista para indicar cuando hubo refrigeracion.
    refrigeracion_activa = []
    # Lista para guardar flujo digital.
    flujo = []
    # Lista para la primera derivada suavizada.
    primera_derivada_sigmoide = []
    # Lista para la segunda derivada suavizada.
    segunda_derivada_sigmoide = []

    # Recorremos el historial para separar los datos en listas.
    for h in historial:
        # Guardamos el segundo.
        t.append(h["segundo"])
        # Guardamos paquetes.
        paquetes.append(h["paquetes"])
        # Guardamos intentos de login.
        intentos.append(h["intentos_login"])
        # Guardamos temperatura final.
        temperatura.append(h["temperatura"])
        # Guardamos temperatura antes de enfriar, o la final si no existe.
        temperatura_sin_enfriamiento.append(
            h.get("temperatura_sin_enfriamiento", h["temperatura"])
        )
        # Guardamos si la refrigeracion estuvo activa.
        refrigeracion_activa.append(h.get("refrigeracion_activa", 0))
        # Guardamos el flujo digital.
        flujo.append(h["flujo"])
        # Guardamos la primera derivada con sigmoide.
        primera_derivada_sigmoide.append(h["primera_derivada_sigmoide"])
        # Guardamos la segunda derivada con sigmoide.
        segunda_derivada_sigmoide.append(h["segunda_derivada_sigmoide"])

    # Esta lista guardara las rutas de las imagenes generadas.
    rutas = []

    # Esta funcion prepara el estilo visual de cada grafica.
    def preparar_figura(titulo, ylabel):
        # Creamos una figura y sus ejes.
        figura, ax = plt.subplots(figsize=(10, 5))
        # Ponemos fondo oscuro a la figura.
        figura.patch.set_facecolor("#07090f")
        # Ponemos fondo oscuro al area de la grafica.
        ax.set_facecolor("#0d1117")
        # Ponemos el titulo de la grafica.
        ax.set_title(titulo, color="#e0e0e0", fontsize=11, fontweight="bold")
        # Ponemos el titulo del eje X.
        ax.set_xlabel("Tiempo (s)", color="#888", fontsize=9)
        # Ponemos el titulo del eje Y.
        ax.set_ylabel(ylabel, color="#888", fontsize=9)
        # Ajustamos color y tamano de los numeros.
        ax.tick_params(colors="#777", labelsize=8)
        # Agregamos una cuadricula ligera.
        ax.grid(color="#1e2a38", linestyle=":", linewidth=0.7)
        # Recorremos los bordes de la grafica.
        for borde in ax.spines.values():
            # Cambiamos el color del borde.
            borde.set_edgecolor("#1e2a38")
        # Regresamos la figura y el eje para seguir dibujando.
        return figura, ax

    # Esta funcion guarda una figura como imagen.
    def guardar(figura, nombre):
        # Creamos la ruta completa de la imagen.
        ruta = os.path.join(carpeta, nombre)
        # Guardamos la imagen en PNG.
        figura.savefig(ruta, dpi=120, bbox_inches="tight", facecolor="#07090f")
        # Cerramos la figura para liberar memoria.
        plt.close(figura)
        # Guardamos la ruta en la lista de rutas.
        rutas.append(ruta)

    # Esta funcion genera una onda de referencia para comparar el trafico.
    def generar_onda_envio(tiempo, valores, max_regular=500, intervalo=5, puntos_por_intervalo=80):
        # Si no hay tiempo, regresamos listas vacias.
        if len(tiempo) == 0:
            # Regresamos sin datos.
            return [], []
        # Lista para los puntos del tiempo de la onda.
        tiempo_onda = []
        # Lista para los valores de la onda.
        valores_onda = []
        # Tomamos el primer segundo.
        inicio_total = tiempo[0]
        # Tomamos el ultimo segundo.
        fin_total = tiempo[-1]
        # Iniciamos desde el primer segundo.
        inicio = inicio_total
        # Recorremos por bloques de tiempo.
        while inicio <= fin_total:
            # Calculamos el final del bloque.
            fin = inicio + intervalo
            # Guardamos los valores que caen dentro del bloque.
            valores_intervalo = []
            # Recorremos cada punto de tiempo real.
            for i in range(len(tiempo)):
                # Revisamos si el punto cae dentro del bloque actual.
                if inicio <= tiempo[i] < fin:
                    # Guardamos el valor del bloque.
                    valores_intervalo.append(valores[i])
            # Si no hubo valores en el bloque, la amplitud es cero.
            if len(valores_intervalo) == 0:
                # Guardamos amplitud cero.
                amplitud = 0
            # Si hubo valores, usamos el mayor sin pasar el maximo regular.
            else:
                # Calculamos la amplitud del bloque.
                amplitud = min(max(valores_intervalo), max_regular)
            # Creamos varios puntos para que la onda se vea suave.
            for paso in range(puntos_por_intervalo):
                # Calculamos la posicion dentro del intervalo.
                local = paso / puntos_por_intervalo
                # Calculamos el valor de X.
                x = inicio + intervalo * local
                # Si la amplitud es cero, la onda queda en cero.
                if amplitud == 0:
                    # Guardamos valor cero.
                    y = 0
                # Si hay amplitud, usamos seno para crear la onda.
                else:
                    # Calculamos el valor de la onda.
                    y = amplitud * math.sin(math.pi * local)
                # Guardamos el tiempo de la onda.
                tiempo_onda.append(x)
                # Guardamos el valor redondeado de la onda.
                valores_onda.append(round(y, 2))
            # Avanzamos al siguiente bloque.
            inicio = fin
        # Agregamos el ultimo segundo.
        tiempo_onda.append(fin_total)
        # Cerramos la onda en cero.
        valores_onda.append(0)
        # Regresamos los puntos de la onda.
        return tiempo_onda, valores_onda

    # Preparamos la grafica 1 de paquetes.
    figura, ax = preparar_figura("1. Paquetes vs Tiempo", "Paquetes/s")
    # Dibujamos la linea de paquetes.
    ax.plot(t, paquetes, color="#00bcd4", linewidth=2, label="paquetes por segundo")
    # Dibujamos el umbral de alerta.
    ax.axhline(y=srv.U_PAQUETES_ALERTA, color="#ffeb3b", linestyle="--", linewidth=1, label="umbral alerta")
    # Dibujamos el umbral critico.
    ax.axhline(y=srv.U_PAQUETES_CRIT, color="#f44336", linestyle="--", linewidth=1, label="umbral critico")
    # Mostramos la simbologia.
    ax.legend(facecolor="#0d1117", edgecolor="#1e2a38", labelcolor="#aaa", fontsize=8)
    # Guardamos la grafica 1.
    guardar(figura, "01_paquetes_vs_tiempo.png")

    # Preparamos la grafica 2 de intentos de login.
    figura, ax = preparar_figura("2. Intentos Login vs Tiempo", "Intentos login")
    # Dibujamos la linea de intentos.
    ax.plot(t, intentos, color="#ff9800", linewidth=2, label="intentos de login")
    # Dibujamos el umbral de alerta.
    ax.axhline(y=srv.U_LOGIN_ALERTA, color="#ffeb3b", linestyle="--", linewidth=1, label="umbral alerta")
    # Dibujamos el umbral critico.
    ax.axhline(y=srv.U_LOGIN_CRIT, color="#f44336", linestyle="--", linewidth=1, label="umbral critico")
    # Mostramos la simbologia.
    ax.legend(facecolor="#0d1117", edgecolor="#1e2a38", labelcolor="#aaa", fontsize=8)
    # Guardamos la grafica 2.
    guardar(figura, "02_intentos_login_vs_tiempo.png")

    # Preparamos la grafica 3 de temperatura.
    figura, ax = preparar_figura("3. Temperatura vs Tiempo", "Temperatura (C)")
    # Dibujamos la temperatura antes de ventilar.
    ax.plot(t, temperatura_sin_enfriamiento, color="#ff7043", linewidth=1.4, linestyle="--", label="antes de ventilar")
    # Dibujamos la temperatura final.
    ax.plot(t, temperatura, color="#40c4ff", linewidth=2, label="temperatura final")
    # Dibujamos el umbral de refrigeracion.
    ax.axhline(y=srv.U_TEMP_REFRIG, color="#ffeb3b", linestyle="--", linewidth=1)
    # Dibujamos el umbral critico.
    ax.axhline(y=srv.U_TEMP_CRITICA, color="#f44336", linestyle="--", linewidth=1)
    # Revisamos si hubo refrigeracion en algun ciclo.
    if any(refrigeracion_activa):
        # Pintamos el espacio donde la refrigeracion redujo temperatura.
        ax.fill_between(t, temperatura, temperatura_sin_enfriamiento, where=refrigeracion_activa, color="#1de9b6", alpha=0.18, label="refrigeracion por fluidos")
    # Mostramos la simbologia.
    ax.legend(facecolor="#0d1117", edgecolor="#1e2a38", labelcolor="#aaa", fontsize=8)
    # Guardamos la grafica 3.
    guardar(figura, "03_temperatura_vs_tiempo.png")

    # Preparamos la grafica 4 de estados.
    figura, ax = preparar_figura("4. Estado del Sistema vs Tiempo", "Estado")
    # Dibujamos el estado como escalones.
    ax.plot(t, estados_num, color="#7c4dff", linewidth=2, drawstyle="steps-post")
    # Indicamos los valores del eje Y.
    ax.set_yticks([0, 1, 2, 3])
    # Ponemos el nombre de cada estado en el eje Y.
    ax.set_yticklabels(["NORMAL", "SOSP.", "ALERTA", "CRITICO"], fontsize=8, color="#aaa")
    # Guardamos la grafica 4.
    guardar(figura, "04_estado_sistema_vs_tiempo.png")

    # Preparamos la grafica 5 de flujo digital.
    figura, ax = preparar_figura("5. Indice Flujo Digital vs Tiempo", "Flujo digital")
    # Dibujamos el flujo digital.
    ax.plot(t, flujo, color="#69ff47", linewidth=2, label="flujo digital")
    # Dibujamos umbral de flujo elevado.
    ax.axhline(y=srv.U_FLUJO_ELEVADO, color="#ffeb3b", linestyle=":", linewidth=1, label="flujo elevado")
    # Dibujamos umbral de flujo en riesgo.
    ax.axhline(y=srv.U_FLUJO_RIESGO, color="#ff9800", linestyle="--", linewidth=1, label="flujo en riesgo")
    # Dibujamos umbral de flujo critico.
    ax.axhline(y=srv.U_FLUJO_CRITICO, color="#f44336", linestyle="--", linewidth=1, label="flujo critico")
    # Mostramos la simbologia.
    ax.legend(facecolor="#0d1117", edgecolor="#1e2a38", labelcolor="#aaa", fontsize=8)
    # Guardamos la grafica 5.
    guardar(figura, "05_indice_flujo_digital_vs_tiempo.png")

    # Preparamos la grafica 6 de derivadas.
    figura, ax = preparar_figura("6. Calculo: derivadas con sigmoide", "Cambio")
    # Dibujamos la linea cero.
    ax.axhline(y=0, color="#90a4ae", linestyle="-", linewidth=0.8, alpha=0.45)
    # Dibujamos el umbral positivo.
    ax.axhline(y=srv.U_TASA, color="#f44336", linestyle="--", linewidth=1, label="umbral +")
    # Dibujamos el umbral negativo.
    ax.axhline(y=-srv.U_TASA, color="#f44336", linestyle=":", linewidth=1, label="umbral -")
    # Lista para marcar valores positivos.
    derivada_positiva = []
    # Lista para marcar valores negativos.
    derivada_negativa = []
    # Recorremos la derivada suavizada.
    for valor in primera_derivada_sigmoide:
        # Guardamos True si el valor es positivo.
        derivada_positiva.append(valor >= 0)
        # Guardamos True si el valor es negativo.
        derivada_negativa.append(valor < 0)
    # Pintamos el area positiva.
    ax.fill_between(t, primera_derivada_sigmoide, 0, where=derivada_positiva, color="#ab47bc", alpha=0.16)
    # Pintamos el area negativa.
    ax.fill_between(t, primera_derivada_sigmoide, 0, where=derivada_negativa, color="#ab47bc", alpha=0.06)
    # Dibujamos la primera derivada.
    ax.plot(t, primera_derivada_sigmoide, color="#ce5cff", linewidth=2.2, label="Primera derivada con sigmoide P'(t)")
    # Dibujamos la segunda derivada.
    ax.plot(t, segunda_derivada_sigmoide, color="#40c4ff", linewidth=1.8, marker="o", markersize=3, label="Segunda derivada con sigmoide P''(t)")
    # Mostramos la simbologia.
    ax.legend(facecolor="#0d1117", edgecolor="#1e2a38", labelcolor="#aaa", fontsize=8)
    # Guardamos la grafica 6.
    guardar(figura, "06_derivadas_trafico_vs_tiempo.png")

    # Preparamos la grafica 7 de analisis oscilatorio.
    figura, ax = preparar_figura("7. Analisis oscilatorio del comportamiento", "Paquetes/s")
    # Generamos la onda regular para comparar.
    tiempo_onda, onda_envio = generar_onda_envio(t, paquetes)
    # Dibujamos la onda regular.
    ax.plot(tiempo_onda, onda_envio, color="#69f0ae", linewidth=2.1, label="onda de envio regular")
    # Dibujamos los paquetes reales.
    ax.plot(t, paquetes, color="#40c4ff", linewidth=1.9, marker="o", markersize=4, label="comportamiento lineal")
    # Pintamos el area de la onda.
    ax.fill_between(tiempo_onda, onda_envio, 0, color="#69f0ae", alpha=0.08)
    # Mostramos la simbologia.
    ax.legend(facecolor="#0d1117", edgecolor="#1e2a38", labelcolor="#aaa", fontsize=8)
    # Guardamos la grafica 7.
    guardar(figura, "07_analisis_oscilatorio_vs_tiempo.png")

    # Regresamos la carpeta donde se guardaron las graficas.
    return carpeta
