import streamlit as st

st.title("Selecciona tu Escuela y Carrera")

# Lista de escuelas y carreras por escuela
escuelas = {
    "Escuela de Ingeniería": ["Ingeniería Civil en Computación"],
}

# Inicializar estado para la selección
if "escuela_seleccionada" not in st.session_state:
    st.session_state.escuela_seleccionada = "Selecciona una opción"

# Menú desplegable de escuelas
escuela_seleccionada = st.selectbox(
    "Selecciona una escuela",
    [st.session_state.escuela_seleccionada] + list(escuelas.keys()),
)

# Actualizar la selección de la escuela en el estado
if escuela_seleccionada != "Selecciona una opción":
    st.session_state.escuela_seleccionada = escuela_seleccionada

# Mostrar el segundo menú si se selecciona una escuela
if escuela_seleccionada != "Selecciona una opción":
    carreras = escuelas[escuela_seleccionada]

    # Inicializar estado para la selección de carrera
    if "carrera_seleccionada" not in st.session_state:
        st.session_state.carrera_seleccionada = "Selecciona una opción"

    carrera_seleccionada = st.selectbox(
        "Selecciona una carrera",
        [st.session_state.carrera_seleccionada] + carreras,
    )

    # Actualizar la selección de la carrera en el estado
    if carrera_seleccionada != "Selecciona una opción":
        st.session_state.carrera_seleccionada = carrera_seleccionada
        st.success(f"Has seleccionado: {escuela_seleccionada} - {carrera_seleccionada}")

else:
    st.warning("Por favor, selecciona una escuela para continuar.")
