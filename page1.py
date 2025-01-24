import streamlit as st

# Título de la aplicación
st.title("Selecciona tu Escuela y Carrera")

# Lista de escuelas y carreras por escuela
escuelas = {
    "Escuela de Ingeniería": ["Ingeniería Civil", "Ingeniería de Sistemas", "Ingeniería Industrial"],
    "Escuela de Medicina": ["Medicina General", "Enfermería", "Biotecnología"],
    "Escuela de Arte": ["Diseño Gráfico", "Bellas Artes", "Fotografía"]
}

# Selección de la escuela
escuela_seleccionada = st.selectbox("Selecciona una escuela", ["Selecciona una opción"] + list(escuelas.keys()))

# Inicializar variable para carreras
carreras = []

# Mostrar el segundo menú si se selecciona una escuela
if escuela_seleccionada != "Selecciona una opción":
    carreras = escuelas[escuela_seleccionada]
    carrera_seleccionada = st.selectbox("Selecciona una carrera", ["Selecciona una opción"] + carreras)

    # Mostrar confirmación
    if carrera_seleccionada != "Selecciona una opción":
        st.success(f"Has seleccionado: {escuela_seleccionada} - {carrera_seleccionada}")
else:
    st.warning("Por favor, selecciona una escuela para continuar.")
