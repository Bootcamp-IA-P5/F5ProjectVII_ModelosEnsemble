#!/bin/bash
# Script para ver logs en tiempo real de ambos servicios

echo "🔍 Iniciando logs en tiempo real..."
echo "📊 Backend API logs:"
echo "📱 Frontend Web logs:"
echo ""
echo "💡 Para salir: Ctrl+C"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🎯 Busca estos mensajes clave cuando hagas predicciones:"
echo "   🔄 Iniciando predicción... (Frontend)"
echo "   📦 Payload a enviar: [...] (Frontend)"
echo "   🎯 Predicción del modelo: X.X (Backend)"
echo "   🎯 Predicción final: X: XXX (Frontend)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Mostrar logs de ambos servicios en tiempo real con colores
docker compose logs -f --tail=50 backend-api frontend-web
