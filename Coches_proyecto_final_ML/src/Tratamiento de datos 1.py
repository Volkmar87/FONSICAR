import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures, StandardScaler, MinMaxScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.impute import KNNImputer

#Leemos el csv
df1 = pd.read_csv('coches-de-segunda-mano-sample.csv')
df1

#Dropeo las columnas que no voy a usar
df1.drop(columns= ['url', 'company','dealer','price_financed','publish_date', 'insert_date','country'],inplace=True)

#Relleno los modelos que faltan con valores obtenidos mediante investigacion
relleno_modelos = {1330: "Córdoba", 25574:"Toledo", 31826: "Córdoba", 32831: "León", 37683: "Toledo"}

for indice, valor in relleno_modelos.items():
    df1.at[indice,'model']=valor

#Relleno los años que faltan con valores obtenidos mediante investigacion
relleno_años = {31025: 2022.0, 42075: 2018.0}
for indice, valor in relleno_años.items():
    df1.at[indice,'year']=valor

#Relleno los combustibles desconocidos que faltan con valores obtenidos mediante investigacion
relleno_fuel = {26639:"Híbrido",37786:"Gasolina"}

for indice, valor in relleno_fuel.items():
    df1.at[indice,'fuel']=valor

#Relleno los valores descnocidos de las marcas que faltan con valores obtenidos mediante investigación
df1['make'] = df1['make'].fillna('INVICTA')


#Relleno los valores con el valor más repetido
df1['province'] = df1['province'].fillna('Madrid')


#Elimino los registros con valores Nan en la potencia
df2 = df1.dropna(subset=['power'])

