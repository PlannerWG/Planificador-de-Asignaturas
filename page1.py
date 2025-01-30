import streamlit as st
import subprocess
import requests
import base64

#####################################################################################################
#####################################################################################################
#####################################################################################################
                                 # FUNCIONES
#####################################################################################################
#####################################################################################################
#####################################################################################################

headers = {"Accept": "application/vnd.github.v3+json"} # Evita que GITHUB rechace la operación
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
    base_url = f"https://api.github.com/repos/PlannerWG/Planificador-de-Asignaturas/contents/{escuela_seleccionada}/{carrera_seleccionada}"
    archivos = ["Ramos.json", "ENG_CFG.json", "Ramos_Minors.json", "Electivos.json", "Ramos_XOR.json", "Minors.json"]
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
    minors = datos["Minors"]
    ing_limit = 5 # Esto hay que trabajarlo para cuando haya más carreras
    return ing_limit, minors
    # Entendiendo que las distintas carreras tienen distintas posibilidades en inglés mi idea
    # sería hacer un json o algo para las carreras, por ahora lo dejé en 5 ya que iccom sólo tiene hasta ing 5

#####################################################################################################
#####################################################################################################
#####################################################################################################
                                   # Aplicación
#####################################################################################################
#####################################################################################################
#####################################################################################################

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
        ing_limit, minors = carrera_vars()
        niv_ing = st.selectbox("Grado inicial de inglés", ["Selecciona una opción"] + list(range(1, ing_limit + 1)))
        minor_elect = st.selectbox("Minor elegido", ["Selecciona una opción"] + minors)
        recomendados = st.selectbox("Usar ramos recomendados", ["Selecciona una opción"] + ["Sí", "No"])
else:
    st.warning("Por favor, selecciona una escuela para continuar.")

############# Inicialización de la lógica
if all(var != "Selecciona una opción" for var in [niv_ing, minor_elect, recomendados]):
    datos = abrir_info(escuela_seleccionada,carrera_seleccionada)

    # Consideré usar .get y dar un valor base ya que no sé si en UCONCE los ramos tendrán las mismas características
    ramos_electivos = datos.get("Electivos", [])
    ramos = datos.get("Ramos", [])
    eng_cfg = datos.get("ENG_CFG", [])
    ramos_minors = datos.get("Ramos_Minors", [])
    ramos_xor = datos.get("Ramos_XOR", [])

    if minor_elect != "Ninguno":
        ramos_minors = [ramo for ramo in ramos_minors if ramo["minor"] == minor_resp] #Filtra en base al minor elegido

    if recomendados== "Si":
        minors_recomendados=list()
        contador_minors = 0
        for minor in ramos_minors:
            if minor["recomendado"]:
                minors_recomendados.append(minor["module_name"])
                ramos.append(minor)
                contador_minors += 1
                if contador_minors == 3:
                    break
        for electivo in ramos_electivos:
            if electivo["recomendado"]:
                electivo_recomendado=electivo["module_name"]
                ramos.append(electivo)
                break
        for xor in ramos_xor:
            if xor["recomendado"]:
                xor_recomendado=xor["module_name"]
                ramos.append(xor)
                for ramo in ramos:
                    if ramo["id"] == "COM3002":
                        ramo["prerequisites"].append(xor["id"])
                        break
                break

    lista_minors=list()
    for ramo in ramos_minors:
        lista_minors.append(ramo["module_name"])

    lista_electivos=list()
    for ramo in ramos_electivos:
        lista_electivos.append(ramo["module_name"])

    lista_xors=list()
    for ramo in ramos_xor:
        lista_xors.append(ramo["module_name"])

    # El siguiente bloque trabaja en conjunto, es importante señalar que elimina del dict los inglés aprobados y borra el prerrequisito del primero que puede tomar.
    for i in range(5):
        if grado_eng>(i+1):
            eng_cfg.pop(0)
        else:
            eng_cfg.pop(5)
    eng_cfg[0]["prerequisites"]=list()


