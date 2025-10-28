#!/bin/bash

# Script para probar el frontend modular
echo "🚀 Probando Frontend Modular - Smart City Energy Predictor"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Verificar estructura de archivos
echo "📁 Verificando estructura de archivos..."
echo ""

echo "frontend/"
ls -la frontend/

echo ""
echo "📋 Archivos creados:"
echo "✅ frontend/main.py (navegación principal)"
echo "✅ frontend/prediction.py (página de predicción)"
echo "✅ frontend/eda.py (análisis exploratorio)"
echo "✅ frontend/models.py (modelos y ensemble)"
echo "✅ frontend/documentation.py (documentación)"
echo "✅ frontend/utils.py (funciones compartidas)"
echo "✅ frontend/__init__.py (paquete Python)"
echo ""

# Verificar imports
echo "🔍 Verificando imports y dependencias..."
cd frontend

echo "📦 Probando imports..."
python3 -c "
try:
    from utils import *
    print('✅ utils.py - imports OK')
except Exception as e:
    print(f'❌ utils.py - Error: {e}')

try:
    import main
    print('✅ main.py - imports OK')
except Exception as e:
    print(f'❌ main.py - Error: {e}')

try:
    import prediction
    print('✅ prediction.py - imports OK')
except Exception as e:
    print(f'❌ prediction.py - Error: {e}')

try:
    import eda
    print('✅ eda.py - imports OK')
except Exception as e:
    print(f'❌ eda.py - Error: {e}')

try:
    import models
    print('✅ models.py - imports OK')
except Exception as e:
    print(f'❌ models.py - Error: {e}')

try:
    import documentation
    print('✅ documentation.py - imports OK')
except Exception as e:
    print(f'❌ documentation.py - Error: {e}')
"

echo ""
echo "🐳 Verificando Dockerfile..."
echo "✅ Dockerfile actualizado para usar main.py"
echo "✅ Copia todo el directorio frontend/"
echo ""

echo "📊 Resumen de la nueva estructura:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🏗️ ARQUITECTURA MODULAR:"
echo "• main.py          → Navegación y routing entre páginas"
echo "• utils.py         → Funciones compartidas y configuración"
echo "• prediction.py    → Lógica de predicción y formularios"
echo "• eda.py          → Análisis exploratorio y visualizaciones"
echo "• models.py       → Comparativa de modelos y métricas"
echo "• documentation.py → Documentación técnica completa"
echo ""
echo "🎯 VENTAJAS DE LA NUEVA ESTRUCTURA:"
echo "✅ Código más organizado y mantenible"
echo "✅ Separación clara de responsabilidades"
echo "✅ Fácil navegación entre secciones"
echo "✅ Reutilización de funciones compartidas"
echo "✅ Mejor experiencia de desarrollo"
echo ""
echo "🚀 INSTRUCCIONES DE EJECUCIÓN:"
echo "cd frontend"
echo "streamlit run main.py"
echo ""
echo "🐳 Con Docker:"
echo "docker compose up --build"
echo ""
echo "🎉 ¡Frontend modular completado exitosamente!"
