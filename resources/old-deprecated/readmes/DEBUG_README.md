# 🔍 DEBUGGING - Energy Predictor Smart City

## 🎯 **PROBLEMA ACTUAL**
Las predicciones del frontend siempre devuelven el mismo resultado, aunque el backend funciona correctamente.

## ✅ **SOLUCIONES IMPLEMENTADAS**

### **1. 🔧 Detección Automática de Docker**
- **Múltiples métodos de detección:** cgroup, variables de entorno, hostname
- **Variable de entorno:** `DOCKER_CONTAINER=true` en docker-compose.yml
- **URL automática:** `backend-api:8000` (Docker) vs `localhost:8000` (desarrollo)

### **2. 🔍 Logging Completo**
- **Frontend logs:** URL, payload, response status, errores
- **Backend logs:** Predicciones del modelo, datos de entrada
- **Tiempo real:** `docker compose logs -f` o `./logs.sh`

### **3. ✅ Validación de Datos**
- **No más valores 0.0:** Validación automática de inputs del usuario
- **Valores realistas:** Mínimos y máximos para evitar datos extremos
- **Logging de validaciones:** Muestra qué valores se corrigieron

### **4. 🚀 Scripts de Debugging**
```bash
./restart.sh    # Reiniciar todo con limpieza completa
./logs.sh       # Ver logs en tiempo real
./test.sh       # Test completo de funcionalidades
```

## 🚀 **COMANDOS RÁPIDOS DE DEBUGGING**

### **1. Reiniciar todo (recomendado):**
```bash
./restart.sh
```

### **2. Ver logs en tiempo real:**
```bash
./logs.sh
# O manualmente:
docker compose logs -f backend-api frontend-web
```

### **3. Test completo:**
```bash
./test.sh
```

### **4. Ver logs específicos:**
```bash
docker compose logs -f backend-api   # Solo backend
docker compose logs -f frontend-web  # Solo frontend
```

## 🔧 **VERIFICACIONES MANUALES**

### **1. Backend funcionando:**
🌐 **http://localhost:8000/health**
- ✅ Debería devolver: `{"status":"ok","model_loaded":true}`

### **2. Frontend funcionando:**
🌐 **http://localhost:8501**
- ✅ Debería mostrar: "🔗 **Backend conectado:** http://backend-api:8000"
- ✅ Debería mostrar: "✅ **Backend funcionando correctamente**"

### **3. Test directo del backend:**
```bash
curl -X POST "http://localhost:8000/predict_demand" \
  -H "Content-Type: application/json" \
  -d '[{"historical_electricity_load_kw": 100.0, ...}]'
```

## 📊 **LOGS A BUSCAR**

### **En logs del BACKEND (deberías ver):**
```
🔍 Datos de entrada después del mapeo: (1, 33)
🎯 Predicción del modelo: 0.0  ← Baja demanda
🎯 Predicción del modelo: 4.0  ← Alta demanda
```

### **En logs del FRONTEND (deberías ver):**
```
🔄 Iniciando predicción...
🔗 URL del backend: http://backend-api:8000/predict_demand
📊 Número de variables: 33
📦 Payload a enviar: [...]
📡 Response status: 200
✅ Resultado recibido: [...]
🎯 Predicción final: 0: Baja
🧪 Testeando conexión con: http://backend-api:8000/health
✅ Backend responde correctamente
```

## 🐛 **PREGUNTAS DE DEBUGGING**

1. **¿Ves el mensaje "🔗 Backend conectado: backend-api:8000" en el frontend?**
   - ✅ **SÍ** → Detección de Docker OK
   - ❌ **NO** → Problema de detección de Docker

2. **¿Aparecen logs del backend cuando haces una predicción?**
   - ✅ **SÍ** → Backend recibe datos correctamente
   - ❌ **NO** → Frontend no envía requests

3. **¿Aparecen logs del frontend cuando haces una predicción?**
   - ✅ **SÍ** → Frontend hace requests correctamente
   - ❌ **NO** → Problema en la función make_prediction()

4. **¿Las predicciones del backend directo son diferentes?**
   - ✅ **SÍ** → Backend funciona correctamente
   - ❌ **NO** → Problema en el modelo

5. **¿Ves mensajes de validación (⚠️) en los logs?**
   - ✅ **SÍ** → Validación de datos funcionando
   - ❌ **NO** → No hay datos en 0.0

## 🔍 **PASOS PARA DEBUGGING**

1. **Ejecuta:** `./restart.sh` (limpia todo y reconstruye)
2. **Ve a:** http://localhost:8501
3. **Verifica:** "🔗 Backend conectado: backend-api:8000"
4. **Verifica:** "✅ Backend funcionando correctamente"
5. **Haz una predicción** desde cualquier escenario
6. **Observa los logs** en tiempo real: `./logs.sh`
7. **Busca los mensajes** 🔍 🎯 📊 🧪 en los logs

## 📋 **ARCHIVOS DE CONFIGURACIÓN**

- **docker-compose.yml** → Configuración de servicios y logging
- **frontend/app.py** → Logging de requests y responses + validación de datos
- **backend/api/main.py** → Logging de predicciones del modelo
- **.env** → Variables de entorno (API_PORT=8000)
- **restart.sh** → Script de reinicio completo
- **test.sh** → Script de testing completo

## 💡 **SOLUCIONES COMUNES**

1. **Reiniciar todo:** `./restart.sh` (con limpieza de cache)
2. **Ver logs específicos:** `docker compose logs backend-api`
3. **Test directo:** curl al backend
4. **Limpiar cache:** `docker system prune -f`
5. **Verificar Docker:** Asegurarse que DOCKER_CONTAINER=true esté configurado

## 🎯 **LO QUE SE CORRIGIÓ**

1. ✅ **URL del backend:** Ahora usa `backend-api:8000` correctamente
2. ✅ **Validación de datos:** No más valores 0.0 que causen problemas
3. ✅ **Logging completo:** Puedes ver exactamente qué se envía y qué se recibe
4. ✅ **Detección de Docker:** Múltiples métodos para asegurar la URL correcta
5. ✅ **Scripts de debugging:** Automatización completa del proceso de debugging

## 🚨 **SI SIGUE SIN FUNCIONAR**

1. **Verifica el test completo:** `./test.sh`
2. **Revisa los logs específicos:** `docker compose logs frontend-web`
3. **Busca errores de conexión:** `Connection refused` o `Max retries exceeded`
4. **Verifica que el backend responde:** `curl http://localhost:8000/health`
5. **Verifica que el frontend detecta Docker:** Busca "backend-api:8000" en logs

**El sistema ahora está completamente instrumentado para debugging. Los logs te dirán exactamente dónde está el problema.** 🔍📊
