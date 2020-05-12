# AutotestAPI-MachineLearning
Github creación del modelo: <a href="https://github.com/damianra/Autotest-Covid19-ML">Link</a>
<br>
Aplicación flask con un solo endpoint.
<br>
<br>
"URL API"/autotest 
<br>
<br>
El cual recibe por método POST los datos de la consulta.
<br>
<br>
Parámetros de la consulta:<br>
-"temp" = Temperatura (float)<br>
-"zona" = Zona de Riesgo<br>
-"contacto" = Contacto con alguna persona infectada<br>
-"cansancio" = Cansancio<br>
-"perOlf" = Repentina perdida de olfato<br>
-"perGus" = Repentina perdida del gusto<br>
-"tos" = Tos o dolor de garganta<br>
-"difRes" = Dificultad respiratoria<br>
-"pacRiesgo" = Paciente de riesgo (Mayores a 60 años, afecciones como inmunodepresión o enfermedades crónicas cardíacas, pulmonares, renales, hepáticas, sanguíneas o metabólicas (por ejemplo, la diabetes)<br>
<br>
Todos los parámetros excepto la temperatura son valores 1 o 0, siendo 1 la respuesta SI y 0 la respuesta NO.
<br>
<br>

La API no es oficial.
Con los datos compartidos llega a un 93% de efectividad.
Se busca que al compartirla obtener más pruebas para aumentar el acierto del algoritmo.

Se utilizó el modelo de aprendizaje supervisado de Sklearn KNeighborsClassifier.<br>
Se lo entreno con un dataset con datos y clasificaciones de autotest (estos fueron generados manualmente).<br><br>
En la API se hacen comparaciones si el valor>=1 se modifica a 1 <br>
y si el valor<=0 se modifica a 0.
<br>
<br>
<br>
<b>Nota:</b> Falta agregar condición para que los valores no sean nulos.

