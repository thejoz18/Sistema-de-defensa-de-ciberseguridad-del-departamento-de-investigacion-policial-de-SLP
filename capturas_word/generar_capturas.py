import csv
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


BASE = Path(__file__).resolve().parent.parent
SALIDA = BASE / "capturas_word"


def generar_captura_csv():
    csv_path = BASE / "reportes_tabla" / "pdi_slp_reporte_tabla.csv"
    png_path = SALIDA / "captura_csv_generado.png"

    columnas_visibles = [
        "segundo",
        "central",
        "usuario",
        "ip",
        "paquetes",
        "intentos_login",
        "flujo",
        "estado",
        "cifrado",
    ]

    with csv_path.open("r", encoding="utf-8-sig", newline="") as archivo:
        lector = csv.DictReader(archivo)
        filas = []
        for fila in lector:
            filas.append([fila.get(col, "") for col in columnas_visibles])
            if len(filas) == 10:
                break

    fig, ax = plt.subplots(figsize=(16, 6))
    fig.patch.set_facecolor("#ffffff")
    ax.axis("off")
    ax.set_title(
        "Captura del CSV generado: reportes_tabla/pdi_slp_reporte_tabla.csv",
        fontsize=15,
        fontweight="bold",
        pad=18,
    )

    tabla = ax.table(
        cellText=filas,
        colLabels=columnas_visibles,
        cellLoc="center",
        loc="center",
    )
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(8)
    tabla.scale(1, 1.7)

    for (fila, columna), celda in tabla.get_celld().items():
        celda.set_edgecolor("#b8c2cc")
        if fila == 0:
            celda.set_facecolor("#17324a")
            celda.set_text_props(color="white", weight="bold")
        else:
            celda.set_facecolor("#f8fafc" if fila % 2 == 0 else "#ffffff")

    fig.savefig(png_path, dpi=170, bbox_inches="tight")
    plt.close(fig)
    return png_path


def generar_captura_consola():
    txt_path = SALIDA / "captura_consola.txt"
    png_path = SALIDA / "captura_consola_sistema.png"

    contenido = txt_path.read_text(encoding="utf-16", errors="replace")
    lineas = contenido.splitlines()
    fragmento = lineas[-42:]
    texto = "\n".join(textwrap.shorten(line, width=112, placeholder="...") for line in fragmento)

    fig, ax = plt.subplots(figsize=(15, 10))
    fig.patch.set_facecolor("#0d1117")
    ax.set_facecolor("#0d1117")
    ax.axis("off")
    ax.text(
        0.02,
        0.98,
        texto,
        va="top",
        ha="left",
        family="monospace",
        fontsize=11,
        color="#e5e7eb",
        linespacing=1.25,
    )
    ax.set_title(
        "Captura de consola del sistema",
        fontsize=16,
        fontweight="bold",
        color="#e5e7eb",
        loc="left",
        pad=16,
    )
    fig.savefig(png_path, dpi=170, bbox_inches="tight", facecolor="#0d1117")
    plt.close(fig)
    return png_path


if __name__ == "__main__":
    print(generar_captura_csv())
    print(generar_captura_consola())
