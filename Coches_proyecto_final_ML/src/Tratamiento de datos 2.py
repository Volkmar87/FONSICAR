
# Tratamiento de datos 2, continuacion

#Elimino los valores nan de las categorias shift y color
df_limpio = df2.dropna(subset=['shift', 'color'])


#Genero una columna nueva ordenando las marcas por su media agrupada:


# Calcular la media de los precios por marca (make)
mean_prices_make = df_limpio.groupby('make')['price'].mean().reset_index()

# Ordenar las marcas por la media del precio de menor a mayor
mean_prices_make_sorted = mean_prices_make.sort_values(by='price')

# Asignar un número a cada marca en función del orden
mean_prices_make_sorted['make_number'] = range(1, len(mean_prices_make_sorted) + 1)

# Unir esta información con el DataFrame original
df_limpio2 = df_limpio.merge(mean_prices_make_sorted[['make', 'make_number']], on='make', how='left')


#Genero una columna nueva ordenando los modelos por su media agrupada



# Calcular la media de los precios por modelo (model)
mean_prices_model = df_limpio.groupby('model')['price'].mean().reset_index()

# Ordenar los modelos por la media del precio de menor a mayor
mean_prices_model_sorted = mean_prices_model.sort_values(by='price')

# Asignar un número a cada modelo en función del orden
mean_prices_model_sorted['model_number'] = range(1, len(mean_prices_model_sorted) + 1)

# Unir esta información con el DataFrame original
df_limpio2 = df_limpio2.merge(mean_prices_model_sorted[['model', 'model_number']], on='model', how='left')


#Genero una columna nueva combinando la ordenacion de la marca y ordenando los modelos por marca para crear una codificacion nueva que incluye las dos codificaciones


# Calcular la media del precio por cada modelo dentro de cada marca
mean_model_prices = df_limpio2.groupby(['make', 'model'])['price'].mean().reset_index()

# Ordenar los modelos dentro de cada marca por el precio medio
mean_model_prices = mean_model_prices.sort_values(by=['make', 'price'])

# Asignar un número a cada modelo dentro de cada marca en función del orden
mean_model_prices['model_numberdos'] = mean_model_prices.groupby('make').cumcount() + 1

# Unir esta información con el DataFrame original
df_limpio2 = df_limpio2.merge(mean_model_prices[['make', 'model', 'model_numberdos']], on=['make', 'model'], how='left')

# Crear una referencia única multiplicando make_number por 100 y sumando model_number
df_limpio2['make_model_ref'] = df_limpio2['make_number'] * 100 + df_limpio2['model_numberdos']


#Genero una columna nueva con los tipos de combustible codificados

my_fuel = {
    "Diésel": 0,
    "Gasolina": 1,
    "Gas natural (CNG)": 2,
    "Gas licuado (GLP)": 3,
    "Híbrido": 4,
    "Híbrido enchufable": 5,
    "Eléctrico": 6
}

df_limpio2['combustible_int'] = df_limpio2['fuel'].map(my_fuel)
df_limpio2.head()

#Genero una columna nueva codificando las provicias con un numero
label_encoder = LabelEncoder()

# Codificar las provincias
df_limpio2['provincia_numero'] = label_encoder.fit_transform(df_limpio2['province'])

#Genero una columna nueva codificando los tipos de cambio
my_cambio = {
    "Manual": 0,
    "Automático": 1
}

df_limpio2['cambio_int'] = df_limpio2['shift'].map(my_cambio)
df_limpio2.head()


#Convierto la columna profesional de booleano a int

df_limpio2['prof_int'] = df_limpio2['is_professional'].astype(int)
df_limpio2.head()

import re
def limpiar_nombre(nombre):
    return re.sub(r'\([^)]*\)', '', nombre).strip()

# Aplicar la función al DataFrame
df_limpio2['color_limpio'] = df_limpio2['color'].apply(limpiar_nombre)

label_encoder = LabelEncoder()

df_limpio2['color_numero'] = label_encoder.fit_transform(df_limpio2['color_limpio'])


#Genero una nueva columna con los km0
df_limpio2['km_0'] = df_limpio2['kms'] < 10000
df_limpio2['km_0_int'] = df_limpio2['km_0'].astype(int)
df_limpio2.head()


percentil_75 = df_limpio2['price'].quantile(0.75)

# Dividir el dataframe en dos partes
df_limpio3 = df_limpio2[df_limpio2['price'] <= percentil_75]
df_premium = df_limpio2[df_limpio2['price'] > percentil_75]

# Verificar la cantidad de registros en cada dataframe
print("Registros en df_bajo_percentil_75:", len(df_limpio3))
print("Registros en df_alto_percentil_75:", len(df_premium))

# Mostrar los primeros registros de cada dataframe
print("Primeros registros de df_bajo_percentil_75:")
print(df_limpio3.head())

print("Primeros registros de df_alto_percentil_75:")
print(df_premium.head())