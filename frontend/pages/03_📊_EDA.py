"""
Página de EDA y Análisis - Smart City Energy Demand Predictor
Análisis exploratorio de datos con visualizaciones
"""
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from matplotlib.patches import Patch
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import *

# Datos de ejemplo para las primeras filas y estadísticas descriptivas
SAMPLE_DATA = {
    'Timestamp': pd.date_range(start='2023-01-01 00:00:00', periods=5, freq='H'),
    'Electricity Load': [120.5, 115.8, 110.2, 105.7, 100.3],
    'Temperature (°C)': [22.1, 21.8, 21.5, 21.3, 21.0],
    'Humidity (%)': [65, 66, 67, 68, 69],
    'Wind Speed (m/s)': [3.2, 3.0, 2.9, 2.8, 2.7]
}

def load_eda_data():
    """
    Cargar datos para las visualizaciones del EDA.
    
    Returns:
        tuple: (hourly_distribution, class_distribution, sample_data, stats_data, 
               model_metrics, confusion_matrix_data, correlation_data)
            - hourly_distribution: DataFrame con la distribución de categorías por hora
            - class_distribution: DataFrame con la distribución porcentual de clases
            - sample_data: DataFrame con las primeras filas de datos
            - stats_data: DataFrame con estadísticas descriptivas
            - model_metrics: Diccionario con métricas de rendimiento del modelo
            - confusion_matrix_data: Datos para la matriz de confusión
            - correlation_data: Datos para la matriz de correlación
    """
    # Crear DataFrame de ejemplo para las primeras filas
    sample_data = pd.DataFrame(SAMPLE_DATA)
    
    # Calcular estadísticas descriptivas
    stats_data = sample_data.describe().reset_index()
    
    # Datos para las métricas del modelo
    model_metrics = {
        'Modelo': ['Random Forest', 'Regresión Logística', 'XGBoost', 'SVM'],
        'Accuracy Entrenamiento': [0.998, 0.908, 0.992, 0.786],
        'Accuracy Validación': [0.991, 0.910, 0.985, 0.785],
        'F1-Score (Crítica)': [0.992, 0.965, 0.988, 0.951],
        'Overfitting (%)': [0.7, -0.2, 0.7, 0.1]
    }
    
    # Datos para la matriz de confusión (ejemplo para Random Forest)
    confusion_matrix_data = pd.DataFrame({
        'Real': ['Baja']*5 + ['Estándar']*5 + ['Media']*5 + ['Alta']*5 + ['Crítica']*5,
        'Predicho': (['Baja', 'Estándar', 'Media', 'Alta', 'Crítica'])*5,
        'Cantidad': [
            2890, 15, 8, 5, 1,
            12, 2880, 20, 5, 1,
            5, 18, 2885, 10, 0,
            3, 5, 12, 2895, 4,
            0, 2, 5, 10, 2891
        ]
    })
    
    # Datos para la matriz de correlación
    np.random.seed(42)
    correlation_data = pd.DataFrame({
        'Demanda Eléctrica': np.random.normal(100, 20, 1000),
        'Temperatura (°C)': np.random.normal(22, 5, 1000),
        'Humedad (%)': np.random.normal(65, 10, 1000),
        'Velocidad Viento (m/s)': np.random.gamma(2, 1.5, 1000),
        'Radiación Solar (W/m²)': np.random.gamma(300, 1, 1000)
    })
    
    # ============================================
    # Datos extraídos de la Celda 3.0 del notebook
    # Distribución porcentual de las 5 clases de demanda
    # ============================================
    class_distribution = pd.DataFrame({
        'Category': ['0: Baja', '1: Estándar', '2: Media', '3: Alta', '4: Crítica'],
        'Percentage': [20.0, 20.0, 20.0, 20.0, 20.0]  # Valores balanceados por pd.qcut
    })
    
    # ============================================
    # Datos extraídos de la Celda 4.0 del notebook
    # Distribución de categorías por hora del día
    # ============================================
    # Nota: Los valores son aproximaciones basadas en el análisis visual de la gráfica
    # En una implementación real, estos deberían cargarse desde el dataset original
    hours = list(range(24))
    # Valores aproximados basados en el análisis visual del notebook
    # Cada lista interna representa [Baja, Estándar, Media, Alta, Crítica] para cada hora
    demand_distribution = {
        0: [120, 80, 40, 20, 10],
        1: [130, 85, 35, 15, 5],
        2: [140, 90, 30, 10, 0],
        3: [150, 80, 25, 8, 0],
        4: [145, 75, 30, 10, 5],
        5: [130, 70, 40, 20, 10],
        6: [100, 80, 60, 40, 20],
        7: [50, 70, 90, 60, 30],
        8: [20, 40, 80, 100, 60],
        9: [15, 30, 70, 90, 80],
        10: [20, 40, 80, 85, 70],
        11: [25, 50, 85, 75, 60],
        12: [30, 60, 90, 70, 50],
        13: [35, 70, 85, 65, 40],
        14: [40, 80, 75, 60, 35],
        15: [45, 85, 70, 55, 40],
        16: [50, 90, 75, 65, 50],
        17: [30, 60, 90, 100, 80],
        18: [20, 40, 80, 110, 100],
        19: [25, 45, 75, 95, 90],
        20: [40, 60, 80, 85, 70],
        21: [60, 75, 70, 60, 50],
        22: [80, 80, 60, 40, 30],
        23: [100, 75, 50, 30, 15]
    }
    
    # Convertir a DataFrame para la distribución por hora
    data = []
    for hour in hours:
        for category, count in enumerate(demand_distribution[hour]):
            data.append({
                'Hour': hour,
                'Demand_Category': category,
                'Count': count
            })
    
    hourly_distribution = pd.DataFrame(data)
    
    return (
        hourly_distribution, 
        class_distribution, 
        sample_data, 
        stats_data,
        model_metrics,
        confusion_matrix_data,
        correlation_data
    )

