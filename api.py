import pickle
import pandas as pd
from flask import jsonify
from flask_restful import Resource, reqparse

modelName = 'AutotestModel.sav'


class ApiTest(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('temp', help='This field cannot be blank', required=True, type=float)
        parser.add_argument('zona', help='This field cannot be blank', required=True, type=int)
        parser.add_argument('contacto', help='This field cannot be blank', required=True, type=int)
        parser.add_argument('cansancio', help='This field cannot be blank', required=True, type=int)
        parser.add_argument('perOlf', help='This field cannot be blank', required=True, type=int)
        parser.add_argument('perGus', help='This field cannot be blank', required=True, type=int)
        parser.add_argument('tos', help='This field cannot be blank', required=True, type=int)
        parser.add_argument('difRes', help='This field cannot be blank', required=True, type=int)
        parser.add_argument('pacRiesgo', help='This field cannot be blank', required=True, type=int)
        data = parser.parse_args()

        clf = pickle.load(open(modelName, 'rb'))
        df = pd.read_csv('autotest.csv')
        lista = validacionAutotest(data)
        pred = clf.predict([lista])
        id = int(df.tail(1)['id'] + 1)

        dic = {'id': id,
               'Temperatura': lista[0],
               'Zona de riesgo': lista[1],
               'Contacto con Algun enfermo': lista[2],
               'Cansancio': lista[3],
               'Perd. Olfato': lista[4],
               'Perd. Gusto': lista[5],
               'Tos o Dolor garganta': lista[6],
               'Dificultad Resp.': lista[7],
               'Situacion de Riesgo': lista[8],
               'Clasificacion': pred[0]
               }
        df = df.append([dic])
        df.to_csv('autotest.csv', mode='w', index=False)

        return jsonify({
            'data': dic,
            'disclaimer': 'El autotest no es oficial, es una recreacion con machine learning https://github.com/damianra/Autotest-Covid19-ML'
        })


def validacionAutotest(consulta):
    temperatura = float(consulta['temp'])
    zonaRiesgo = None
    contacto = None
    cansancio = None
    perdidaOlf = None
    perdidaGus = None
    tos = None
    dificultadRes = None
    pacRiesgo = None
    l = []

    if consulta['zona'] >= 1:
        zonaRiesgo = 1
    else:
        zonaRiesgo = 0
    if consulta['contacto'] >= 1:
        contacto = 1
    else:
        contacto = 0
    if consulta['cansancio'] >= 1:
        cansancio = 1
    else:
        cansancio = 0
    if consulta['perOlf'] >= 1:
        perdidaOlf = 1
    else:
        perdidaOlf = 0
    if consulta['perGus'] >= 1:
        perdidaGus = 1
    else:
        perdidaGus = 0
    if consulta['tos'] >= 1:
        tos = 1
    else:
        tos = 0
    if consulta['difRes'] >= 1:
        dificultadRes = 1
    else:
        dificultadRes = 0
    if consulta['pacRiesgo'] >= 1:
        pacRiesgo = 1
    else:
        pacRiesgo = 0
    l = [temperatura, zonaRiesgo, contacto, cansancio, perdidaOlf, perdidaGus, tos, dificultadRes, pacRiesgo]
    return l