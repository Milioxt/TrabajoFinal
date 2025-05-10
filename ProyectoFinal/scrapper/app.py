# main.py

from scrapertest import (
    cargar_revistas, cargar_datos_existentes, guardar_resultados,
    obtener_url_revista, extraer_info_revista
)
from unidecode import unidecode
import time

ENTRADA_JSON = 'datos/json/prueba.json'
SALIDA_JSON = 'datos/json/prueba_info.json'

def main():
    revistas = cargar_revistas(ENTRADA_JSON)
    resultados = cargar_datos_existentes(SALIDA_JSON)

    for nombre in revistas:
        if nombre in resultados:
            continue

        nombre_limpio = unidecode(nombre)
        nombre_formateado = ' '.join([p.capitalize() for p in nombre_limpio.split()])

        print(f"\nBuscando: {nombre_formateado}")
        url = obtener_url_revista(nombre_formateado)

        if not url:
            print(f"No encontrada: '{nombre}'")
            continue

        info = extraer_info_revista(url)
        if info:
            resultados[nombre] = info
            print(f"✔ OK: {nombre}")
        else:
            print(f"✖ Error al extraer datos de: {nombre}")

        time.sleep(1)

        if len(resultados) % 5 == 0:
            guardar_resultados(resultados, SALIDA_JSON)
            print("Progreso guardado")

    guardar_resultados(resultados, SALIDA_JSON)
    print(f"\nProceso terminado. Datos en: {SALIDA_JSON}")

if __name__ == '__main__':
    main()