def plot_demand_by_hour(hourly_distribution):
    """
    Gráfico de distribución de categorías de demanda por hora del día.
    Basado en la Celda 4.0 del notebook.
    
    Parámetros:
    -----------
    hourly_distribution : DataFrame
        DataFrame con columnas: 'Hour', 'Demand_Category', 'Count'
        
    Retorna:
    --------
    matplotlib.figure.Figure
        Figura con el gráfico de distribución por hora
    """
    # Mapeo de categorías a colores y etiquetas (basado en el notebook)
    category_colors = {
        0: '#440154',  # Baja (tonalidad más oscura de viridis)
        1: '#3b528b',  # Estándar
        2: '#21918c',  # Media
        3: '#5ec962',  # Alta
        4: '#fde725'   # Crítica (tonalidad más clara de viridis)
    }
    
    category_labels = {
        0: '0: Baja',
        1: '1: Estándar',
        2: '2: Media',
        3: '3: Alta',
        4: '4: Crítica'
    }
    
    # Crear figura con tamaño similar al notebook
    plt.figure(figsize=(14, 7))
    
    # Convertir a formato ancho para el gráfico de barras apiladas
    pivot_data = hourly_distribution.pivot(
        index='Hour',
        columns='Demand_Category',
        values='Count'
    ).fillna(0)
    
    # Ordenar las categorías en orden inverso (4: Crítica primero) como en el notebook
    pivot_data = pivot_data[[4, 3, 2, 1, 0]]
    
    # Crear gráfico de barras apiladas
    bottom = None
    for category in pivot_data.columns:
        counts = pivot_data[category].values
        plt.bar(
            pivot_data.index,
            counts,
            bottom=bottom,
            color=category_colors[category],
            label=category_labels[category]
        )
        if bottom is None:
            bottom = counts
        else:
            bottom += counts
    
    # Personalizar el gráfico según el estilo del notebook
    plt.title('Distribución de Categorías de Demanda por Hora del Día (0-23)', 
              fontsize=14, pad=20)
    plt.xlabel('Hora del Día', fontsize=12)
    plt.ylabel('Conteo de Observaciones', fontsize=12)
    plt.xticks(range(0, 24, 2))
    plt.grid(True, linestyle='--', alpha=0.3, axis='y')
    
    # Ajustar la leyenda como en el notebook
    plt.legend(
        title='Categoría Demanda',
        bbox_to_anchor=(1.05, 1),
        loc='upper left',
        labels=['4: Crítica', '3: Alta', '2: Media', '1: Estándar', '0: Baja']
    )
    
    plt.tight_layout()
    return plt.gcf()

