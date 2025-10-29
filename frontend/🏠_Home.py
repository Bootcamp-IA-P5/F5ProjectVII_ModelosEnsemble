"""
🚨 Energy Crisis Predictor - Smart City Guardian
IA que previene colapsos energéticos urbanos antes de que ocurran
"""
import streamlit as st
from utils import *

def main():
    """Dashboard principal del sistema de predicción de crisis energéticas"""

    # Configuración de la página principal
    st.set_page_config(
        page_title="⚡ Crisis Predictor - Smart City Guardian",
        layout="wide",
        page_icon="⚡"
    )

    # Aplicar estilos CSS
    st.markdown(get_css_styles(), unsafe_allow_html=True)

    # Título principal con gancho
    st.markdown('<h1 class="main-header">⚡⚡ Smart City Crisis Guardian ⚡⚡</h1>', unsafe_allow_html=True)
    
    # Introducción con storytelling impactante
    st.subheader("🚨🚨🚨🚨🚨🚨🚨 RIESGO DE APAGON INMINENTE: 🚨🚨🚨🚨🚨🚨🚨 ")

    st.warning("""
    ⚠️ Ciudades enteras a oscuras. Tráfico caótico, hospitales sin energía, y toda la economía paralizada. 
    
    Por supuesto que ninguno queremos que vuelva a suceder nada parecido, por lo que...

    ¿Y si pudieramos predecirlo mas eficazmente?
    """)

    st.markdown("**🧠 Kiru Solutions S.L. presenta: la IA que predice crisis energéticas ANTES de que impacten en tu Ciudad**")

    # Estado del sistema con lenguaje más impactante
    backend_ok = test_backend_connection()

    if backend_ok:
        st.success("""✅ **IA Guardián activa - Protegiendo tu ciudad ✅**

    - 🚨 Detecta demandas críticas que pueden colapsar la red
    - 🔮 Predice 5 niveles de riesgo
    - 🧠 Solo necesita 10 datos - el resto lo calcula internamente
    - ⚡ Respuesta en 200ms - más rápido que contartar a Flash
    - 🎯 Protege lo que más importa: tu ciudad, tu gente, tu futuro.
    """)
        st.info("💡 El sistema está disponible 24/7, para adelantarse a cualquier crisis energética en todo momento")
    else:
        st.error("❌ **¡ALERTA! Guardián desconectado** - Ciudad en riesgo")

    st.markdown("---")

    # Métricas principales con contexto de crisis
    st.header("📊 Centro de Control - Vigilancia en Tiempo Real")
    metrics = get_model_metrics()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎯 Detección de Crisis", f"{metrics['accuracy']:.1%}", delta="+0.08%", help="Precisión para detectar demandas críticas")
    with col2:
        st.metric("🚨 Prevención de Blackouts", f"{metrics['f1_critica']:.1%}", delta="+0.21%", help="Efectividad en clase más crítica")
    with col3:
        st.metric("🔄 Estabilidad del Sistema", f"{metrics['overfitting']:.2%}", delta="+0.00%", help="Control de sobreajuste")
    with col4:
        st.metric("⚡ Tiempo de Respuesta", "~200ms", help="Velocidad de predicción de crisis")

    st.markdown("---")

    st.subheader("📊 Sistema de Clasificación - 5 Niveles de Riesgo")

    st.info("""
    **El Guardián clasifica la demanda eléctrica en 5 niveles de riesgo:**

    - 🟢 **Baja** (0-229 kW): Horas valle, mínima actividad
    - 🔵 **Estándar** (229-343 kW): Consumo normal, actividad regular  
    - 🟡 **Media** (343-467 kW): Horas laborales, actividad moderada
    - 🟠 **Alta** (467-645 kW): Horas pico, alta actividad
    - 🔴 **Crítica** (645+ kW): Máxima demanda, **emergencia potencial**

    **🛡️ Con 91.09% de precisión en detección de crisis**
    """)
    # Cómo funciona con lenguaje de crisis
    st.subheader("🛡️ A cargo de la protección de tu Ciudad")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""

        **🚨 Cómo se detecta una crisis:**
        - Me he basado en un dataset de 72,960 de patrones de consumo, 
        - He identificado una serie de variables que, sin vigilancia, 
        pueden ocasionar una crisi energética
        - Gracias a esto, he entrenado un modelo de ML capaz de predecir 
        picos de demanda que superen la capacidad de la red
        - Para comprobar su eficazia rapidamente, se han definido 
        varios escenarios "tipo", basandonos en 5 niveles de riesgo.

        """)

    with col2:
        st.markdown("""
        
        **📊 Análisis Inteligente y validación:**
        - Visualiza patrones de consumo personalizados al momento
        - Validado con técnicas de ensemble avanzadas
        - Predicciones confiables al 96.67% para los casos críticos


         **⚡ Posibles usos de esta tecnología:**
        - Alertas inmediatas que se enviaran a los operadores de red
        - Recomendaciones de acciones preventivas
        - Alerta para la activacion inmediata de reservas de emergencia
        """)

    # Navegación con contexto de crisis
    st.subheader("🚀 Centro de Control - Accede a Todas las Funciones")

    st.info("""
    **🎛️ Usa el panel de control lateral para gestionar la protección:**

    - **🏠 Home**: Centro de control y metricas generales
    - **🔮 Predicción**: Simula escenarios de crisis y prueba respuestas en tiempo real
    - **📊 EDA**: Analiza el dataset y muestra visualizaciones de interés
    - **🤖 Modelos & Ensemble**: Comparativa de algoritmos
    - **📋 Documentación**: Guía y troubleshooting

    """)

    # Footer con llamada a la acción
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p><strong>⚡ ⚡  Smart City Crisis Guardian⚡ ⚡ </strong></p>
        <p>Cuando la energía falla, el guardian responde</p>
        <p><em>Kiru Solutions S.L.</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
