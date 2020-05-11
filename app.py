import pickle
import pandas as pd
from flask import Flask, jsonify, request
import sklearn

modelName = 'AutotestModel.sav'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'snvu124qchmf9483rcrc2er15q3f1ado13403'
app.config['JSON_SORT_KEYS'] = False


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

    if int(consulta['zona']) >= 1:
        zonaRiesgo = 1
    else:
        zonaRiesgo = 0
    if int(consulta['contacto']) >= 1:
        contacto = 1
    else:
        contacto = 0
    if int(consulta['cansancio']) >= 1:
        cansancio = 1
    else:
        cansancio = 0
    if int(consulta['perOlf']) >= 1:
        perdidaOlf = 1
    else:
        perdidaOlf = 0
    if int(consulta['perGus']) >= 1:
        perdidaGus = 1
    else:
        perdidaGus = 0
    if int(consulta['tos']) >= 1:
        tos = 1
    else:
        tos = 0
    if int(consulta['difRes']) >= 1:
        dificultadRes = 1
    else:
        dificultadRes = 0
    if int(consulta['pacRiesgo']) >= 1:
        pacRiesgo = 1
    else:
        pacRiesgo = 0
    l = [temperatura, zonaRiesgo, contacto, cansancio, perdidaOlf, perdidaGus, tos, dificultadRes, pacRiesgo]
    return l


@app.route('/autotest', methods=['POST'])
def autotest():
    df = pd.read_csv('autotest.csv')
    consulta = request.get_json()
    lista = validacionAutotest(consulta)
    id = int(df.tail(1)['id'] + 1)
    pred = clf.predict([lista])
    data = { 'id': id,
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
    # df2 = pd.DataFrame(data)
    df = df.append([data])
    df.to_csv('autotest.csv', mode='w', index=False)
    return jsonify({'pred': pred[0]})


if __name__ == '__main__':
    file = open(modelName)
    clf = pickle.load(open(modelName, 'rb'))

    app.run(debug=False)