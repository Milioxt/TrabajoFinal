#Un programa "web scrapper" que leerá un archivo JSON y buscará información de cada revista en SCIMAGO 
# y la guardará en un nuevo archivo JSON

import os 
import json
import time
from urllib.parse import quote_plus
import requests
import argparse
from bs4 import BeautifulSoup

# ——— Configuración ———
HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/123.0.0.0 Safari/537.36'
    )
}
SEARCH_BASE = 'https://www.scimagojr.com/journalsearch.php?q='
DETAIL_BASE = 'https://www.scimagojr.com/'

INPUT_JSON  = 'revistas.json'
OUTPUT_JSON = 'revistas_scraped.json'
DELAY       = 1.0  # segundos entre peticiones

# ——— Funciones ———
def load_json(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        #revisamos si la info esta en un diccionario o en una lista
    return data if isinstance(data, dict) else {title: {} for title in data}
        # Si es una lista, convertimos a diccionario con títulos como claves y valores vacíos

def scrap(url: str) -> BeautifulSoup:
    r = requests.get(url, headers=HEADERS, timeout=15)
    if r.status_code != 200:
        raise RuntimeError(f"Error {r.status_code} al pedir {url}")
    return BeautifulSoup(r.text, 'html.parser')

def find_journal_url(title: str) -> str:
    q = quote_plus(title)
    url = SEARCH_BASE + q
    soup = scrap(url)
    row = soup.select_one('table#journalversion tbody tr')
    if not row:
        return None
    a = row.find('a', href=True)
    return DETAIL_BASE + a['href'] if a else None

def parse_journal_detail(url: str) -> dict:
    soup = scrap(url)
    info = {}
    # Título
    h2 = soup.select_one('div.journalheader > h2')
    info['title'] = h2.text.strip() if h2 else None
    # Publisher
    pub = soup.find('a', title="view all publisher's journals")
    info['publisher'] = pub.text.strip() if pub else None
    # SJR (2024)
    sjr = soup.find('p', class_='sjr')
    info['sjr_2024'] = sjr.text.strip() if sjr else None
    # H-Index
    hidx = soup.find('p', class_='hindexnumber')
    info['h_index'] = hidx.text.strip() if hidx else None
    # ISSN
    info['issn'] = [
        tag.find_next_sibling('p').text.strip()
        for tag in soup.find_all('div', string='ISSN')
        if tag.find_next_sibling('p')
    ]
    # Áreas temáticas
    info['areas'] = [
        li.text.split('\n')[0].strip()
        for li in soup.select('div#subjectarea ul li')
    ]
    return info

def save_json(data: dict, path: str):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ——— Función principal ———
def main():
    revistas = load_json(INPUT_JSON)
    resultados = {}
    for title in revistas:
        print(f"[INFO] Procesando «{title}»")
        url = find_journal_url(title)
        if url:
            try:
                resultados[title] = parse_journal_detail(url)
            except Exception as e:
                resultados[title] = {'error': f'Parse failed: {e}'}
        else:
            resultados[title] = {'error': 'URL no encontrada'}
        time.sleep(DELAY)
    save_json(resultados, OUTPUT_JSON)
    print(f"[OK] Resultados guardados en «{OUTPUT_JSON}»")

if __name__ == '__main__':
    main()