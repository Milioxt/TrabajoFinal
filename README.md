# TrabajoFinal

#Requisitos 
Python 3.7+ instalado

#Dependencias:

- `requests`
- `beautifulsoup4`
- `unidecode`

## Notas

- El scraper hace una pausa de 1 segundo entre cada petición para no sobrecargar el servidor.
- El archivo de salida se actualiza automáticamente cada 5 revistas.
- Si una revista ya fue procesada, no se vuelve a consultar.


#Instalación
Clona este repositorio o descarga el script.\
Instala las dependencias:\
```bash
pip install requests beautifulsoup4 unidecode
```
Prepara tu archivo de entrada revistas.json en formato:\
Lista de títulos:\
[
  "Revista A",
  "Revista B",
  ...
]\
O diccionario (cualquier valor):\
{
  "Revista A": {},
  "Revista B": {}
}\
(si se da una lista el codigo del scrapper lo convierte en diccionario)

#Uso

```bash
python app.py
```

## ¿Qué información se obtiene?

Para cada revista se extraen los siguientes datos:

- `sitio_web`: Enlace oficial de la revista.
- `h_index`: Índice H de la revista.
- `subject_area`: Área temática principal.
- `publisher`: Editorial responsable.
- `issn`: Código ISSN de la revista.
- `widget`: URL de imagen del widget con el ranking SJR.
- `tipo_publicacion`: Tipo de publicación.
- `ultima_visita`: Fecha en que se realizó la consulta.

**Integrantes:**\
Emilio Portela Salido\
Mauricio Andres Huerta Teran\
Bryan Gallegos Solano
