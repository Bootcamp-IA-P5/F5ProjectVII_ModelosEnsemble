from typing import List, Literal, Optional
from pydantic import BaseModel, Field, RootModel # Importamos RootModel para Pydantic V2

# 1. Modelo para un solo conjunto de features
# Usamos Optional para los campos que puedan tener valores nulos o 0.0 al inicio
class EnergyFeatures(BaseModel):
    # Numéricas (23)
    historical_electricity_load_kw: float = Field(..., description="Carga histórica de electricidad en kW")
    voltage_level_v: float = Field(..., description="Nivel de voltaje en V")
    current_level_a: float = Field(..., description="Nivel de corriente en A")
    power_factor: float = Field(..., description="Factor de potencia (0.0 a 1.0)")
    solar_pv_output_kw: float = Field(..., description="Producción de energía solar fotovoltaica en kW")
    wind_power_output_kw: float = Field(..., description="Producción de energía eólica en kW")
    solar_panel_temperature_c: float = Field(..., description="Temperatura del panel solar en °C")
    wind_speed_m_s: float = Field(..., description="Velocidad del viento en m/s")
    temperature_c: float = Field(..., description="Temperatura ambiente en °C")
    humidity_pct: float = Field(..., description="Humedad relativa en %")
    solar_irradiance_w_m2: float = Field(..., description="Irradiancia solar en W/m²")
    cloud_cover_pct: float = Field(..., description="Cobertura de nubes en %")
    rainfall_mm: float = Field(..., description="Precipitación en mm")
    atmospheric_pressure_hpa: float = Field(..., description="Presión atmosférica en hPa")
    dew_point_c: float = Field(..., description="Punto de rocío en °C")
    building_occupancy_rate_pct: float = Field(..., description="Tasa de ocupación del edificio en %")
    public_transit_operational_load_kw: float = Field(..., description="Carga operativa del transporte público en kW")
    ev_charging_station_load_kw: float = Field(..., description="Carga de la estación de vehículos eléctricos en kW")
    traffic_congestion_index: float = Field(..., description="Índice de congestión del tráfico")
    human_mobility_score: float = Field(..., description="Puntuación de movilidad humana")
    time_since_last_peak_hours: float = Field(..., description="Tiempo desde el último pico (horas)")
    time_until_next_predicted_peak_hours: float = Field(..., description="Tiempo hasta el próximo pico predicho (horas)")
    distance_to_nearest_substation_km: float = Field(..., description="Distancia a la subestación más cercana (km)")
    
    # Categóricas/Temporales (10) - Usamos int para numérico/binario, y Literal para strings fijos
    hour: int = Field(..., ge=0, le=23, description="Hora del día (0-23)")
    day_of_week: int = Field(..., ge=1, le=7, description="Día de la semana (1=Lunes, 7=Domingo)")
    month: int = Field(..., ge=1, le=12, description="Mes del año (1-12)")
    year: int = Field(..., ge=2020, description="Año (e.g., 2024)")
    is_weekend: Literal[0, 1] = Field(..., description="Es fin de semana (0=No, 1=Sí)")
    is_peak_hour: Literal[0, 1] = Field(..., description="Es hora pico (0=No, 1=Sí)")
    is_holiday: Literal["No", "Yes"] = Field(..., description="Es festivo ('No' o 'Yes')")
    season: Literal["Spring", "Summer", "Autumn", "Winter"] = Field(..., description="Estación del año")
    weather_condition: Literal["Clear", "Cloudy", "Rainy", "Snowy"] = Field(..., description="Condición meteorológica")
    area_type: Literal["Industrial", "Residential", "Commercial"] = Field(..., description="Tipo de área")


# 2. Modelo de entrada para el endpoint por lotes (el que usamos)
# SOLUCIÓN PYDANTIC V2: Usa RootModel en lugar de __root__
class PredictionBatchInput(RootModel[List[EnergyFeatures]]):
    """Representa una lista o lote de registros de features para predicción."""
    # En Pydantic V2, la lista se define directamente al heredar de RootModel
    pass


# 3. Modelo de respuesta del endpoint
class PredictionOutput(BaseModel):
    prediction_category: str = Field(..., description="La categoría de demanda energética predicha.")
    prediction_score: Optional[float] = Field(None, description="Puntuación de confianza de la predicción (opcional).")
