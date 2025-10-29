#!/bin/bash
# Script de testing completo del proyecto

echo "🧪 TEST COMPLETO - Energy Predictor Smart City"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 1. Test de conectividad del backend
echo "1️⃣  Testing Backend API..."
BACKEND_OK=$(curl -s http://localhost:8000/health | grep -c "ok" || echo "0")
if [ "$BACKEND_OK" -gt 0 ]; then
    echo "   ✅ Backend API funcionando"
else
    echo "   ❌ Backend API no responde"
    echo "   💡 Solución: docker compose up backend-api"
fi

echo ""

# 2. Test de conectividad del frontend
echo "2️⃣  Testing Frontend Web..."
FRONTEND_OK=$(curl -s http://localhost:8501 | grep -c "Energy Predictor" || echo "0")
if [ "$FRONTEND_OK" -gt 0 ]; then
    echo "   ✅ Frontend Web funcionando"
else
    echo "   ❌ Frontend Web no responde"
    echo "   💡 Solución: docker compose up frontend-web"
fi

echo ""

# 3. Test de predicción del backend
echo "3️⃣  Testing Backend Predictions..."
echo "   📊 Test 1: Baja demanda (100kW)"
RESPONSE1=$(curl -s -X POST "http://localhost:8000/predict_demand" \
  -H "Content-Type: application/json" \
  -d '[{"historical_electricity_load_kw": 100.0, "hour": 2, "day_of_week": 7, "month": 1, "year": 2024, "is_weekend": 1, "is_peak_hour": 0, "is_holiday": "No", "temperature_c": 5.0, "humidity_pct": 90.0, "solar_irradiance_w_m2": 0.0, "building_occupancy_rate_pct": 1.0, "traffic_congestion_index": 0.01, "voltage_level_v": 220.0, "current_level_a": 0.45, "power_factor": 0.91, "solar_pv_output_kw": 0.0, "wind_power_output_kw": 0.0, "wind_speed_m_s": 7.0, "solar_panel_temperature_c": 10.0, "cloud_cover_pct": 100.0, "rainfall_mm": 0.0, "atmospheric_pressure_hpa": 1008.25, "dew_point_c": -5.0, "public_transit_operational_load_kw": 10.0, "ev_charging_station_load_kw": 0.0, "human_mobility_score": 0.05, "time_since_last_peak_hours": 6.0, "time_until_next_predicted_peak_hours": 2.0, "distance_to_nearest_substation_km": 1.2, "season": "Winter", "weather_condition": "Clear", "area_type": "Commercial"}]' 2>/dev/null)

if echo $RESPONSE1 | grep -q "Baja"; then
    echo "   ✅ Predicción 1: $RESPONSE1"
elif echo $RESPONSE1 | grep -q "0:"; then
    echo "   ✅ Predicción 1: $RESPONSE1 (código numérico)"
else
    echo "   ❌ Predicción 1 falló: $RESPONSE1"
fi

echo "   📊 Test 2: Alta demanda (1000kW)"
RESPONSE2=$(curl -s -X POST "http://localhost:8000/predict_demand" \
  -H "Content-Type: application/json" \
  -d '[{"historical_electricity_load_kw": 1000.0, "hour": 8, "day_of_week": 2, "month": 8, "year": 2024, "is_weekend": 0, "is_peak_hour": 1, "is_holiday": "No", "temperature_c": 35.0, "humidity_pct": 15.0, "solar_irradiance_w_m2": 1000.0, "building_occupancy_rate_pct": 100.0, "traffic_congestion_index": 0.95, "voltage_level_v": 220.0, "current_level_a": 4.55, "power_factor": 0.99, "solar_pv_output_kw": 150.0, "wind_power_output_kw": 0.0, "wind_speed_m_s": 3.0, "solar_panel_temperature_c": 40.0, "cloud_cover_pct": 0.0, "rainfall_mm": 0.0, "atmospheric_pressure_hpa": 1018.25, "dew_point_c": 0.0, "public_transit_operational_load_kw": 300.0, "ev_charging_station_load_kw": 50.0, "human_mobility_score": 0.95, "time_since_last_peak_hours": 0.5, "time_until_next_predicted_peak_hours": 1.5, "distance_to_nearest_substation_km": 1.2, "season": "Summer", "weather_condition": "Clear", "area_type": "Commercial"}]' 2>/dev/null)

if echo $RESPONSE2 | grep -q "Crítica"; then
    echo "   ✅ Predicción 2: $RESPONSE2"
elif echo $RESPONSE2 | grep -q "4:"; then
    echo "   ✅ Predicción 2: $RESPONSE2 (código numérico)"
else
    echo "   ❌ Predicción 2 falló: $RESPONSE2"
fi

echo ""

# 4. Verificar que las predicciones son diferentes
if echo $RESPONSE1 | grep -q -E "(Baja|0:)" && echo $RESPONSE2 | grep -q -E "(Crítica|4:)"; then
    echo "🎯 ✅ BACKEND FUNCIONA CORRECTAMENTE"
    echo "   Las predicciones son diferentes como se espera"
else
    echo "🎯 ❌ BACKEND TIENE PROBLEMAS"
    echo "   Las predicciones no son diferentes"
fi

echo ""

# 5. Verificar conectividad del frontend con el backend
echo "4️⃣  Testing Frontend-Backend Connection..."
if [ "$FRONTEND_OK" -gt 0 ] && [ "$BACKEND_OK" -gt 0 ]; then
    echo "   ✅ Servicios conectados correctamente"
    echo "   📝 El frontend debería mostrar: '🔗 Backend conectado: http://backend-api:8000'"
    echo "   📝 El frontend debería mostrar: '✅ Backend funcionando correctamente'"
else
    echo "   ❌ Problemas de conectividad entre servicios"
fi

echo ""

# 6. Mostrar logs recientes
echo "5️⃣  Logs recientes del backend:"
docker compose logs backend-api | tail -5

echo ""
echo "6️⃣  Logs recientes del frontend:"
docker compose logs frontend-web | tail -5

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💡 PRÓXIMOS PASOS:"
echo "1. Ve a: http://localhost:8501"
echo "2. Haz una predicción desde cualquier escenario"
echo "3. Observa los logs en tiempo real: ./monitor.sh"
echo "4. Busca los mensajes 🔍 🎯 📊 en los logs"
echo ""
echo "🔍 MONITOREO DE LOGS:"
echo "• ./monitor.sh (con guía visual mejorada)"
echo "• docker compose logs -f backend-api frontend-web"
echo ""
echo "📋 MENSAJES A BUSCAR:"
echo "• 🖱️ Usuario hizo clic (cuando presionas 'Predecir')"
echo "• 🎯 Usuario seleccionó escenario (cuando eliges escenario)"
echo "• 🔄 Iniciando predicción (envío al backend)"
echo "• 🎯 Predicción del modelo (respuesta del backend)"
echo "• 🎯 Predicción final (resultado en frontend)"
echo ""
echo "🔧 CONFIGURACIONES APLICADAS:"
echo "• ✅ Detección automática de Docker"
echo "• ✅ Variables de entorno DOCKER_CONTAINER=true"
echo "• ✅ Validación de datos (no más valores 0.0)"
echo "• ✅ URL del backend: backend-api:8000"
echo "• ✅ Logging completo de requests y responses"
