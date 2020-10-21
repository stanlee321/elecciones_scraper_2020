import time
import json
import os

from datetime import datetime
from flask import Flask, request

from main import EleccionesScraper

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World :D! THIS IS A DEV SERVER. I have been seen this...'

@app.route("/api/elecciones/download_data", methods=['POST', 'GET'])
def update_post():
    # Update post
    if request.method == 'GET':


        cwd = os.getenv("PROJ_DIR")

        # Create aux folder name for download files

        download_path = os.path.join(cwd, "tmp")

        # Open the selectors
        with open(f"{cwd}/selectors_nal.json") as a:
            selectors = json.load(a)

        # Create safe dir Folder 
        os.makedirs(download_path, exist_ok=True)  # succeeds even if directory exists.

        # Create Instance of the scraper
        elecciones = EleccionesScraper(project_path = cwd , download_dir = download_path)
        
        # Test main pipeline
        elecciones.main(selectors=selectors, headless=False, kind = "nal")
        
        elecciones.main_excel(selectors=selectors, headless=False)

        response = app.response_class(
            response=json.dumps(
                {
                    "response":  'DONE'
                }
            ),
            status=200,
            mimetype='application/json'
        )

        response.headers.add('Access-Control-Allow-Origin', '*')

        return response


    response = app.response_class(
            response=json.dumps({"response": "EXPECTED GET REQUEST" }),
            status=400,
            mimetype='application/json'
        )

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