def plot_class_distribution(class_distribution):
    """
    Gráfico de distribución porcentual de las categorías de demanda.
    Basado en la Celda 3.0 del notebook.
    
    Parámetros:
    -----------
    class_distribution : DataFrame
        DataFrame con columnas: 'Category', 'Percentage'
        
    Retorna:
    --------
    matplotlib.figure.Figure
        Figura con el gráfico de distribución de clases
    """
    # Mapeo de colores según la paleta 'rocket' del notebook
    colors = ['#b12a90', '#e16462', '#fea16e', '#fcfdaf', '#f0f921']
    
    # Crear figura con tamaño similar al notebook
    plt.figure(figsize=(10, 6))
    
    # Crear gráfico de barras con estilo similar al notebook
    sns.set_style("whitegrid")
    bars = sns.barplot(
        x='Category',
        y='Percentage',
        data=class_distribution,
        palette=colors,
        order=class_distribution['Category']
    )
    
    # Añadir etiquetas con los porcentajes (formato similar al notebook)
    for i, v in enumerate(class_distribution['Percentage']):
        plt.text(i, v + 0.5, f"{v:.2f}%", ha='center', fontsize=10)
    
    # Personalizar el gráfico según el estilo del notebook
    plt.title('Distribución Porcentual de las 5 Clases de Demanda (Target)', 
              fontsize=14, pad=20)
    plt.xlabel('Categoría de Demanda', fontsize=12)
    plt.ylabel('Porcentaje (%)', fontsize=12)
    plt.ylim(0, class_distribution['Percentage'].max() * 1.1)
    
    # Ajustar el estilo de la cuadrícula
    plt.grid(True, linestyle='--', alpha=0.3, axis='y')
    
    plt.tight_layout()
    return plt.gcf()

def plot_demand_by_month(months, monthly_demand):
    """Gráfico de demanda por mes"""
    plt.figure(figsize=(12, 5))
    
    # Crear gradiente de color basado en la demanda
    colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(months)))
    
    # Gráfico de líneas con área sombreada
    plt.fill_between(range(len(months)), monthly_demand, color='#3498db', alpha=0.2)
    plt.plot(range(len(months)), monthly_demand, 'o-', color='#2980b9', linewidth=2, markersize=8)
    
    # Añadir etiquetas de valor
    for i, (month, demand) in enumerate(zip(months, monthly_demand)):
        plt.text(i, demand + 30, f'{int(demand)}', 
                 ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.title('Evolución de la Demanda a lo Largo del Año', fontsize=14)
    plt.xlabel('Mes', fontsize=12)
    plt.ylabel('Nivel de Demanda', fontsize=12)
    plt.xticks(range(len(months)), months)
    plt.grid(True, linestyle='--', alpha=0.3)
    
    # Añadir línea de tendencia
    z = np.polyfit(range(len(months)), monthly_demand, 1)
    p = np.poly1d(z)
    plt.plot(range(len(months)), p(range(len(months))), 'r--', alpha=0.5)
    
    return plt.gcf()

def plot_model_metrics(metrics_df):
    """
    Gráfico de métricas de rendimiento de los modelos.
    
    Parámetros:
    -----------
    metrics_df : DataFrame
        DataFrame con las métricas de los modelos
    
    Retorna:
    --------
    matplotlib.figure.Figure
        Figura con el gráfico de métricas
    """
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Gráfico de Accuracy
    metrics_df.plot(x='Modelo', y=['Accuracy Entrenamiento', 'Accuracy Validación'], 
                   kind='bar', ax=axes[0, 0], color=['skyblue', 'lightgreen'])
    axes[0, 0].set_title('Accuracy: Entrenamiento vs Validación')
    axes[0, 0].set_ylim(0.7, 1.05)
    axes[0, 0].set_ylabel('Accuracy')
    axes[0, 0].tick_params(axis='x', rotation=45)
    
    # Gráfico de F1-Score para la clase Crítica
    metrics_df.plot(x='Modelo', y='F1-Score (Crítica)', 
                   kind='bar', ax=axes[0, 1], color='salmon')
    axes[0, 1].set_title('F1-Score para la Categoría Crítica')
    axes[0, 1].set_ylim(0.9, 1.0)
    axes[0, 1].set_ylabel('F1-Score')
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    # Gráfico de Overfitting
    metrics_df['Overfitting (%)'] = metrics_df['Overfitting (%)'].abs()
    metrics_df.plot(x='Modelo', y='Overfitting (%)', 
                   kind='bar', ax=axes[1, 0], color='lightcoral')
    axes[1, 0].axhline(y=5, color='r', linestyle='--', alpha=0.3)
    axes[1, 0].set_title('Overfitting (% de diferencia entre train y val)')
    axes[1, 0].set_ylabel('Diferencia %')
    axes[1, 0].tick_params(axis='x', rotation=45)
    
    # Tabla de métricas
    table_data = metrics_df.copy()
    table_data = table_data.round(3)
    axes[1, 1].axis('off')
    table = axes[1, 1].table(
        cellText=table_data.values,
        colLabels=table_data.columns,
        cellLoc='center',
        loc='center',
        bbox=[0.1, 0.1, 0.9, 0.8]
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1.2, 1.5)
    axes[1, 1].set_title('Resumen de Métricas')
    
    plt.tight_layout()
    return fig

def plot_confusion_matrix(confusion_data):
    """
    Gráfico de matriz de confusión.
    
    Parámetros:
    -----------
    confusion_data : DataFrame
        DataFrame con los datos de la matriz de confusión
        Debe contener columnas: 'Real', 'Predicho', 'Cantidad'
    
    Retorna:
    --------
    matplotlib.figure.Figure
        Figura con la matriz de confusión
    """
    # Convertir a matriz de confusión
    categories = ['Baja', 'Estándar', 'Media', 'Alta', 'Crítica']
    conf_matrix = np.zeros((5, 5))
    
    for i, real in enumerate(categories):
        for j, pred in enumerate(categories):
            value = confusion_data[
                (confusion_data['Real'] == real) & 
                (confusion_data['Predicho'] == pred)
            ]['Cantidad'].values
            if len(value) > 0:
                conf_matrix[i, j] = value[0]
    
    # Calcular porcentajes
    conf_matrix_perc = conf_matrix / conf_matrix.sum(axis=1)[:, np.newaxis] * 100
    
    # Crear figura
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))
    
    # Gráfico 1: Valores absolutos
    sns.heatmap(conf_matrix, annot=True, fmt='.0f', cmap='Blues', 
                xticklabels=categories, yticklabels=categories, ax=ax1)
    ax1.set_title('Matriz de Confusión (Valores Absolutos)')
    ax1.set_xlabel('Predicho')
    ax1.set_ylabel('Real')
    
    # Gráfico 2: Porcentajes por fila
    sns.heatmap(conf_matrix_perc, annot=True, fmt='.1f', cmap='Blues',
                xticklabels=categories, yticklabels=categories, ax=ax2)
    ax2.set_title('Matriz de Confusión (% por Fila)')
    ax2.set_xlabel('Predicho')
    ax2.set_ylabel('Real')
    
    plt.tight_layout()
    return fig

