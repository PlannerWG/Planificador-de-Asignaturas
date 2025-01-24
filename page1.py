import streamlit as st
import subprocess

def carrera_vars():
    minors = ["Ninguno","Ingeniería de Gestión", "Operaciones y Manufactura", "Sistemas de Energía"]
    ing_limit = 5
    return ing_limit, minors
    # Entendiendo que las distintas carreras tienen distintas posibilidades en inglés mi idea
    # sería hacer un json o algo para las carreras, por ahora lo dejé en 5 ya que iccom sólo tiene hasta ing 5

st.title("Selecciona tu Escuela y Carrera")

# Lista de escuelas y carreras por escuela
# En la lista que son los valores del dict se pueden agregar las carreras a medida que las tengamos.
escuelas = {
    "Escuela de Ingeniería": ["Ingeniería Civil en Computación"],
}
escuela_seleccionada = st.selectbox("Selecciona una escuela", list(escuelas.keys()))

carreras = []

# Mostrar el segundo menú si se selecciona una escuela
if escuela_seleccionada != "Selecciona una opción":
    carreras = escuelas[escuela_seleccionada]
    carrera_seleccionada = st.selectbox("Selecciona una carrera", carreras)

    if carrera_seleccionada != "Selecciona una opción":
        st.success(f"Has seleccionado: {escuela_seleccionada} - {carrera_seleccionada}")
        ing_limit, minors = nivel_ingles()
        carrera_vars = st.selectbox("Grado inicial de inglés", range(1, ing_limit + 1))
        minor_elect = st.selectbox("Minor elegido", minors)

else:
    st.warning("Por favor, selecciona una escuela para continuar.")
    
