import os
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import m01_servidores as srv

def generar_graficas(historial, carpeta="pdi_slp_graficas"):
    os.makedirs(carpeta, exist_ok=True)

    estados_num = []
    for h in historial:
        if h["estado"] == "NORMAL":
            estados_num.append(0)
        elif h["estado"] == "SOSPECHOSO":
            estados_num.append(1)
        elif h["estado"] == "ALERTA":
            estados_num.append(2)
        else:
            estados_num.append(3)

    t = []
    paquetes = []
    intentos = []
    temperatura = []
    temperatura_sin_enfriamiento = []
    refrigeracion_activa = []
    flujo = []
    primera_derivada_sigmoide = []
    segunda_derivada_sigmoide = []

    for h in historial:
        t.append(h["segundo"])
        paquetes.append(h["paquetes"])
        intentos.append(h["intentos_login"])
        temperatura.append(h["temperatura"])
        temperatura_sin_enfriamiento.append(
            h.get("temperatura_sin_enfriamiento", h["temperatura"])
        )
        refrigeracion_activa.append(h.get("refrigeracion_activa", 0))
        flujo.append(h["flujo"])
        primera_derivada_sigmoide.append(h["primera_derivada_sigmoide"])
        segunda_derivada_sigmoide.append(h["segunda_derivada_sigmoide"])

    rutas = []

    def preparar_figura(titulo, ylabel):
        figura, ax = plt.subplots(figsize=(10, 5))
        figura.patch.set_facecolor("#07090f")
        ax.set_facecolor("#0d1117")
        ax.set_title(titulo, color="#e0e0e0", fontsize=11, fontweight="bold")
        ax.set_xlabel("Tiempo (s)", color="#888", fontsize=9)
        ax.set_ylabel(ylabel, color="#888", fontsize=9)
        ax.tick_params(colors="#777", labelsize=8)
        ax.grid(color="#1e2a38", linestyle=":", linewidth=0.7)
        for borde in ax.spines.values():
            borde.set_edgecolor("#1e2a38")
        return figura, ax

    def guardar(figura, nombre):
        ruta = os.path.join(carpeta, nombre)
        figura.savefig(ruta, dpi=120, bbox_inches="tight", facecolor="#07090f")
        plt.close(figura)
        rutas.append(ruta)

    def generar_onda_envio(tiempo, valores, max_regular=500, intervalo=5, puntos_por_intervalo=80):
        if len(tiempo) == 0:
            return [], []
        tiempo_onda = []
        valores_onda = []
        inicio_total = tiempo[0]
        fin_total = tiempo[-1]
        inicio = inicio_total
        while inicio <= fin_total:
            fin = inicio + intervalo
            valores_intervalo = []
            for i in range(len(tiempo)):
                if inicio <= tiempo[i] < fin:
                    valores_intervalo.append(valores[i])
            if len(valores_intervalo) == 0:
                amplitud = 0
            else:
                amplitud = min(max(valores_intervalo), max_regular)
            for paso in range(puntos_por_intervalo):
                local = paso / puntos_por_intervalo
                x = inicio + intervalo * local
                if amplitud == 0:
                    y = 0
                else:
                    y = amplitud * math.sin(math.pi * local)
                tiempo_onda.append(x)
                valores_onda.append(round(y, 2))
            inicio = fin
        tiempo_onda.append(fin_total)
        valores_onda.append(0)
        return tiempo_onda, valores_onda

    figura, ax = preparar_figura("1. Paquetes vs Tiempo", "Paquetes/s")
    ax.plot(t, paquetes, color="#00bcd4", linewidth=2)
    ax.axhline(y=srv.U_PAQUETES_ALERTA, color="#ffeb3b", linestyle="--", linewidth=1)
    ax.axhline(y=srv.U_PAQUETES_CRIT, color="#f44336", linestyle="--", linewidth=1)
    guardar(figura, "01_paquetes_vs_tiempo.png")

    figura, ax = preparar_figura("2. Intentos Login vs Tiempo", "Intentos login")
    ax.plot(t, intentos, color="#ff9800", linewidth=2)
    ax.axhline(y=srv.U_LOGIN_ALERTA, color="#ffeb3b", linestyle="--", linewidth=1)
    ax.axhline(y=srv.U_LOGIN_CRIT, color="#f44336", linestyle="--", linewidth=1)
    guardar(figura, "02_intentos_login_vs_tiempo.png")

    figura, ax = preparar_figura("3. Temperatura vs Tiempo", "Temperatura (C)")
    ax.plot(t, temperatura_sin_enfriamiento, color="#ff7043", linewidth=1.4,
            linestyle="--", label="sin enfriamiento")
    ax.plot(t, temperatura, color="#40c4ff", linewidth=2, label="con enfriamiento")
    ax.axhline(y=srv.U_TEMP_REFRIG, color="#ffeb3b", linestyle="--", linewidth=1)
    ax.axhline(y=srv.U_TEMP_CRITICA, color="#f44336", linestyle="--", linewidth=1)
    if any(refrigeracion_activa):
        ax.fill_between(t, temperatura, temperatura_sin_enfriamiento,
                        where=refrigeracion_activa, color="#1de9b6", alpha=0.18,
                        label="refrigeracion activa")
    ax.legend(facecolor="#0d1117", edgecolor="#1e2a38", labelcolor="#aaa", fontsize=8)
    guardar(figura, "03_temperatura_vs_tiempo.png")

    figura, ax = preparar_figura("4. Estado del Sistema vs Tiempo", "Estado")
    ax.plot(t, estados_num, color="#7c4dff", linewidth=2, drawstyle="steps-post")
    ax.set_yticks([0, 1, 2, 3])
    ax.set_yticklabels(["NORMAL", "SOSP.", "ALERTA", "CRITICO"], fontsize=8, color="#aaa")
    guardar(figura, "04_estado_sistema_vs_tiempo.png")

    figura, ax = preparar_figura("5. Indice Flujo Digital vs Tiempo", "Flujo digital")
    ax.plot(t, flujo, color="#69ff47", linewidth=2)
    ax.axhline(y=srv.U_FLUJO_ELEVADO, color="#ffeb3b", linestyle=":", linewidth=1)
    ax.axhline(y=srv.U_FLUJO_RIESGO, color="#ff9800", linestyle="--", linewidth=1)
    ax.axhline(y=srv.U_FLUJO_CRITICO, color="#f44336", linestyle="--", linewidth=1)
    guardar(figura, "05_indice_flujo_digital_vs_tiempo.png")

    figura, ax = preparar_figura("6. Calculo: derivadas con sigmoide", "Cambio")
    ax.axhline(y=0, color="#90a4ae", linestyle="-", linewidth=0.8, alpha=0.45)
    ax.axhline(y=srv.U_TASA, color="#f44336", linestyle="--", linewidth=1,
               label="umbral +")
    ax.axhline(y=-srv.U_TASA, color="#f44336", linestyle=":", linewidth=1,
               label="umbral -")
    derivada_positiva = []
    derivada_negativa = []
    for valor in primera_derivada_sigmoide:
        derivada_positiva.append(valor >= 0)
        derivada_negativa.append(valor < 0)
    ax.fill_between(t, primera_derivada_sigmoide, 0, where=derivada_positiva,
                    color="#ab47bc", alpha=0.16)
    ax.fill_between(t, primera_derivada_sigmoide, 0, where=derivada_negativa,
                    color="#ab47bc", alpha=0.06)
    ax.plot(t, primera_derivada_sigmoide, color="#ce5cff", linewidth=2.2,
            label="Primera derivada con sigmoide P'(t)")
    ax.plot(t, segunda_derivada_sigmoide, color="#40c4ff", linewidth=1.8,
            marker="o", markersize=3, label="Segunda derivada con sigmoide P''(t)")
    ax.legend(facecolor="#0d1117", edgecolor="#1e2a38", labelcolor="#aaa", fontsize=8)
    guardar(figura, "06_derivadas_trafico_vs_tiempo.png")

    figura, ax = preparar_figura("7. Analisis oscilatorio del comportamiento", "Paquetes/s")
    tiempo_onda, onda_envio = generar_onda_envio(t, paquetes)
    ax.plot(tiempo_onda, onda_envio, color="#69f0ae", linewidth=2.1,
            label="onda de envio regular")
    ax.plot(t, paquetes, color="#40c4ff", linewidth=1.9,
            marker="o", markersize=4, label="comportamiento lineal")
    ax.fill_between(tiempo_onda, onda_envio, 0, color="#69f0ae", alpha=0.08)
    ax.legend(facecolor="#0d1117", edgecolor="#1e2a38", labelcolor="#aaa", fontsize=8)
    guardar(figura, "07_analisis_oscilatorio_vs_tiempo.png")

    print("[ PDI SLP ] Reportes graficos guardados en: " + carpeta)
    for ruta in rutas:
        print("  - " + ruta)
    return carpeta