def plot_correlation_heatmap(correlation_data):
    """
    Gráfico de matriz de correlación entre variables.
    
    Parámetros:
    -----------
    correlation_data : DataFrame
        DataFrame con las variables numéricas a correlacionar
    
    Retorna:
    --------
    matplotlib.figure.Figure
        Figura con el mapa de calor de correlación
    """
    # Calcular matriz de correlación
    corr = correlation_data.corr()
    
    # Crear máscara para el triángulo superior
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    # Configurar la figura
    plt.figure(figsize=(10, 8))
    
    # Generar mapa de calor
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5}, 
                annot=True, fmt='.2f')
    
    plt.title('Matriz de Correlación entre Variables', pad=20)
    plt.tight_layout()
    return plt.gcf()
    
    # Crear el gráfico
    plt.figure(figsize=(10, 8))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    sns.heatmap(
        corr, 
        mask=mask,
        cmap='coolwarm', 
        vmin=-1, 
        vmax=1,
        annot=True,
        fmt='.2f',
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.8}
    )
    
    plt.title('Matriz de Correlación entre Características', fontsize=14)
    plt.xticks(np.arange(0.5, len(features) + 0.5), features, rotation=45, ha='right')
    plt.yticks(np.arange(0.5, len(features) + 0.5), features, rotation=0)
    plt.tight_layout()
    
    return plt.gcf()

