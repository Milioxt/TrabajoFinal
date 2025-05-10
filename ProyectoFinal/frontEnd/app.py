''' Programa principal de Página proyecto final '''

from flask import Flask, request, url_for, render_template, redirect, flash, session
from functions import get_authors

import os
import random

app = Flask(__name__)

@app.route('/')
def index():
    ''' Pagina principal de la aplicacion '''
    return render_template('index.html')

@app.route('/area')
def area():
    ''' Area '''
    return render_template('area.html')

@app.route('/catalogs')
def catalogs():
    ''' Catalogs '''
    return render_template('catalogs.html')

@app.route('/explore')
def explore():
    ''' Explore '''
    return render_template('explore.html')

@app.route('/search')
def search():
    ''' Search '''
    return render_template('search.html')

@app.route('/credits')
def credits():
    authors = get_authors()
    ''' Credits '''
    return render_template('credits.html', authors=authors)


if __name__ == '__main__':
    app.run(debug=True)