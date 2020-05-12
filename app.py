# Librería pickle nos permite abrir nuestro modelo entrenado y crear un objeto.
import pickle
import pandas as pd
from flask import Flask, jsonify, request
# Es necesario tener instalada e importada la librería de Sklearn.
import sklearn

# Nombre del modelo en la carpeta
modelName = 'AutotestModel.sav'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'
app.config['JSON_SORT_KEYS'] = False


# Validación de números mayores o menores a los aceptados
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


# Ruta del autotest
# Abre el archivo del modelo y lo carga con pickle
# Válida los datos, realiza la predicción y antes de devolver la consulta
# guarda los resultados en un archivo csv.
@app.route('/autotest', methods=['POST'])
def autotest():
    file = open(modelName)
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



# Sirve para ver los resultados del csv con todos los autotest realizados.
@app.route('/data')
def data():
    df = pd.read_csv('autotest.csv')
    json = df.to_json()
    return json


if __name__ == '__main__':

    app.run(debug=False)
