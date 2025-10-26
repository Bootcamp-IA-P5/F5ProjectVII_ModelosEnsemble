
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import os
import sys
from typing import List # Necesaria para la nueva importación de Pydantic
import logging

# Importamos los Schemas del nuevo archivo
from .schemas import EnergyFeatures, PredictionBatchInput, PredictionOutput

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- 1. Configuración de Rutas y Carga del Modelo ---
# La ruta retrocede de 'backend/api/' a la raíz
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'resources', 'models', 'model_RandomForest_FINAL.pkl')
try:
    # Carga del pipeline completo (preprocesador + clasificador RF)
    model_pipeline = joblib.load(MODEL_PATH)
    logger.info("✅ Modelo Random Forest cargado exitosamente.")
except FileNotFoundError:
    logger.error(f"❌ ERROR: No se encontró el modelo en la ruta: {MODEL_PATH}")
    sys.exit(1)

# --- 2. Definición de la API ---
app = FastAPI(
    title="API de Predicción de Demanda Crítica de Energía",
    version="1.0.0"
)

# --- 3. Función de Mapeo de Columnas (¡CRUCIAL!) ---

def map_features(data: dict) -> pd.DataFrame:
    """Mapea los nombres de las features de la API (snake_case) a los nombres 
    de columnas del DataFrame usado en el entrenamiento (con espacios y símbolos).
    
    NOTA: Esta función está diseñada para recibir UN SOLO registro (diccionario)."""
    
    df = pd.DataFrame([data])
    
    # Mapeo completo (snake_case -> nombre del DataFrame original)
    column_mapping = {
        'historical_electricity_load_kw': 'Historical Electricity Load (kW)',
        'voltage_level_v': 'Voltage Level (V)',
        'current_level_a': 'Current Level (A)',
        'power_factor': 'Power Factor',
        'solar_pv_output_kw': 'Solar PV Output (kW)',
        'wind_power_output_kw': 'Wind Power Output (kW)',
        'solar_panel_temperature_c': 'Solar Panel Temperature (°C)',
        'wind_speed_m_s': 'Wind Speed (m/s)',
        'temperature_c': 'Temperature (°C)',
        'humidity_pct': 'Humidity (%)',
        'solar_irradiance_w_m2': 'Solar Irradiance (W/m²)',
        'cloud_cover_pct': 'Cloud Cover (%)',
        'rainfall_mm': 'Rainfall (mm)',
        'atmospheric_pressure_hpa': 'Atmospheric Pressure (hPa)',
        'dew_point_c': 'Dew Point (°C)',
        'building_occupancy_rate_pct': 'Building Occupancy Rate (%)',
        'public_transit_operational_load_kw': 'Public Transit Operational Load (kW)',
        'ev_charging_station_load_kw': 'EV Charging Station Load (kW)',
        'traffic_congestion_index': 'Traffic Congestion Index',
        'human_mobility_score': 'Human Mobility Score',
        'time_since_last_peak_hours': 'Time Since Last Peak (hours)',
        'time_until_next_predicted_peak_hours': 'Time Until Next Predicted Peak (hours)',
        'distance_to_nearest_substation_km': 'Distance to Nearest Substation (km)',
        'hour': 'Hour',
        'day_of_week': 'DayOfWeek',
        'month': 'Month',
        'year': 'Year',
        'is_weekend': 'Is_Weekend',
        'is_peak_hour': 'Is_Peak_Hour',
        'is_holiday': 'Is Holiday', 
        'season': 'Season',
        'weather_condition': 'Weather Condition', 
        'area_type': 'Area Type' 
    }
    
    # Renombrar columnas
    df.rename(columns=column_mapping, inplace=True)
    
    # Reordenar las columnas del DF para coincidir exactamente con el orden de X_train
    # Este es el orden EXACTO que espera el modelo (obtenido del modelo entrenado)
    ordered_columns = [
        'Historical Electricity Load (kW)', 'Voltage Level (V)', 'Current Level (A)',
        'Power Factor', 'Solar PV Output (kW)', 'Wind Power Output (kW)',
        'Solar Panel Temperature (°C)', 'Wind Speed (m/s)', 'Temperature (°C)',
        'Humidity (%)', 'Solar Irradiance (W/m²)', 'Cloud Cover (%)',
        'Rainfall (mm)', 'Atmospheric Pressure (hPa)', 'Dew Point (°C)',
        'Building Occupancy Rate (%)', 'Public Transit Operational Load (kW)',
        'EV Charging Station Load (kW)', 'Traffic Congestion Index',
        'Human Mobility Score', 'Time Since Last Peak (hours)',
        'Time Until Next Predicted Peak (hours)', 'Distance to Nearest Substation (km)',
        'Hour', 'DayOfWeek', 'Month', 'Year', 'Is_Weekend', 'Is_Peak_Hour',
        'Is Holiday', 'Season', 'Weather Condition', 'Area Type'
    ]
    
    # Verificación de que el input tiene las columnas correctas
    if set(df.columns) != set(ordered_columns):
        # Usamos HTTPException de FastAPI
        missing_cols = set(ordered_columns) - set(df.columns)
        raise HTTPException(status_code=400, detail=f"Las features mapeadas no coinciden con las 33 features requeridas por el modelo. Faltan: {missing_cols}")
   
    return df[ordered_columns]

