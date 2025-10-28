"""
Página de Predicción - Smart City Energy Demand Predictor
"""
import streamlit as st
import requests
import pandas as pd
from utils import *

def show_prediction_page():
    """Página de predicción de demanda energética"""

    st.header("🔮 Predicción de Demanda Energética")
    st.caption("Clasificación multiclase con 5 niveles (Baja a Crítica)")

    # Explicación del enfoque inteligente
    st.info("""
    **🎯 Enfoque Inteligente:** Solo necesitas ingresar las **10 variables más importantes**
    (75.7% de poder predictivo). El resto se calcula automáticamente con valores realistas
    basados en análisis del dataset.

    **🚀 Escenarios de Demostración:** Cada botón representa un rango específico de demanda
    para que puedas probar todas las categorías del modelo (Baja → Crítica).
    """)

    # Botones de escenarios predefinidos
    st.write("**🚀 Escenarios de Demostración (5 rangos completos):**")
    scenario_cols = st.columns(5)

    scenarios = [
        "🏠 Baja Demanda",      # Categoría 0: 0-229 kW
        "💼 Estándar",          # Categoría 1: 229-343 kW
        "🏢 Media Demanda",     # Categoría 2: 343-467 kW
        "⚡ Alta Demanda",      # Categoría 3: 467-645 kW
        "🚨 Crítica"            # Categoría 4: 645+ kW
    ]

    # Explicación de los escenarios
    with st.expander("📋 ¿Qué hace cada escenario?", expanded=False):
        st.write("""
        **🎯 Escenarios diseñados para demostrar cada categoría de predicción:**

        - **🏠 Baja Demanda:** 3 AM, invierno, mínima actividad (80 kW - claramente BAJA)
        - **💼 Estándar:** 2 PM, día normal, actividad regular (280 kW - claramente ESTÁNDAR)
        - **🏢 Media Demanda:** 11 AM, viernes, hora pico ligera (400 kW - claramente MEDIA)
        - **⚡ Alta Demanda:** 9 AM, lunes, hora pico alta (520 kW - claramente ALTA)
        - **🚨 Crítica:** 8 AM, verano extremo, máxima actividad (900 kW - claramente CRÍTICA)

        *Cada escenario está calibrado para producir su categoría específica de predicción.*
        """)

    # Inicializar session_state para el escenario seleccionado
    if 'selected_scenario' not in st.session_state:
        st.session_state.selected_scenario = None

    # Botones de escenarios (solo el set que funciona)
    for i, scenario in enumerate(scenarios):
        if scenario_cols[i].button(f"📋 {scenario}", width="stretch", key=f"scenario_{i}"):
            st.session_state.selected_scenario = scenario
            logger.info(f"🎯 Usuario seleccionó escenario: {scenario}")
            logger.info(f"📊 Datos del escenario: {create_scenario_data(scenario)}")
            st.rerun()

    # Usar el escenario de session_state
    current_scenario = st.session_state.selected_scenario

    # Variables críticas
    st.write("**📝 Variables Principales (Top 10 por importancia):**")

    critical_features = [
        "Historical Electricity Load (kW)",  # 28.5% importancia
        "Hour",                               # 14.2% importancia
        "Is Peak Hour",                       # 8.9% importancia
        "Temperature (°C)",                   # 6.7% importancia
        "Day of Week",                        # 4.5% importancia
        "Traffic Congestion Index",           # 3.4% importancia
        "Building Occupancy Rate (%)",        # 2.9% importancia
        "Solar Irradiance (W/m²)",           # 2.5% importancia
        "Humidity (%)",                       # 2.2% importancia
        "Month"                               # 1.9% importancia
    ]

    # Formulario para que el usuario ingrese las 10 variables
    with st.form("prediction_form"):
        form_data = {}

        # Crear inputs para cada una de las 10 variables principales
        for feature_name in critical_features:
            if feature_name in FEATURES_MAPEO:
                key_snake = FEATURES_MAPEO[feature_name]
                col1, col2 = st.columns([2, 1])

                with col1:
                    # Crear el input apropiado según el tipo de variable
                    if key_snake in ["hour", "day_of_week", "month", "year"]:
                        max_val = 23 if key_snake == "hour" else 12 if key_snake in ["month"] else 7 if key_snake == "day_of_week" else 2025
                        min_val = 0 if key_snake == "hour" else 1 if key_snake in ["day_of_week", "month"] else 2020

                        default_value = create_scenario_data(current_scenario).get(key_snake, min_val)
                        form_data[key_snake] = st.number_input(
                            feature_name, min_value=min_val, max_value=max_val, step=1,
                            value=default_value
                        )
                    elif feature_name in MAPEO_CATEGORICAS:
                        default_value = create_scenario_data(current_scenario).get(key_snake, MAPEO_CATEGORICAS[feature_name][0])
                        if key_snake in create_scenario_data(current_scenario):
                            default_index = MAPEO_CATEGORICAS[feature_name].index(default_value)
                        else:
                            default_index = 0

                        form_data[key_snake] = st.selectbox(
                            feature_name, MAPEO_CATEGORICAS[feature_name],
                            index=default_index
                        )
                    else:
                        default_value = float(create_scenario_data(current_scenario).get(key_snake, 0.0))
                        form_data[key_snake] = st.number_input(
                            feature_name,
                            value=default_value,
                            step=0.01
                        )

        # Botón para hacer la predicción
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            predict_button = st.form_submit_button("🔮 Predecir Demanda", width="stretch", type="primary")

        if predict_button:
            logger.info("🖱️ Usuario hizo clic en 'Predecir Demanda'")
            logger.info(f"📋 Datos del formulario: {form_data}")

            # Validar datos
            validated_data = {}
            for key, value in form_data.items():
                if isinstance(value, (int, float)) and value == 0.0:
                    if key == "historical_electricity_load_kw":
                        validated_data[key] = 100.0
                        logger.warning(f"⚠️  {key} estaba en 0.0, usando valor por defecto: 100.0")
                    elif key in ["temperature_c", "humidity_pct", "solar_irradiance_w_m2", "building_occupancy_rate_pct", "traffic_congestion_index"]:
                        validated_data[key] = 20.0 if key == "temperature_c" else 50.0
                        logger.warning(f"⚠️  {key} estaba en 0.0, usando valor por defecto: {validated_data[key]}")
                    else:
                        validated_data[key] = value
                else:
                    validated_data[key] = value

            default_values = generate_default_values(validated_data)
            complete_data = {**validated_data, **default_values}

            logger.info(f"✅ Datos validados: {validated_data}")
            logger.info(f"🔧 Variables por defecto generadas: {len(default_values)}")
            logger.info(f"📊 Total de variables para predicción: {len(complete_data)}")

            # Mostrar variables generadas automáticamente
            with st.expander("🔧 Variables Generadas Automáticamente (23 variables)", expanded=False):
                st.write(f"**✅ {len(default_values)} variables calculadas automáticamente:**")
                for key, value in default_values.items():
                    feature_name = [k for k, v in FEATURES_MAPEO.items() if v == key][0]
                    st.write(f"• **{feature_name}**: {value}")

            # Hacer la predicción
            logger.info("🚀 Enviando datos al backend para predicción...")
            make_prediction(complete_data)

