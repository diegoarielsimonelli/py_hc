#!/usr/bin/env python


from config import config
import paciente
import matplotlib.image as mpimg
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.pyplot as plt
import traceback
import io
import sys
import os
import base64
import json
import sqlite3
from datetime import datetime, timedelta
import numpy as np
from flask import Flask, request, jsonify, render_template, Response, redirect, url_for
import matplotlib
# For multi thread, non-interactive backend (avoid run in main loop)
matplotlib.use('Agg')


app = Flask(__name__)

# Obtener la path de ejecución actual del script
script_path = os.path.dirname(os.path.realpath(__file__))

# Obtener los parámetros del archivo de configuración
config_path_name = os.path.join(script_path, 'config.ini')
db_config = config('db', config_path_name)
server_config = config('server', config_path_name)

# Indicamos al sistema (app) de donde leer la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_config['database']}"
# Asociamos nuestro controlador de la base de datos con la aplicacion
paciente.db.init_app(app)


# Ruta que se ingresa por la ULR 127.0.0.1:5000
@app.route("/")
def index():
    try:

        if os.path.isfile(db_config['database']) == False:
            # Sino existe la base de datos la creo
            paciente.create_schema()

        # En el futuro se podria realizar una página de bienvenida
        return redirect(url_for('pacientes'))
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/api")
def api():
    try:
        # Imprimir los distintos endopoints disponibles
        result = "<h1>Bienvenido!!</h1>"
        result += "<h2>Endpoints disponibles:</h2>"
        result += "<h3>[GET] /reset --> borrar y crear la base de datos</h3>"
        result += "<h3>[GET] /pacientes --> mostrar la tabla de pacientes. </h3>"
        result += "<h3>[GET] /registro --> mostrar el HTML con el formulario de registro de pacientes</h3>"
        result += "<h3>[GET] /comparativa/ --> mostrar un gráfico que compare cuantas personas con el mismo Diagnóstico. </h3>"

        return(result)
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/reset")
def reset():
    try:
        # Borrar y crear la base de datos
        paciente.create_schema()
        result = "<h3>Base de datos re-generada!</h3>"
        return (result)
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/pacientes")
def pacientes():
    try:

        data = paciente.report()

        return render_template('tabla.html', data=data)
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/comparativa/<diagnosis>")
def comparativa(diagnosis):
    try:

        return paciente.diagnosis_report(diagnosis)
    except:
        return jsonify({'trace': traceback.format_exc()})


@app.route("/registro", methods=['GET', 'POST'])
def registro():
    if request.method == 'GET':
        try:
            return render_template('registro.html')
        except:
            return jsonify({'trace': traceback.format_exc()})

    if request.method == 'POST':
        try:

            name = str(request.form.get('name'))
            age = str(request.form.get('age'))
            nationality = str(request.form.get('nationality'))
            diagnosis = str(request.form.get('diagnosis'))
            treatment = str(request.form.get('treatment'))
            telephone = str(request.form.get('telephone'))

            if (name is None or nationality is None or diagnosis is None or treatment is None or telephone is None or age is None or age.isdigit() is False):
                return Response(status=400)
            paciente.insert(name, int(age), int(telephone), treatment.lower(),
                            diagnosis.lower(), nationality.lower())
            return redirect(url_for('pacientes'))
        except:
            return jsonify({'trace': traceback.format_exc()})


if __name__ == '__main__':
    print('Servidor arriba!')

    app.run(host=server_config['host'],
            port=server_config['port'],
            debug=True)
