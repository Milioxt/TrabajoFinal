# main.py
import argparse
import time
from unidecode import unidecode
from scrapertest import (
    cargar_revistas, cargar_datos_existentes, guardar_resultados,
    obtener_url_revista, extraer_info_revista
)

def main():
    parser = argparse.ArgumentParser(description="Scrapper SCImago")
    parser.add_argument('entrada', help="Ruta del archivo JSON de entrada")
    parser.add_argument('inicio', type=int, help="Índice inicial (inclusive)")
    parser.add_argument('fin', type=int, help="Índice final (exclusivo)")
    parser.add_argument('salida', help="Ruta del archivo JSON de salida")
    args = parser.parse_args()

    revistas = cargar_revistas(args.entrada)
    resultados = cargar_datos_existentes(args.salida)

    # Soporta diccionario o lista
    if isinstance(revistas, dict):
        keys = list(revistas.keys())[args.inicio:args.fin]
    else:
        keys = revistas[args.inicio:args.fin]

    for nombre in keys:
        if nombre in resultados:
            continue

        nombre_limpio = unidecode(nombre)
        print(f"\nBuscando: {nombre_limpio}")
        url = obtener_url_revista(nombre_limpio)

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
            guardar_resultados(resultados, args.salida)
            print("Progreso guardado")

    guardar_resultados(resultados, args.salida)
    print(f"\nProceso terminado. Datos en: {args.salida}")

if __name__ == '__main__':
    main()
