# 🔍 Guía de Logs - Energy Predictor Smart City

## 📋 **¿Cómo ver los logs cuando usas la interfaz web?**

Los logs SÍ se registran cuando interactúas con la aplicación desde el navegador. Para verlos en tiempo real, ejecuta:

```bash
# Opción 1: Script mejorado con guía
./monitor.sh

# Opción 2: Script original
./logs.sh

# Opción 3: Comando directo
docker compose logs -f backend-api frontend-web
```

## 🎯 **¿Qué logs buscar cuando haces predicciones?**

### **FRONTEND** (Interfaz de usuario)
```
🖱️ Usuario hizo clic en 'Predecir Demanda'
🎯 Usuario seleccionó escenario: 🏠 Baja Demanda
📋 Datos del formulario: {...}
⚠️ temperature_c estaba en 0.0, usando valor por defecto: 20.0
✅ Datos validados: {...}
🔧 Variables por defecto generadas: 23
📊 Total de variables para predicción: 33
🚀 Enviando datos al backend para predicción...
🔄 Iniciando predicción...
📦 Payload a enviar: [...]
📡 Response status: 200
✅ Resultado recibido: [...]
🎯 Predicción final: 0: Baja
```

### **BACKEND** (Motor de IA)
```
🔍 Datos de entrada después del mapeo: (1, 33)
🎯 Predicción del modelo: 0.0
📊 Input values: {...}
POST /predict_demand HTTP/1.1" 200 OK
```

## 📊 **Flujo Completo de Logs**

1. **Usuario selecciona escenario** → `🎯 Usuario seleccionó escenario:`
2. **Usuario hace clic en predecir** → `🖱️ Usuario hizo clic en`
3. **Validación de datos** → `⚠️ Variables con valores por defecto`
4. **Generación de datos** → `🔧 Variables por defecto generadas`
5. **Envío al backend** → `🚀 Enviando datos al backend`
6. **Recepción en backend** → `🔍 Datos de entrada después del mapeo`
7. **Predicción del modelo** → `🎯 Predicción del modelo: X.X`
8. **Respuesta del backend** → `POST /predict_demand HTTP/1.1" 200 OK`
9. **Recepción en frontend** → `✅ Resultado recibido`
10. **Visualización final** → `🎯 Predicción final: X: XXX`

## 💡 **Consejos para Debugging**

- **Si no ves logs:** Asegúrate de que ambos servicios estén corriendo
- **Logs retrasados:** Los logs aparecen cuando se completa la predicción
- **Warnings normales:** Los `⚠️` son informativos, no errores
- **Para más detalles:** Los logs se guardan en `docker compose logs`

## 🚀 **Ejemplo de Uso**

1. Abre **http://localhost:8501** en tu navegador
2. Ejecuta **`./monitor.sh`** en una terminal
3. Selecciona un escenario (ej: 🏠 Baja Demanda)
4. Haz clic en **"🔮 Predecir Demanda"**
5. **Observa los logs en tiempo real** en la terminal

**Verás aparecer todos los mensajes paso a paso mostrando exactamente qué está haciendo el sistema.** 🎯