def make_prediction(form_data: dict):
    """
    Realiza la predicción usando la API del backend
    """
    try:
        logger.info("🔄 Iniciando predicción...")
        logger.info(f"🔗 URL del backend: {BACKEND_URL}/predict_demand")
        logger.info(f"📊 Número de variables: {len(form_data)}")

        payload = [form_data]

        with st.spinner("🔄 Procesando predicción con IA..."):
            response = requests.post(
                f"{BACKEND_URL}/predict_demand",
                json=payload,
                timeout=30
            )

        if response.status_code == 200:
            result = response.json()

            if result and isinstance(result, list) and result[0]:
                predicted_category = result[0].get('prediction_category', "Desconocida")

                # Mostrar resultado con colores según gravedad
                if 'Crítica' in predicted_category:
                    st.error(f"⚠️ **¡ALERTA!** Demanda **{predicted_category}** - Riesgo Crítico")
                    st.warning("🚨 **Recomendación**: Activar protocolos de emergencia de red")
                elif 'Alta' in predicted_category:
                    st.warning(f"📈 **ATENCIÓN** Demanda **{predicted_category}** - Alto Consumo")
                    st.info("⚡ **Recomendación**: Monitorear carga de la red y preparar reservas")
                else:
                    st.success(f"✅ **NORMAL** Demanda **{predicted_category}** - Consumo Estable")
                    st.info("💡 **Recomendación**: Continuar operaciones normales")

                # Detalles técnicos
                with st.expander("🔍 Detalles Técnicos de la Predicción", expanded=False):
                    st.json({
                        "input_features": len(form_data),
                        "model_used": "Random Forest Ensemble",
                        "prediction_confidence": "96.67% (F1-Score)",
                        "response_time": "~200ms",
                        "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                    })

            else:
                st.error("❌ La respuesta de la API no contiene una predicción válida.")

        else:
            st.error(f"❌ Error en la API. Código de estado: {response.status_code}")

    except requests.exceptions.ConnectionError:
        st.error("❌ No se pudo conectar a la API del Backend (FastAPI).")
        st.info("💡 **Solución**: Asegúrate de que Docker esté ejecutándose: `docker compose up`")
    except Exception as e:
        st.error(f"❌ Error inesperado: {str(e)}")
