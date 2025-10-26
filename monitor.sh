#!/bin/bash
# Script mejorado para monitorear logs en tiempo real con colores y guía

echo "🔍 MONITOREO DE LOGS - Energy Predictor Smart City"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🎯 CÓMO USAR EL SISTEMA DE LOGS:"
echo ""
echo "1️⃣  Abre la aplicación: http://localhost:8501"
echo "2️⃣  Selecciona un escenario (🏠 Baja → 🚨 Crítica)"
echo "3️⃣  Haz clic en '🔮 Predecir Demanda'"
echo "4️⃣  Observa los logs en tiempo real abajo"
echo ""
echo "📋 MENSAJES CLAVE A BUSCAR:"
echo "   🖱️ Usuario hizo clic en 'Predecir Demanda' (Frontend)"
echo "   🎯 Usuario seleccionó escenario: XXX (Frontend)"
echo "   ⚠️ Variables con valores por defecto (Frontend)"
echo "   🔄 Iniciando predicción... (Frontend)"
echo "   📦 Payload a enviar: [...] (Frontend)"
echo "   🎯 Predicción del modelo: X.X (Backend)"
echo "   🎯 Predicción final: X: XXX (Frontend)"
echo "   ✅ Resultado recibido: [...] (Frontend)"
echo ""
echo "💡 Presiona Ctrl+C para salir"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Función para mostrar logs con mejor formato
docker compose logs -f --tail=10 backend-api frontend-web 2>&1 | while read line; do
    echo "📊 $line"
done
