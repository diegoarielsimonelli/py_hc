#!/usr/bin/env python
'''
Heart DB manager
---------------------------
Autor: Inove Coding School
Version: 1.2

Descripcion:
Programa creado para administrar la base de datos de registro de personas
'''

__author__ = "Inove Coding School"
__email__ = "alumnos@inove.com.ar"
__version__ = "1.2"


from flask.wrappers import Response
import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import func
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
import json
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Paciente(db.Model):
    __tablename__ = "paciente"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(String)
    telephone = db.Column(Integer)
    age = db.Column(Integer)
    nationality = db.Column(String)
    diagnosis = db.Column(String)
    treatment = db.Column(String)

    def __repr__(self):
        return f"Paciente:{self.name} con nacionalidad {self.nationality} con diagnóstico {self.diagnosis} y tratamiento para {self.treatment}"


def create_schema():
    # Borrar todos las tablas existentes en la base de datos
    # Esta linea puede comentarse sino se eliminar los datos
    db.drop_all()

    # Crear las tablas
    db.create_all()


def insert(name, age, nationality, telephone, diagnosis, treatment):
    # Crear una nueva persona
    person = Paciente(name=name, age=age, nationality=nationality,
                      telephone=telephone, diagnosis=diagnosis, treatment=treatment)

    # Agregar la persona a la DB
    db.session.add(person)
    db.session.commit()


def report(limit=0, offset=0):
    # Obtener todas las personas
    query = db.session.query(Paciente)
    if limit > 0:
        query = query.limit(limit)
        if offset > 0:
            query = query.offset(offset)

    json_result_list = []

    # De los resultados obtenidos pasar a un diccionario
    # que luego será enviado como JSON
    # TIP --> la clase Persona podría tener una función
    # para pasar a JSON/diccionario
    for person in query:
        json_result = {'name': person.name, 'age': person.age,
                       'nationality': person.nationality, 'treatment': person.treatment, 'telephone': person.telephone, 'diagnosis': person.diagnosis}
        json_result_list.append(json_result)

    return json_result_list


def diagnosis_report(diagnosis):
    user_diagnosis = db.session.query(Paciente).filter(
        Paciente.diagnosis == diagnosis.lower()).all()

    list_name = [x.name for x in user_diagnosis]
    list_age = [x.age for x in user_diagnosis]
    new_dict = dict(zip(list_name, list_age))

    fig = Figure()
    fig.tight_layout()

    ax = fig.add_subplot()
    ax.set_title("Pacientes con un mismo Diagnóstico y sus edades")
    ax.bar(new_dict.keys(), new_dict.values())
    ax.set_facecolor("r")
    ax.set_xlabel("Nombre del Paciente")
    ax.set_ylabel("Edad")

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
