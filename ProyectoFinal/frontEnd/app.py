''' Programa principal de Página proyecto final '''

from flask import Flask, request, url_for, render_template, redirect, flash, session
from functions import get_authors

import json
import os
import random

app = Flask(__name__)

with open("data/salida_final.json", "r", encoding="utf-8") as f:
    revistas_data = json.load(f)

@app.route('/')
def index():
    ''' Pagina principal de la aplicacion '''
    return render_template('index.html')

@app.route('/area')
def area():
    ''' Area '''
    areas_unicas = set()

    for v in revistas_data.values():
        if isinstance(v.get("subject_area"), str):
            for area in v["subject_area"].split(','):
                areas_unicas.add(area.strip())

    return render_template("area.html", areas=sorted(areas_unicas))

@app.route('/catalogs')
def catalogs():
    ''' Catalogs '''
    catalogos_unicos = sorted(set(
    v["tipo_publicacion"].strip()
    for v in revistas_data.values()
    if v.get("tipo_publicacion") and isinstance(v.get("tipo_publicacion"), str)
))
    return render_template("catalogs.html", catalogos=catalogos_unicos)

@app.route('/explore')
def explorar():
    letras = sorted(set([titulo[0].upper() for titulo in revistas_data.keys() if titulo[0].isalpha()]))
    return render_template("explore.html", letras=letras)

@app.route("/explore/<letra>")
def revistas_por_letra(letra):
    letra = letra.upper()
    revistas_filtradas = {
        k: v for k, v in revistas_data.items() if k.strip().upper().startswith(letra)
    }
    print(f"Filtradas con '{letra}': {len(revistas_filtradas)} revistas")
    return render_template("revistas_por_letra.html", letra=letra, revistas=revistas_filtradas)

@app.route("/mag/<nombre>")
def revista_detalle(nombre):
    revista = revistas_data.get(nombre)
    if not revista:
        return f"Revista '{nombre}' no encontrada", 404
    return render_template("revista_detalle.html", nombre=nombre, revista=revista)

@app.route("/catalogs/<nombre>")
def catalogo_detalle(nombre):
    nombre_normalizado = nombre.strip().lower()

    revistas_catalogo = {
        k: v for k, v in revistas_data.items()
        if isinstance(v.get("tipo_publicacion"), str) and v["tipo_publicacion"].strip().lower() == nombre_normalizado
    }

    return render_template("catalogo_detalle.html", nombre=nombre, revistas=revistas_catalogo)

@app.route("/area/<nombre>")
def area_detalle(nombre):
    nombre_normalizado = nombre.strip().lower()
    revistas_area = {}

    for k, v in revistas_data.items():
        if isinstance(v.get("subject_area"), str):
            areas = [a.strip().lower() for a in v["subject_area"].split(',')]
            if nombre_normalizado in areas:
                revistas_area[k] = v

    return render_template("area_detalle.html", nombre=nombre, revistas=revistas_area)

@app.route('/search')
def search():
    ''' Search '''
    query = request.args.get("q", "").strip().lower()
    resultados = {}

    if query:
        palabras = query.split()
        for titulo, info in revistas_data.items():
            titulo_limpio = titulo.lower()
            if any(palabra in titulo_limpio for palabra in palabras):
                resultados[titulo] = info

    return render_template("search.html", resultados=resultados, query=query)

@app.route('/credits')
def credits():
    authors = get_authors()
    ''' Credits '''
    return render_template('credits.html', authors=authors)


if __name__ == '__main__':
    app.run(debug=True)