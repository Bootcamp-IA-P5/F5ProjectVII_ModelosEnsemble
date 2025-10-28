#!/bin/bash
# Script para iniciar el proyecto completo con logs automáticos

echo "🚀 Iniciando Energy Predictor Smart City..."
echo "📊 Backend API: http://localhost:8000"
echo "🌐 Frontend Web: http://localhost:8501"
echo ""
echo "🔍 Los logs se mostrarán automáticamente a continuación:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Iniciar servicios y mostrar logs en tiempo real
docker compose up --build