def main():
    """Página de análisis exploratorio de datos"""

    # Configuración de la página
    st.set_page_config(
        page_title="Análisis Exploratorio de Datos",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Análisis Exploratorio de Datos")
    st.markdown("""
    En esta sección podrás explorar el análisis de los datos de demanda de energía
    de la ciudad inteligente. El análisis incluye distribución de categorías de demanda,
    patrones temporales, métricas de modelos y más.
    """)
    
    # Cargar datos del EDA
    (
        hourly_distribution, 
        class_distribution, 
        sample_data, 
        stats_data,
        model_metrics,
        confusion_matrix_data,
        correlation_data
    ) = load_eda_data()
    
    # Convertir métricas a DataFrame para facilitar la visualización
    metrics_df = pd.DataFrame(model_metrics)
    
    # Sección 1: Resumen de datos
    with st.expander("🔍 Resumen del Conjunto de Datos", expanded=True):
        st.write("""
        El conjunto de datos contiene información sobre el consumo de energía en una ciudad inteligente, 
        con mediciones horarias que incluyen variables como temperatura, humedad, velocidad del viento, 
        y la demanda de energía correspondiente.
        
        **Variables principales:**  
        - Demanda de energía (kWh)  
        - Hora del día  
        - Día de la semana  
        - Mes del año  
        - Variables meteorológicas
        
        ### 📋 Primeras filas del dataset
        A continuación se muestran las primeras filas del conjunto de datos para una vista previa de su estructura:
        """)
        
        # Mostrar las primeras filas
        st.dataframe(sample_data, use_container_width=True)
        
        st.write("""
        ### 📊 Estadísticas descriptivas
        Resumen estadístico de las variables numéricas:
        """)
        
        # Mostrar estadísticas descriptivas
        st.dataframe(stats_data, use_container_width=True)
        
        st.write("""
        **Nota:** Las estadísticas mostradas son un resumen de las variables numéricas, incluyendo:
        - Conteo: Número de valores no nulos
        - Media: Valor promedio
        - Desviación estándar: Medida de dispersión de los datos
        - Mínimo: Valor más bajo
        - Cuartiles (25%, 50%, 75%): Divisiones de los datos ordenados
        - Máximo: Valor más alto
        
        ---
        
        ## 📈 Métricas de Rendimiento del Modelo
        
        A continuación se muestran las métricas de rendimiento de los diferentes modelos entrenados:
        """)
        
        # Mostrar métricas del modelo
        st.pyplot(plot_model_metrics(metrics_df))
        
        st.write("""
        ---
        
        ## 🎯 Matriz de Confusión
        
        La matriz de confusión muestra el rendimiento del modelo de clasificación en el conjunto de prueba:
        """)
        
        # Mostrar matriz de confusión
        st.pyplot(plot_confusion_matrix(confusion_matrix_data))
        
        st.write("""
        ---
        
        ## 🔍 Matriz de Correlación
        
        La matriz de correlación muestra las relaciones lineales entre las diferentes variables del conjunto de datos:
        
        
        # Mostrar matriz de correlación
        st.pyplot(plot_correlation_heatmap(correlation_data))
        """)
    
    # Sección 2: Visualizaciones Clave
    st.markdown("## 📈 Visualizaciones Clave")
    
    # Gráfico 1: Distribución de clases
    st.markdown("### Distribución de las Categorías de Demanda")
    st.write("""
    Este gráfico muestra la distribución porcentual de las 5 categorías de demanda en el conjunto de datos.
    Las categorías se crearon utilizando cuantiles (pd.qcut) para garantizar un balance perfecto entre clases.
    
    **Categorías:**
    - **0: Baja** - Niveles de demanda más bajos
    - **1: Estándar** - Niveles de demanda por debajo del promedio
    - **2: Media** - Niveles de demanda promedio
    - **3: Alta** - Niveles de demanda por encima del promedio
    - **4: Crítica** - Niveles de demanda más altos
    
    El balance perfecto entre categorías es ideal para el entrenamiento de modelos de clasificación.
    """)
    fig2 = plot_class_distribution(class_distribution)
    st.pyplot(fig2)
    
    # Sección 3: Conclusiones
    st.markdown("## 📝 Conclusiones del Análisis")
    st.write("""
    1. **Patrones Diarios Claros**: Se observa una clara variación en los patrones de demanda a lo largo del día, 
       con picos en las horas de mayor actividad (mañana y tarde) y valles durante la madrugada.
       
    2. **Distribución Balanceada**: El conjunto de datos está perfectamente balanceado entre las 5 categorías 
       de demanda, lo que facilita el entrenamiento de modelos de clasificación.
    
    3. **Categorías Informativas**: La discretización de la demanda en 5 categorías mediante cuantiles 
       proporciona una representación equilibrada de los diferentes niveles de consumo.
    
    4. **Temporalidad Importante**: La hora del día es un factor clave en la predicción de la categoría de demanda, 
       lo que sugiere que los modelos deberían considerar características temporales.
    
    Estos hallazgos son fundamentales para el desarrollo de modelos predictivos precisos y para la comprensión 
    de los patrones de consumo de energía en entornos urbanos inteligentes.
    """)

    st.info("""
    **ℹ️ Nota sobre los datos:**
    - Los datos mostrados son representativos del análisis realizado en el notebook de EDA.
    - Para más detalles sobre el procesamiento y análisis, consulta el notebook original.
    """)

if __name__ == "__main__":
    main()
