import os 
import json

def get_authors():
    return [
        'Mauricio Huerta Terán - Front End',
        'Emilio Portela Salido - Scrapper'
        'Bryan Gallegos Solano - CSV to JSON',
    ]

GUARDADOS_PATH = "data/guardados.json"

def cargar_guardados():
    if os.path.exists(GUARDADOS_PATH):
        with open(GUARDADOS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def guardar_guardados(data):
    with open(GUARDADOS_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)