import streamlit as st

# Verifica si debe redirigir a page2
if "redirigir_a_page2" in st.session_state and st.session_state.redirigir_a_page2:
    st.title("Página 2")
    st.write("¡Bienvenido a la página 2! Has confirmado tu selección.")
    # Puedes agregar más contenido para la página 2 aquí
else:
    st.warning("Por favor, confirma tu selección para continuar.")
