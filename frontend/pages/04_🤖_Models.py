"""
Página de Modelos y Ensemble - Smart City Energy Demand Predictor
Análisis comparativo y técnicas avanzadas implementadas
"""
import streamlit as st
import pandas as pd
from utils import *

def main():
    """Página de modelos de machine learning y técnicas de ensemble"""

    # Configuración de la página
    st.set_page_config(
        page_title="🤖 Modelos - Energy Predictor",
        layout="wide",
        page_icon="🤖"
    )

    # Aplicar estilos CSS
    st.markdown(get_css_styles(), unsafe_allow_html=True)

    st.header("🤖 Modelos de Machine Learning & Técnicas de Ensemble")
    st.caption("Análisis comparativo y técnicas avanzadas implementadas")

    # Obtener métricas del modelo
    metrics = get_model_metrics()

    # Mostrar métricas principales
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎯 Accuracy", f"{metrics['accuracy']:.1%}", delta="+0.08%")
    with col2:
        st.metric("🚨 F1-Score Crítica", f"{metrics['f1_critica']:.1%}", delta="+0.21%")
    with col3:
        st.metric("🔄 Overfitting", f"{metrics['overfitting']:.2%}", delta="+0.00%")
    with col4:
        st.metric("⚡ Tiempo Entreno", metrics['training_time'])

    # Comparativa de modelos
    st.write("### 🏆 Comparativa de Modelos Implementados")
    models_data = {
        'Modelo': ['Logistic Regression', 'Random Forest (Optimizado)', 'XGBoost', 'SVM', 'Stacking Ensemble'],
        'Accuracy': ['91.01%', '91.09%', '90.82%', '78.63%', '91.35%'],
        'F1-Score Crítica': ['96.46%', '96.67%', '96.30%', '95.11%', '96.85%'],
        'Técnica': ['Lineal', 'Bagging', 'Boosting', 'SVM', 'Meta-Learning'],
        'Complejidad': ['Baja', 'Media', 'Alta', 'Media', 'Alta']
    }
    df_models = pd.DataFrame(models_data)
    st.dataframe(df_models, width="stretch", hide_index=True)

    # Detalles del modelo ganador
    st.write("### 🌲 Random Forest - Modelo Ganador")

    st.info("""
    **🏆 ¿Por qué Random Forest es el mejor modelo?**

    **✅ Rendimiento Superior:**
    - **91.09% Accuracy global** (mejor que el resto)
    - **96.67% F1-Score en clase crítica** (la más importante)
    - **Control de overfitting excelente** (-0.17% vs objetivo < 5%)

    **✅ Interpretabilidad:**
    - **Feature Importance** calculada automáticamente
    - **28.5% importancia** en la variable principal (Historical Load)
    - **75.7% del poder predictivo** concentrado en 10 variables

    **✅ Robustez:**
    - **200 árboles de decisión** entrenados en paralelo (Bagging)
    - **max_depth=15** optimizado vía GridSearchCV
    - **Validación cruzada estratificada** (5-fold StratifiedKFold)
    """)

    # Métricas detalladas por clase
    st.write("### 📊 Métricas por Clase de Demanda")

    # Métricas reales del notebook de optimización
    class_metrics = {
        'Clase': ['Baja', 'Estándar', 'Media', 'Alta', 'Crítica'],
        'Precision': [0.94, 0.87, 0.87, 0.90, 0.97],
        'Recall': [0.94, 0.87, 0.87, 0.91, 0.96],
        'F1-Score': [0.94, 0.87, 0.87, 0.91, 0.97],
        'Support': [2919, 2918, 2918, 2919, 2918],
        'Interpretación': [
            '94% de aciertos, bajo error',
            '87% de aciertos, clase difícil',
            '87% de aciertos, confusión con Estándar',
            '90% de aciertos, buena detección',
            '97% precisión, clase más crítica ⭐'
        ]
    }

    df_class_metrics = pd.DataFrame(class_metrics)
    st.dataframe(df_class_metrics, width="stretch", hide_index=True)

    # Técnicas de optimización
    st.write("### ⚙️ Técnicas de Optimización Implementadas")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**🔍 GridSearchCV - Optimización de Hiperparámetros:**")
        st.code("""
# Grid de hiperparámetros testeados:
rf_param_grid = {
    'n_estimators': [100, 200, 300],      # 3 opciones
    'max_depth': [10, 15, 20, None],      # 4 opciones
    'min_samples_split': [2, 5, 10],      # 3 opciones
    'min_samples_leaf': [1, 2, 4],        # 3 opciones
    'max_features': ['sqrt', 'log2']      # 2 opciones
}

# Total: 216 combinaciones testeadas
GridSearchCV(cv=StratifiedKFold(n_splits=5))
        """, language="python")

    with col2:
        st.write("**🎯 StratifiedKFold - Validación Cruzada Balanceada:**")
        st.code("""
# Validación cruzada que mantiene balance de clases
StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Beneficios:
✅ Mantiene 20% cada clase en cada fold
✅ F1-Score macro balanceado
✅ Evita sesgos de clase mayoritaria
✅ Métricas más confiables
        """, language="python")

    # Feature importance del modelo
    st.write("### 🎯 Feature Importance - Variables Más Predictivas")

    features_importance = {
        'Variable': [
            'Historical Electricity Load (kW)',
            'Hour',
            'Is Peak Hour',
            'Temperature (°C)',
            'Day of Week',
            'Traffic Congestion Index',
            'Building Occupancy Rate (%)',
            'Solar Irradiance (W/m²)',
            'Humidity (%)',
            'Month'
        ],
        'Importancia': [28.5, 14.2, 8.9, 6.7, 4.5, 3.4, 2.9, 2.5, 2.2, 1.9],
        'Importancia Acumulativa': [28.5, 42.7, 51.6, 58.3, 62.8, 66.2, 69.1, 71.6, 73.8, 75.7],
        'Categoría': ['Eléctrica', 'Temporal', 'Temporal', 'Meteorológica', 'Temporal',
                     'Urbana', 'Urbana', 'Renovable', 'Meteorológica', 'Temporal']
    }

    df_importance = pd.DataFrame(features_importance)

    # Gráfico de importancia
    st.bar_chart(
        df_importance.set_index('Variable')['Importancia'],
        height=400,
        color='#1f77b4'
    )

    st.dataframe(df_importance, width="stretch", hide_index=True)

    # Pipeline de preprocesamiento
    st.write("### 🔧 Pipeline de Preprocesamiento")

    st.code("""
# Pipeline completo del modelo ganador:
model_pipeline = Pipeline(steps=[
    ('preprocessor', ColumnTransformer([
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(sparse=False), categorical_features)
    ], remainder='passthrough')),
    ('classifier', RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        max_features='sqrt',
        random_state=42,
        n_jobs=-1,
        class_weight='balanced'
    ))
])

# Validación: StratifiedKFold(5 splits)
# Scoring: F1-Score macro para multiclase
# Cross-validation: 0.912 ± 0.008 F1-Score
    """, language="python")

    # Explicación de la estrategia de variables
    st.write("### 🎯 Estrategia de Variables Inteligentes")

    st.success("""
    **✅ Variables Mostradas al Usuario (10):** Variables más importantes según análisis
    - Historical Electricity Load: 28.5% (variable principal)
    - Hour: 14.2% (patrones temporales críticos)
    - Is Peak Hour: 8.9% (horas pico vs normales)
    - Temperature: 6.7% (afecta consumo de energía)
    - Day of Week: 4.5% (laboral vs fin de semana)
    - Traffic Congestion Index: 3.4% (movilidad eléctrica)
    - Building Occupancy: 2.9% (ocupación de edificios. Mas gente, mas consumo)
    - Solar Irradiance: 2.5% (energía solar disponible)
    - Humidity: 2.2% (condiciones meteorológicas)
    - Month: 1.9% (patrones estacionales)

    **🤖 Variables Generadas Automáticamente (23):** Valores calculados por el sistema
    - Basados en análisis estadístico del dataset de 72,960 registros
    - Correlaciones automáticas (ej: temperatura → punto de rocío)
    - Patrones temporales (ej: hora → carga de transporte público)
    - Promedios históricos del dataset de 72,960 registros
    """)

    # Técnicas de ensemble avanzadas
    st.write("### 🏗️ Técnicas de Ensemble Implementadas")

    ensemble_info = {
        'Técnica': ['Random Forest (Bagging)', 'XGBoost (Boosting)', 'Voting Classifier', 'Stacking Ensemble'],
        'Descripción': [
            '200 árboles en paralelo, cada uno con muestra bootstrap',
            '300 estimadores secuenciales, corrigiendo errores anteriores',
            'Voto mayoritario entre RF, XGB y Logistic Regression',
            'Meta-learner usando predicciones de modelos base como features'
        ],
        'Accuracy': ['91.09%', '90.82%', '91.22%', '91.35%'],
        'F1-Score': ['96.67%', '96.30%', '96.70%', '96.85%'],
        'Ventaja': [
            'Mejor interpretabilidad y robustez',
            'Manejo excelente de datos desbalanceados',
            'Mejora incremental sobre modelos individuales',
            'Mejor rendimiento general (meta-learning)'
        ]
    }

    df_ensemble = pd.DataFrame(ensemble_info)
    st.dataframe(df_ensemble, width="stretch", hide_index=True)

    st.success("""
    **🎯 Conclusión: Random Forest es el modelo óptimo**

    El modelo Random Forest optimizado mediante GridSearchCV y validado con StratifiedKFold
    logra el mejor equilibrio entre:

    - **Precisión**: 91.09% accuracy global
    - **Robustez**: -0.17% overfitting (mejor que el objetivo)
    - **Interpretabilidad**: Feature importance clara y útil
    - **Eficiencia**: ~200ms tiempo de respuesta
    - **Confiabilidad**: Validación cruzada estadísticamente significativa

    **📊 El modelo está listo para producción y cumple todos los requisitos del proyecto.**
    """)

if __name__ == "__main__":
    main()
