''' Programa principal de Página proyecto final '''

from flask import Flask, request, url_for, render_template, redirect, flash, session
from functions import get_authors, cargar_guardados, guardar_guardados
from werkzeug.security import generate_password_hash, check_password_hash

import json
import os
import random

app = Flask(__name__)
app.secret_key = 'clave_secreta_segura'
usuarios = {
    "mauricio": generate_password_hash("12345"),
    "emilio": generate_password_hash("emili0"),
    "bryan": generate_password_hash("mozz")
}

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

@app.route('/catalogs')
def catalogs():
    ''' Catalogs '''
    catalogos_unicos = sorted(set(
    v["tipo_publicacion"].strip()
    for v in revistas_data.values()
    if v.get("tipo_publicacion") and isinstance(v.get("tipo_publicacion"), str)
))
    return render_template("catalogs.html", catalogos=catalogos_unicos)

@app.route("/catalogs/<nombre>")
def catalogo_detalle(nombre):
    nombre_normalizado = nombre.strip().lower()

    revistas_catalogo = {
        k: v for k, v in revistas_data.items()
        if isinstance(v.get("tipo_publicacion"), str) and v["tipo_publicacion"].strip().lower() == nombre_normalizado
    }

    return render_template("catalogo_detalle.html", nombre=nombre, revistas=revistas_catalogo)

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

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pw = request.form["password"]

        if user in usuarios and check_password_hash(usuarios[user], pw):
            session["logged_in"] = True
            session["username"] = user
            session.setdefault("guardados", {})  # Diccionario por usuario
            flash("Inicio de sesión exitoso", "success")
            return redirect("/")
        else:
            flash("Credenciales incorrectas", "danger")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión", "info")
    return redirect("/")

@app.route("/guardar/<nombre>")
def guardar_revista(nombre):
    if not session.get("logged_in"):
        flash("Debes iniciar sesión para guardar revistas", "warning")
        return redirect(url_for("login"))

    user = session["username"]
    guardados = cargar_guardados()

    guardados.setdefault(user, [])
    if nombre not in guardados[user]:
        guardados[user].append(nombre)
        flash("Revista guardada", "success")
        guardar_guardados(guardados)
    else:
        flash("Ya habías guardado esta revista", "info")

    return redirect(url_for("revista_detalle", nombre=nombre))

@app.route("/saved")
def saved():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    user = session["username"]
    guardados = cargar_guardados().get(user, [])

    revistas_guardadas = {k: revistas_data[k] for k in guardados if k in revistas_data}
    return render_template("saved.html", revistas=revistas_guardadas)


if __name__ == '__main__':
    app.run(debug=True)