# --- 4. Endpoint de Predicción ---
@app.post("/predict_demand", response_model=List[PredictionOutput]) 
def predict(features_batch: PredictionBatchInput):
    """
    Realiza una predicción de la categoría de demanda eléctrica (0: Baja a 4: Crítica).
    Requiere que se envíen TODAS las 33 features.
    """
    # 1. Convertir los modelos Pydantic del lote a una lista de diccionarios
    # Pydantic V2: features_batch.root es la lista de modelos `EnergyFeatures`.
    # Usamos .model_dump() para convertir cada modelo a un diccionario estándar de Python.
    list_of_dicts = [item.model_dump() for item in features_batch.root] 
    
    if not list_of_dicts:
        raise HTTPException(status_code=400, detail="La lista de datos de entrada está vacía.")
        
    
    # PROCESAMIENTO ACTUAL: Solo tomamos el primer elemento (índice 0) 
    # ya que el frontend de Streamlit solo envía un registro.
    try:
        input_dict = list_of_dicts[0]
        # map_features mapea las claves y crea el DataFrame para la predicción.
        input_df = map_features(input_dict) 
    except HTTPException:
        # Re-lanzar la excepción si el mapeo falló
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno durante el mapeo de features: {str(e)}")


    # 2. Realizar la predicción
    # Como solo envías 1 registro, predict() devuelve un array con 1 elemento: [clase]
    prediction = model_pipeline.predict(input_df)[0]

    # Logging para debugging
    logger.info(f"🔍 Datos de entrada después del mapeo: {input_df.shape}")
    logger.info(f"🎯 Predicción del modelo: {prediction}")
    logger.info(f"📊 Input values: {input_df.iloc[0].to_dict()}")

    # 5. Mapeo de la etiqueta de salida (para mejor UX)
    category_map = {
        0: "0: Baja", 1: "1: Estándar", 2: "2: Media",
        3: "3: Alta", 4: "4: Crítica"
    }
    
    # 3. Crear el objeto de respuesta, asegurándonos de que cumpla con el PredictionOutput schema
    response_item = PredictionOutput(
        prediction_category=category_map.get(int(prediction), "Desconocida"),
        # Dejamos prediction_score como None ya que el modelo RF no produce puntuaciones directas.
        prediction_score=None 
    )
    
    # Devolvemos la lista de una sola predicción, como requiere el tipo de respuesta (Batch)
    return [response_item]

# --- 5. Health Check Endpoint ---
@app.get("/health")
def health_check():
    """Verifica que el servicio y el modelo estén cargados."""
    logger.info("🔍 Health check solicitado")
    return {"status": "ok", "model_loaded": True}