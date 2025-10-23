# CÓDIGO: backend/api/main.py (VERSION ESTRICTA)

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field
import os
import sys

# --- 1. Configuración de Rutas y Carga del Modelo ---

# La ruta retrocede de 'backend/api/' a la raíz
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'resources', 'models', 'model_RandomForest_FINAL.pkl')
try:
    # Carga del pipeline completo (preprocesador + clasificador RF)
    model_pipeline = joblib.load(MODEL_PATH)
    print("✅ Modelo Random Forest cargado exitosamente.")
except FileNotFoundError:
    print(f"❌ ERROR: No se encontró el modelo en la ruta: {MODEL_PATH}")
    sys.exit(1)

# --- 2. Definición de la API ---

app = FastAPI(
    title="API de Predicción de Demanda Crítica de Energía",
    version="1.0.0"
)

# --- 3. Definición del Esquema de Entrada (Pydantic) ---

# CRUCIAL: NO se usan valores por defecto para forzar al cliente a enviar TODAS las features.
# Los nombres son los 'snake_case' que el cliente debe usar en el JSON de entrada.

class EnergyFeatures(BaseModel):
    # 23 Features Numéricas (Todas deben ser float)
    historical_electricity_load_kw: float
    voltage_level_v: float
    current_level_a: float
    power_factor: float
    solar_pv_output_kw: float
    wind_power_output_kw: float
    solar_panel_temperature_c: float
    wind_speed_m_s: float
    temperature_c: float
    humidity_pct: float
    solar_irradiance_w_m2: float
    cloud_cover_pct: float
    rainfall_mm: float
    atmospheric_pressure_hpa: float
    dew_point_c: float
    building_occupancy_rate_pct: float
    public_transit_operational_load_kw: float
    ev_charging_station_load_kw: float
    traffic_congestion_index: float
    human_mobility_score: float
    time_since_last_peak_hours: float
    time_until_next_predicted_peak_hours: float
    distance_to_nearest_substation_km: float

    # 10 Features Categóricas/Temporales (Mixtas)
    hour: int
    day_of_week: int
    month: int
    year: int
    is_weekend: int # Binaria (0 o 1)
    is_peak_hour: int # Binaria (0 o 1)
    is_holiday: str
    season: str
    weather_condition: str
    area_type: str


# --- 4. Función de Mapeo de Columnas (¡CRUCIAL!) ---

def map_features(data: dict) -> pd.DataFrame:
    """Mapea los nombres de las features de la API (snake_case) a los nombres 
    de columnas del DataFrame usado en el entrenamiento (con espacios y símbolos)."""
    
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
        'is_holiday': 'Is Holiday', # ¡Cuidado con el espacio!
        'season': 'Season',
        'weather_condition': 'Weather Condition', # ¡Cuidado con el espacio!
        'area_type': 'Area Type' # ¡Cuidado con el espacio!
    }
    
    # Renombrar columnas
    df.rename(columns=column_mapping, inplace=True)
    
    # Reordenar las columnas del DF para coincidir exactamente con el orden de X_train (aunque a veces no es estrictamente necesario, es la práctica más segura)
    # Lista de orden de columnas del entrenamiento (FEATURES_NUMERICAS + FEATURES_CATEGORICAS)
    ordered_columns = list(column_mapping.values())
    
    # Verificación de que el input tiene las columnas correctas
    if set(df.columns) != set(ordered_columns):
        # En una API real se lanzaría un error HTTP 400
        raise ValueError(f"Las features mapeadas no coinciden con las 33 features requeridas por el modelo. Faltan: {set(ordered_columns) - set(df.columns)}")
        
    return df[ordered_columns]


# --- 5. Endpoint de Predicción ---

@app.post("/predict_demand")
def predict(features: EnergyFeatures):
    """
    Realiza una predicción de la categoría de demanda eléctrica (0: Baja a 4: Crítica).
    Requiere que se envíen TODAS las 33 features.
    """
    # 1. Convertir la entrada Pydantic a un DataFrame de Pandas y mapear columnas
    try:
        input_df = map_features(features.model_dump())
    except ValueError as e:
        return {"error": str(e)}, 400 # Error si falta alguna columna clave
    
    # 2. Realizar la predicción
    prediction = model_pipeline.predict(input_df)[0]
    
    # 3. Mapeo de la etiqueta de salida (para mejor UX)
    category_map = {
        0: "0: Baja", 1: "1: Estándar", 2: "2: Media", 
        3: "3: Alta", 4: "4: Crítica"
    }
    
    return {
        "prediction_code": int(prediction),
        "prediction_category": category_map.get(prediction, "Desconocida"),
        "model_used": "RandomForest_FINAL"
    }

# --- 6. Health Check Endpoint ---

@app.get("/health")
def health_check():
    """Verifica que el servicio y el modelo estén cargados."""
    return {"status": "ok", "model_loaded": True}