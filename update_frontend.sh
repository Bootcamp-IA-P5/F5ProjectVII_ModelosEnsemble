#!/bin/bash
# Script para actualizar solo el frontend con los cambios

echo "🔄 Actualizando frontend con los últimos cambios..."
echo ""

echo "⏹️  Deteniendo frontend..."
docker compose down frontend-web

echo "🔨 Reconstruyendo frontend (sin cache)..."
docker compose build --no-cache frontend-web

echo "🚀 Iniciando frontend actualizado..."
docker compose up -d frontend-web

echo ""
echo "✅ Frontend actualizado!"
echo "🌐 Ve a: http://localhost:8501"
echo ""
echo "📋 Los cambios aplicados:"
echo "• ✅ Función test_backend_connection agregada"
echo "• ✅ Validación de conectividad con el backend"
echo "• ✅ Manejo de errores mejorado"
echo "• ✅ Logging completo de requests y responses"
echo ""
echo "🔍 Verifica en los logs que ahora funciona:"
echo "docker compose logs frontend-web"
