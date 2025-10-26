#!/bin/bash
# Script para reiniciar el proyecto completo

echo "🔄 Reiniciando Energy Predictor Smart City..."
echo ""

# Detener servicios
echo "⏹️  Deteniendo servicios..."
docker compose down

# Limpiar contenedores e imágenes antiguas
echo "🧹 Limpiando contenedores antiguos..."
docker system prune -f

# Construir e iniciar servicios con logs
echo "🔨 Construyendo servicios..."
echo "🚀 Iniciando servicios..."
echo ""
echo "📊 Backend API: http://localhost:8000"
echo "🌐 Frontend Web: http://localhost:8501"
echo ""
echo "🔍 Los logs se mostrarán automáticamente:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Construir primero para evitar problemas de cache
docker compose build --no-cache

# Iniciar servicios
docker compose up
