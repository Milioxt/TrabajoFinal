# scraper.py

import os
import json
import time
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
from urllib.parse import quote

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

def cargar_revistas(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def cargar_datos_existentes(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def guardar_resultados(datos, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)

def construir_url(nombre):
    return f'https://www.scimagojr.com/journalsearch.php?q={quote(nombre)}'

def obtener_url_revista(nombre_revista):
    url = construir_url(nombre_revista)
    print(f"Buscando en: {url}")
    
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        enlaces = soup.select(".search_results a[href*='journalsearch.php?q=']")
        
        for a in enlaces:
            href = a.get("href", "")
            if "tip=sid" in href:
                return 'https://www.scimagojr.com/' + href
    except Exception as e:
        print(f"Error al buscar URL: {e}")
    
    return None

def get_texto(soup, selector):
    el = soup.select_one(selector)
    return el.text.strip() if el else None

def obtener_sitio_web(soup):
    heading = soup.find('h2', string='Information')
    if heading:
        for a in heading.find_all_next('a', id='question_journal'):
            if 'Homepage' in a.text:
                return a['href'].strip()
    return None

def extraer_info_revista(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        return {
            'sitio_web': obtener_sitio_web(soup),
            'h_index': get_texto(soup, "p.hindexnumber"),
            'subject_area': get_texto(soup, "div:has(h2:contains('Subject Area and Category')) p"),
            'publisher': get_texto(soup, "div:has(h2:contains('Publisher')) p"),
            'issn': get_texto(soup, "div:has(h2:contains('ISSN')) p"),
            'widget': get_texto(soup, "textarea#sjr_widget"),
            'tipo_publicacion': get_texto(soup, "div:has(h2:contains('Publication type')) p"),
            'ultima_visita': time.strftime("%Y-%m-%d")
        }
    except Exception as e:
        print(f"Error al extraer datos: {e}")
        return None
