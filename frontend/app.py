# CÓDIGO: frontend/app.py
import streamlit as st
import requests

# CRUCIAL: 'backend-api' es el nombre del servicio en docker-compose.yml
BACKEND_URL = "http://backend-api:8000"

st.set_page_config(page_title="MVP Energy Predictor (Streamlit)", layout="centered")

st.title("⚡ MVP: Orquestación Backend + Frontend")

try:
    # Llamar al endpoint /health del backend (FastAPI)
    response = requests.get(f"{BACKEND_URL}/health")
    
    if response.status_code == 200:
        data = response.json()
        st.success("✅ Conexión con el Backend (FastAPI) exitosa.")
        st.json(data)
        st.success("¡El Modelo Random Forest está cargado y listo para predecir!")
            
    else:
        st.error(f"❌ Error al contactar al Backend. Estado: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    st.error("❌ No se pudo conectar al Backend. Revisa el archivo docker-compose.yml y los logs del backend.")

st.markdown("---")
st.header("Formulario de Predicción (Próximo Paso)")