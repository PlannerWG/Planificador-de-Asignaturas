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
escuela_seleccionada = st.selectbox("Selecciona una escuela", ["Selecciona una opción"] + list(escuelas.keys()))

carreras = []

# Mostrar el segundo menú si se selecciona una escuela
if escuela_seleccionada != "Selecciona una opción":
    carreras = escuelas[escuela_seleccionada]
    carrera_seleccionada = st.selectbox("Selecciona una carrera", ["Selecciona una opción"] + carreras)

    if carrera_seleccionada != "Selecciona una opción":
        st.success(f"Has seleccionado: {escuela_seleccionada} - {carrera_seleccionada}")
        ing_limit, minors = carrera_vars()
        niv_ing = st.selectbox("Grado inicial de inglés", ["Selecciona una opción"] + list(range(1, ing_limit + 1)))
        minor_elect = st.selectbox("Minor elegido", ["Selecciona una opción"] + minors)
        recomendados = st.selectbox("Usar ramos recomendados", ["Selecciona una opción"] + ["Sí", "No"])

else:
    st.warning("Por favor, selecciona una escuela para continuar.")
    
def abrir_info(escuela_seleccionada,carrera_seleccionada): # Me faltaría hacer un switch o algo así para que las escuelas cuadren.
    base_url = f"https://api.github.com/repos/PlannerWG/Planificador-de-Asignaturas/contents/{escuela_seleccionada}/{carrera_seleccionada}"
    archivos = ["Ramos.json", "ENG_CFG.json", "Ramos_Minors.json", "Electivos.json", "Ramos_XOR.json"]
    
    for archivo in archivos:
        archivo_url = f"{base_url}/{archivo}"
        try:
            response = requests.get(archivo_url, headers=headers)
            response.raise_for_status()
            archivo_data = json.loads(response.json()['content'])
            datos[archivo.replace(".json", "")] = archivo_data
        except requests.exceptions.RequestException as e:
            st.warning(f"Error al obtener el archivo {archivo}: {e}")
    
    return datos # Este diccionario funcionaría similar a las variables que se usaban en el código local.


#if all(var != "Selecciona una opción" for var in [niv_ing, minor_elect, recomendados]):
    #abrir_info(escuela_seleccionada,carrera_seleccionada)


