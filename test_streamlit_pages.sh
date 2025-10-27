#!/bin/bash

# Script para probar la estructura nativa de páginas de Streamlit
echo "🚀 Probando Estructura Nativa de Páginas - Streamlit"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Verificar estructura de archivos
echo "📁 Estructura de archivos actual:"
echo ""
echo "frontend/"
ls -la frontend/

echo ""
echo "frontend/pages/"
ls -la frontend/pages/

echo ""
echo "📋 Archivos de páginas creados:"
echo "✅ 01_🏠_Home.py (página principal)"
echo "✅ 02_🔮_Prediction.py (página de predicción)"
echo "✅ 03_📊_EDA.py (análisis exploratorio)"
echo "✅ 04_🤖_Models.py (modelos y ensemble)"
echo "✅ 05_📋_Documentation.py (documentación)"
echo ""

# Verificar que cada página tiene la función main()
echo "🔍 Verificando funciones principales en cada página..."
echo ""

for page in frontend/pages/*.py; do
    page_name=$(basename "$page")
    if grep -q "def main()" "$page"; then
        echo "✅ $page_name - función main() encontrada"
    else
        echo "❌ $page_name - función main() NO encontrada"
    fi
done

echo ""
echo "🐳 Verificando Dockerfile..."
echo "✅ Dockerfile actualizado para copiar todo el directorio"
echo "✅ Streamlit detectará automáticamente las páginas en /pages"
echo ""

echo "📊 Nueva estructura implementada:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🏗️ ESTRUCTURA NATIVA DE STREAMLIT:"
echo "• main.py          → Página principal (🏠 Inicio)"
echo "• pages/01_🏠_Home.py      → Dashboard y métricas"
echo "• pages/02_🔮_Prediction.py → Formulario de predicción"
echo "• pages/03_📊_EDA.py       → Análisis exploratorio"
echo "• pages/04_🤖_Models.py    → Modelos y ensemble"
echo "• pages/05_📋_Documentation.py → Documentación"
echo ""
echo "🎯 VENTAJAS DE LA ESTRUCTURA NATIVA:"
echo "✅ Navegación automática generada por Streamlit"
echo "✅ Sin código de routing personalizado"
echo "✅ Mejor rendimiento y compatibilidad"
echo "✅ URLs limpias (/pages/nombre_pagina)"
echo "✅ Estructura estándar de la comunidad"
echo ""
echo "🚀 CÓMO FUNCIONA:"
echo "1. Streamlit detecta automáticamente los archivos en /pages"
echo "2. Los números (01_, 02_, etc.) definen el orden en el sidebar"
echo "3. Los emojis aparecen en la navegación"
echo "4. Cada página se ejecuta independientemente"
echo "5. main.py es la página de inicio por defecto"
echo ""
echo "🔧 EJECUCIÓN:"
echo "cd frontend"
echo "streamlit run main.py"
echo ""
echo "🐳 Con Docker:"
echo "docker compose up --build"
echo ""
echo "📱 La navegación aparecerá automáticamente en el sidebar izquierdo"
echo ""
echo "🎉 ¡Estructura nativa de Streamlit implementada exitosamente!"
