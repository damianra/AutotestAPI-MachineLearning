import pickle
import pandas as pd
from flask import Flask, jsonify, request, render_template
import sklearn

modelName = 'AutotestModel.sav'

app = Flask(__name__, template_folder='templates')
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
    clf = pickle.load(open(modelName, 'rb'))
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
    return jsonify({
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
    })


@app.route('/data')
def data():
    df = pd.read_csv('autotest.csv')
    json = df.to_json()
    return json


@app.route('/')
@app.route('/index')
def index():

    return render_template('index.html')


@app.route('/test', methods=['POST'])
def test():
    temp = request.form['temp']
    zona = request.form['zona']
    contacto = request.form['contacto']
    cansancio = request.form['cansancio']
    perOlf = request.form['perOlf']
    perGus = request.form['perGus']
    tos = request.form['tos']
    difRes = request.form['difRes']
    pacRiesgo = request.form['pacRiesgo']
    clf = pickle.load(open(modelName, 'rb'))
    df = pd.read_csv('autotest.csv')
    id = int(df.tail(1)['id'] + 1)
    pred = clf.predict([[float(temp),int(zona),int(contacto),int(cansancio),int(perOlf), int(perGus), int(tos), int(difRes), int(pacRiesgo)]])
    dic = {
            'id': id,
            'Temperatura': float(temp),
            'Zona de riesgo': int(zona),
            'Contacto con Algun enfermo': int(contacto),
            'Cansancio': int(cansancio),
            'Perd. Olfato': int(perOlf),
            'Perd. Gusto': int(perGus),
            'Tos o Dolor garganta': int(tos),
            'Dificultad Resp.': int(difRes),
            'Situacion de Riesgo': int(pacRiesgo),
            'Clasificacion': pred[0]
        }
    df = df.append([dic])
    print(dic)
    df.to_csv('autotest.csv', mode='w', index=False)

    return render_template('index.html', dic=dic)


if __name__ == '__main__':

    app.run(debug=False)
