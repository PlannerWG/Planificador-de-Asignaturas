import streamlit as st

st.title("Selecciona tu Escuela y Carrera")

# Lista de escuelas y carreras por escuela
# En la lista que son los valores del dict se pueden agregar las carreras a medida que las tengamos.
escuelas = {
    "Escuela de Ingeniería": ["Ingeniería Civil en Computación"],
}
escuela_seleccionada = st.selectbox("Selecciona una escuela", ["Selecciona una opción"] + list(escuelas.keys()))

carreras = []

# Mostrar el segundo menú si se selecciona una escuela
if escuela_seleccionada != "Selecciona una opción":
    carreras = escuelas[escuela_seleccionada]
    carrera_seleccionada = st.selectbox("Selecciona una carrera", ["Selecciona una opción"] + carreras)

    if carrera_seleccionada != "Selecciona una opción":
        st.success(f"Has seleccionado: {escuela_seleccionada} - {carrera_seleccionada}")
        st.button("Confirmar")
else:
    st.warning("Por favor, selecciona una escuela para continuar.")
