''' Generador de archivo JSON a partir de archivos CSV de áreas y catálogos '''

import os
import csv
import json
import argparse

def leer_titulos_csv(ruta_archivo: str) -> list:
    ''' Lee los títulos de revistas desde un archivo CSV '''
    for codificacion in ('utf-8', 'latin-1', 'windows-1252'):
        try:
            with open(ruta_archivo, 'r', encoding=codificacion) as f:
                lector = csv.reader(f)
                next(lector, None)
                return [fila[0].strip() for fila in lector if fila and fila[0].strip()]
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f"No se pudo leer el archivo '{ruta_archivo}' con codificaciones comunes.")

def construir_diccionario_desde_csv(directorio: str) -> dict:
    ''' Crea un diccionario donde cada título apunta a una lista de categorías (áreas o catálogos) '''
    diccionario = {}
    for archivo in sorted(os.listdir(directorio)):
        if archivo.endswith('.csv'):
            etiqueta = os.path.splitext(archivo)[0] 
            ruta_completa = os.path.join(directorio, archivo)
            for titulo in leer_titulos_csv(ruta_completa):
                diccionario.setdefault(titulo, []).append(etiqueta)
    
    # Ordenar y eliminar duplicados en los valores
    for titulo in diccionario:
        diccionario[titulo] = sorted(set(diccionario[titulo]))
    
    return diccionario

def verificar_directorio(ruta: str) -> bool:
    ''' Verifica si el directorio existe y contiene archivos CSV '''
    if not os.path.exists(ruta):
        print(f"No existe el directorio '{ruta}'.")
        return False
    print(f"Directorio encontrado: '{ruta}'.")

    archivos = os.listdir(ruta)
    if not archivos:
        print(f"El directorio '{ruta}' está vacío.")
        return False
    if not any(f.lower().endswith('.csv') for f in archivos):
        print(f"No se encontraron archivos CSV en '{ruta}'.")
        return False
    return True

def combinar_areas_y_catalogos(dic_areas: dict, dic_catalogos: dict) -> dict:
    ''' Une los diccionarios de áreas y catálogos por título '''
    return {
        titulo: {
            'areas': dic_areas.get(titulo, []),
            'catalogos': dic_catalogos.get(titulo, [])
        }
        for titulo in sorted(set(dic_areas) | set(dic_catalogos))
    }

def guardar_json(diccionario: dict, ruta_salida: str) -> None:
    ''' Guarda el diccionario como un archivo JSON '''
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        json.dump(diccionario, f, ensure_ascii=False, indent=2)

def generar_json(ruta_csv: str, ruta_json: str) -> None:
    ''' Función principal del programa '''

    ruta_areas = os.path.join(ruta_csv, 'areas')
    ruta_catalogos = os.path.join(ruta_csv, 'catalogos')

    print('\nVerificando directorio de áreas:')
    if not verificar_directorio(ruta_areas):
        print("\nPrograma finalizado.\n")
        return
    print('\nVerificando directorio de catálogos:')
    if not verificar_directorio(ruta_catalogos):
        print("\nPrograma finalizado.\n")
        return

    if os.path.exists(ruta_json):
        respuesta = input(f"\nEl archivo '{ruta_json}' ya existe. ¿Deseas reemplazarlo? (s/n): ").strip().lower()
        if respuesta == 's':
            os.remove(ruta_json)
            print(f"\nArchivo eliminado: '{ruta_json}'")
        else:
            print("\nPrograma finalizado.\n")
            return

    print("\nProcesando archivos...")

    dic_areas = construir_diccionario_desde_csv(ruta_areas)
    dic_catalogos = construir_diccionario_desde_csv(ruta_catalogos)
    dic_revistas = combinar_areas_y_catalogos(dic_areas, dic_catalogos)

    guardar_json(dic_revistas, ruta_json)
    print(f"\nArchivo JSON generado exitosamente en '{ruta_json}'")
    print("\nPrograma finalizado.\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--datos_dir_path', type=str, help='Ruta de la carpeta datos')
    parser.add_argument('--output_filename', type=str, help='Nombre del archivo de salida JSON')
    args = parser.parse_args()

    # Establecer rutas por defecto si no se pasan argumentos
    base_dir = os.path.dirname(os.path.abspath(__file__))
    datos_dir = args.datos_dir_path or os.path.join(base_dir, 'datos')
    nombre_salida = args.output_filename or 'revistas_unison.json'

    ruta_csv = os.path.join(datos_dir, 'csv')
    ruta_json = os.path.join(datos_dir, 'json', nombre_salida)

    generar_json(ruta_csv, ruta_json)
