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



def obtener_sitio_web(soup):
    heading = soup.find('h2', string='Information')
    if heading:
        for a in heading.find_all_next('a', id='question_journal'):
            if 'Homepage' in a.text:
                return a['href'].strip()
    return None

def obtener_imgen(soup):
    try:
        img = soup.find('img', class_='imgwidget')
        if img and 'src' in img.attrs:
            return 'https://www.scimagojr.com/' + img['src']
    except Exception as e:
        print(f"Error al extraer widget: {e}")
    return None
    
def get_texto_por_h2(soup, titulo):
    h2 = soup.find('h2', string=titulo)
    if h2:
        p = h2.find_next('p')
        if p:
            return p.text.strip()



''' def extraer_hindex(soup):
    texto = get_texto_por_h2(soup, "phindexnumber")
    if texto and texto.isdigit():
        return int(texto)
    return None'''


def extraer_info_revista(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        return  {
        'sitio_web': obtener_sitio_web(soup),
        'h_index': get_texto_por_h2(soup, "H-Index"),
        'subject_area': get_texto_por_h2(soup, 'Subject Area and Category'),
        'publisher': get_texto_por_h2(soup, 'Publisher'),
        'issn': get_texto_por_h2(soup, 'ISSN'),
        'widget': obtener_imgen(soup),
        'tipo_publicacion': get_texto_por_h2(soup, 'Publication type'),
        'ultima_visita': time.strftime("%Y-%m-%d")
}

    except Exception as e:
        print(f"Error al extraer info de {url}: {e}")
        return None