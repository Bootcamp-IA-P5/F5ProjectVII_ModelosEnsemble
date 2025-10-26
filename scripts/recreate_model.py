#!/usr/bin/env python3
"""
Script para recrear el modelo Random Forest compatible con sklearn 1.7.2
Usa exactamente la misma configuración del notebook original
"""

import pandas as pd
import numpy as np
import os
import joblib
import kagglehub
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

print("🔄 Recreando modelo Random Forest compatible con sklearn 1.7.2...")
print()

# === 1. DESCARGAR DATASET ===
print("📥 Descargando dataset...")
try:
    base_path = kagglehub.dataset_download("datasetengineer/isone-smart-city-energy-dataset")
    csv_file_name = 'smart_city_energy_dataset.csv'
    file_path = os.path.join(base_path, csv_file_name)
    df = pd.read_csv(file_path)
    print(f"✅ Dataset cargado: {df.shape[0]} filas, {df.shape[1]} columnas")
except Exception as e:
    print(f"❌ Error descargando dataset: {e}")
    exit(1)

# === 2. PREPROCESAMIENTO EXACTO DEL NOTEBOOK ===
print("\n🔧 Aplicando preprocesamiento...")

# 2.1: Renombrar columna Timestamp -> Time
if 'Timestamp' in df.columns:
    df.rename(columns={'Timestamp': 'Time'}, inplace=True)

# 2.2: Convertir Time a datetime y extraer features temporales
df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
df.dropna(subset=['Time'], inplace=True)

df['Year'] = df['Time'].dt.year
df['Month'] = df['Time'].dt.month
df['Day'] = df['Time'].dt.day
df['DayOfWeek'] = df['Time'].dt.dayofweek  # Lunes=0, Domingo=6
df['Hour'] = df['Time'].dt.hour

# Features binarias
df['Is_Weekend'] = df['DayOfWeek'].apply(lambda x: 1 if x >= 5 else 0)
df['Is_Peak_Hour'] = df['Hour'].apply(lambda x: 1 if (7 <= x <= 10) or (17 <= x <= 20) else 0)

# 2.3: Crear variable target multiclase
TARGET = 'Demand_Category'
df[TARGET] = pd.qcut(df['Electricity Load'], q=5, labels=False, duplicates='drop').astype('Int64')

# 2.4: Seleccionar features exactas del notebook
FEATURES_NUMERICAS = [
    'Historical Electricity Load (kW)', 'Voltage Level (V)', 'Current Level (A)',
    'Power Factor', 'Solar PV Output (kW)', 'Wind Power Output (kW)',
    'Solar Panel Temperature (°C)', 'Wind Speed (m/s)', 'Temperature (°C)',
    'Humidity (%)', 'Solar Irradiance (W/m²)', 'Cloud Cover (%)',
    'Rainfall (mm)', 'Atmospheric Pressure (hPa)', 'Dew Point (°C)',
    'Building Occupancy Rate (%)', 'Public Transit Operational Load (kW)',
    'EV Charging Station Load (kW)', 'Traffic Congestion Index',
    'Human Mobility Score', 'Time Since Last Peak (hours)',
    'Time Until Next Predicted Peak (hours)', 'Distance to Nearest Substation (km)'
]

FEATURES_CATEGORICAS_OHE = [
    'Hour', 'DayOfWeek', 'Month', 'Year',
    'Is Holiday', 'Season', 'Weather Condition', 'Area Type'
]

FEATURES_BINARIAS = ['Is_Weekend', 'Is_Peak_Hour']

# Filtrar dataset
df_ml = df[FEATURES_NUMERICAS + FEATURES_CATEGORICAS_OHE + FEATURES_BINARIAS + [TARGET]].copy()

# Manejar nulos
for col in FEATURES_NUMERICAS:
    if df_ml[col].isnull().any():
        df_ml[col].fillna(df_ml[col].mean(), inplace=True)

for col in FEATURES_CATEGORICAS_OHE + FEATURES_BINARIAS:
    if df_ml[col].isnull().any():
        df_ml[col].fillna('missing', inplace=True)

print(f"✅ Datos procesados: {df_ml.shape[0]} filas, {df_ml.shape[1]} columnas")

# === 3. SPLIT DE DATOS ===
print("\n✂️  Dividiendo datos (Train/Test)...")
X = df_ml.drop(columns=[TARGET])
y = df_ml[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"✅ Train: {X_train.shape}, Test: {X_test.shape}")

# === 4. CREAR PIPELINE DE PREPROCESAMIENTO ===
print("\n🔨 Creando pipeline de preprocesamiento...")

# Preprocesadores
numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

# ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, FEATURES_NUMERICAS),
        ('cat', categorical_transformer, FEATURES_CATEGORICAS_OHE),
    ],
    remainder='passthrough'  # Para las binarias
)

# === 5. CREAR Y ENTRENAR MODELO ===
print("\n🤖 Entrenando Random Forest...")
model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        random_state=42,
        n_jobs=-1,
        class_weight='balanced'
    ))
])

model_pipeline.fit(X_train, y_train)
print("✅ Modelo entrenado exitosamente")

# === 6. EVALUAR MODELO ===
print("\n📊 Evaluando modelo...")
train_score = model_pipeline.score(X_train, y_train)
test_score = model_pipeline.score(X_test, y_test)

print(f"Accuracy Train: {train_score:.4f}")
print(f"Accuracy Test:  {test_score:.4f}")
print(f"Overfitting: {(train_score - test_score)*100:.2f}%")

# === 7. GUARDAR MODELO COMPATIBLE ===
print("\n💾 Guardando modelo compatible...")
MODEL_DIR = 'resources/models'
MODEL_FILENAME = 'model_RandomForest_FINAL_v2.pkl'

if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

model_path = os.path.join(MODEL_DIR, MODEL_FILENAME)
joblib.dump(model_pipeline, model_path)

print(f"✅ Modelo guardado en: {model_path}")
print(f"📦 Tamaño del archivo: {os.path.getsize(model_path) / (1024*1024):.1f} MB")

# === 8. VERIFICAR QUE FUNCIONA ===
print("\n🧪 Verificando que el modelo funciona...")
test_prediction = model_pipeline.predict(X_test[:1])
print(f"✅ Predicción de prueba: {test_prediction[0]}")

print("\n🎉 ¡MODELO RECREADO EXITOSAMENTE!")
print("Ahora es compatible con sklearn 1.7.2 y debería funcionar correctamente.")
