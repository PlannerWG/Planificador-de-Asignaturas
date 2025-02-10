import streamlit as st
import subprocess
import requests
import base64
import json
import unicodedata

#####################################################################################################
#####################################################################################################
#####################################################################################################
                                 # FUNCIONES
#####################################################################################################
#####################################################################################################
#####################################################################################################


# Inicialización de GITHUB
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]
headers = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {GITHUB_TOKEN}" # El token queda inaccesible sin el acceso al dev de la app.
} # Evita que GITHUB rechace la operación

# Esta función cumple con emparejar los nombres que ve el usuario en el botón respecto a como se llaman realmente las carpetas.
def cargar_mapeo(nombre_archivo):
    url = f"https://api.github.com/repos/PlannerWG/Planificador-de-Asignaturas/contents/{nombre_archivo}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza un error si la petición falla

        contenido_base64 = response.json().get("content", "")
        if contenido_base64:
            contenido_decodificado = base64.b64decode(contenido_base64).decode("utf-8")
            return json.loads(contenido_decodificado)
        else:
            st.warning(f"El archivo {nombre_archivo} está vacío o no se pudo obtener correctamente.")
            return {}
    except requests.exceptions.RequestException as e:
        st.error(f"Error al cargar {nombre_archivo}: {e}")
        return {}

map_carr = cargar_mapeo("map_carr.json")
map_esc = cargar_mapeo("map_esc.json")

def abrir_info(escuela_seleccionada,carrera_seleccionada): # Me faltaría hacer un switch o algo así para que las escuelas cuadren.
    escuela_seleccionada = map_esc[escuela_seleccionada]
    carrera_seleccionada = map_carr[carrera_seleccionada]
    base_url = f"https://api.github.com/repos/PlannerWG/Planificador-de-Asignaturas/contents/escuela/{escuela_seleccionada}/{carrera_seleccionada}"
    archivos = ["Ramos.json", "ENG_CFG.json", "Ramos_Minors.json", "Electivos.json", "Ramos_XOR.json", "Info.json"]
    datos = {}

    for archivo in archivos:
        archivo_url = f"{base_url}/{archivo}"
        try:
            response = requests.get(archivo_url, headers=headers)
            response.raise_for_status()
            # Codificando para que se pueda usar
            contenido_base64 = response.json().get("content", "")
            if contenido_base64:
                contenido_decodificado = base64.b64decode(contenido_base64).decode("utf-8")
                datos[archivo.replace(".json", "")] = json.loads(contenido_decodificado)
            else:
                st.warning(f"El archivo {archivo} está vacío o no se pudo obtener correctamente.")
        except requests.exceptions.RequestException as e:
            st.warning(f"Error al obtener el archivo {archivo}: {e}")
    
    return datos # Este diccionario funcionaría similar a las variables que se usaban en el código local

def carrera_vars():
    datos = abrir_info(escuela_seleccionada,carrera_seleccionada)
    minors = datos["Info"]
    ing_limit = 5 # Esto hay que trabajarlo para cuando haya más carreras
    return ing_limit, minors
    # Entendiendo que las distintas carreras tienen distintas posibilidades en inglés mi idea
    # sería hacer un json o algo para las carreras, por ahora lo dejé en 5 ya que iccom sólo tiene hasta ing 5

def quitar_tildes(texto):
    # Normalizamos el texto y eliminamos los acentos
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

#####################################################################################################
#####################################################################################################
#####################################################################################################
                                   # Aplicación
#####################################################################################################
#####################################################################################################
#####################################################################################################

niv_ing = "Selecciona una opción"
minor_elect = "Selecciona una opción"
flag = False

# Título de la App
st.title("Selecciona tu Escuela y Carrera")

################### Interacción de usuario
# Lista de escuelas y carreras por escuela
# Se podría cargar un mapeo igual a medida que se agreguen escuelas y carreras.
escuelas = {
    "Escuela de Ingeniería": ["Ingeniería Civil en Computación"],
}
escuela_seleccionada = st.selectbox("Selecciona una escuela", ["Selecciona una opción"] + list(escuelas.keys()))

# Mostrar el segundo menú si se selecciona una escuela
if escuela_seleccionada != "Selecciona una opción":
    carreras = escuelas[escuela_seleccionada]
    carrera_seleccionada = st.selectbox("Selecciona una carrera", ["Selecciona una opción"] + carreras)
    if carrera_seleccionada != "Selecciona una opción":
        st.success(f"Has seleccionado: {escuela_seleccionada} - {carrera_seleccionada}")
        ing_limit, info = carrera_vars()
        grado_eng = st.selectbox("Grado inicial de inglés", ["Selecciona una opción"] + list(range(1, ing_limit + 1)))
        minor_elect = st.selectbox("Minor elegido", ["Selecciona una opción"] + info["Minors"])
        if grado_eng != "Selecciona una opción" and minor_elect != "Selecciona una opción":
            st.success(f"Nivel inicial de inglés: {grado_eng} - Minor: {minor_elect}")
            flag = True
            cant_electivos = info["Electivos"]
            cant_electivos_esp = info["Electivos especialidad"]
else:
    st.warning("Por favor, selecciona una escuela para continuar.")

############# Inicialización de la lógica
if flag:
    datos = abrir_info(escuela_seleccionada,carrera_seleccionada)

    # Consideré usar .get y dar un valor base ya que no sé si en UCONCE los ramos tendrán las mismas características
    ramos_electivos = datos.get("Electivos", [])
    ramos = datos.get("Ramos", [])
    eng_cfg = datos.get("ENG_CFG", [])
    ramos_minors = datos.get("Ramos_Minors", [])
    ramos_xor = datos.get("Ramos_XOR", [])

    if minor_elect != "Ninguno":
        minor_elect = quitar_tildes(minor_elect)
        ramos_minors = [ramo for ramo in ramos_minors if ramo["minor"] == minor_elect] #Filtra en base al minor elegido

    lista_minors = [[ramo["module_name"], ramo["recommended_semester"]] for ramo in ramos_minors]
    lista_electivos = [[ramo["module_name"], ramo["recommended_semester"]] for ramo in ramos_electivos]
    lista_xors = [[ramo["module_name"], ramo["recommended_semester"]] for ramo in ramos_xor]

    # El siguiente bloque trabaja en conjunto, es importante señalar que elimina del dict los inglés aprobados y borra el prerrequisito del primero que puede tomar.
    for i in range(5):
        if grado_eng>(i+1):
            eng_cfg.pop(0)
        else:
            eng_cfg.pop(5)
    eng_cfg[0]["prerequisites"]=list()

    for ramo in eng_cfg:
        ramos.append(ramo)

    st.markdown(f"##### Elija los electivos de carrera. Se deben seleccionar {info["XOR"]} ramo(s).")

    # Crear checkboxes para cada electivo
    elec_selec = []
    st.write("Selecciona tus electivos:")
    for electivo in lista_electivos:
        nombre = electivo[0]  # Solo usamos el nombre
        if st.checkbox(nombre, key=nombre):
            elec_selec.append(nombre)

    # Validar selección
    if len(elec_selec) < info["XOR"]:
        st.warning(f"Debes seleccionar exactamente {info['XOR']} electivos. Te faltan {info['XOR'] - len(elec_selec)}.")
    elif len(elec_selec) > info["XOR"]:
        st.error(f"Debes seleccionar exactamente {info['XOR']} electivos. Te has pasado por {len(elec_selec) - info['XOR']}.")
    else:
        st.success(f"Has seleccionado correctamente tus {info['XOR']} electivos: {', '.join(elec_selec)}")