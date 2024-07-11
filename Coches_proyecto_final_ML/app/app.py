import streamlit as st
import pickle
import numpy as np

# Cargar el modelo entrenado
with open('xgb_aplicacion.pkl', 'rb') as file:
    model = pickle.load(file)

# Cargar los diccionarios
with open('marca_map.pkl', 'rb') as file:
    marca_map = pickle.load(file)

with open('modelo_map.pkl', 'rb') as file:
    modelo_map = pickle.load(file)

# Definir el diccionario para el tipo de cambio
my_cambio = {
    "Manual": 0,
    "Automático": 1
}

# Definir la interfaz de la aplicación
st.title("FONSICAR")
st.header('¿Quieres comprar o vender un coche de segunda mano?')
st.subheader('Introduce los datos del coche si quieres saber su valor aproximado')
# Crear entradas para los datos de entrada del modelo
year = st.number_input('Año del coche', min_value=1900, max_value=2024, step=1)
kms = st.number_input('Kilometraje', min_value=0)
power = st.number_input('Potencia (CV)', min_value=0)
marca = st.selectbox('Marca', list(marca_map.keys()))
modelo = st.selectbox('Modelo', list(modelo_map.keys()))
cambio = st.selectbox('Tipo de cambio', list(my_cambio.keys()))
prof_int = st.selectbox('¿Es el vendedor profesional?', ['No', 'Sí'])

# Procesar las entradas
def procesar_entrada(year, kms, power, marca, modelo, cambio, prof_int):
    marca_num = marca_map.get(marca, -1)  # -1 si no se encuentra la marca
    modelo_num = modelo_map.get(modelo, -1)  # -1 si no se encuentra el modelo
    cambio_num = my_cambio.get(cambio, -1)  # -1 si no se encuentra el tipo de cambio
    prof_int_num = 1 if prof_int == 'Sí' else 0
    
    return np.array([year, kms, power, marca_num, modelo_num, cambio_num, prof_int_num])

# Cuando se hace clic en el botón, realiza la predicción
if st.button("Predecir"):
    input_data = procesar_entrada(year, kms, power, marca, modelo, cambio, prof_int).reshape(1, -1)
    prediction = model.predict(input_data)
    st.write(f'El precio predicho es: {prediction[0]:.2f} €')