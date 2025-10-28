# 🚀 Frontend Modular - Smart City Energy Predictor

## 📁 Estructura del Frontend

El frontend ha sido completamente reestructurado en módulos separados para mejor organización y mantenibilidad:

```
frontend/
├── main.py              # 🏠 Navegación principal y routing
├── utils.py             # 🔧 Funciones compartidas y configuración
├── prediction.py        # 🔮 Página de predicción de demanda
├── eda.py              # 📊 Análisis exploratorio de datos
├── models.py           # 🤖 Modelos y técnicas de ensemble
├── documentation.py    # 📋 Documentación técnica
├── __init__.py         # 📦 Paquete Python
└── Dockerfile          # 🐳 Containerización actualizada
```

## 🎯 Características de la Nueva Estructura

### ✅ **Separación por Responsabilidades**
- Cada página tiene su propio archivo dedicado
- Funciones compartidas centralizadas en `utils.py`
- Navegación intuitiva en el sidebar

### ✅ **Navegación Mejorada**
- Sidebar con botones de navegación
- Estado de página preservado con session_state
- Indicadores visuales de página activa

### ✅ **Mantenibilidad**
- Código más limpio y organizado
- Fácil localización de funcionalidades
- Reutilización de componentes

## 🚀 Cómo Ejecutar

### **Desarrollo Local:**
```bash
cd frontend
streamlit run main.py
```

### **Con Docker:**
```bash
# Desde la raíz del proyecto
docker compose up --build

# El Dockerfile ya está actualizado para usar main.py
```

## 📋 Páginas Disponibles

### 🏠 **main.py - Página Principal**
- Dashboard con métricas principales
- Navegación entre todas las páginas
- Estado del sistema y conectividad

### 🔮 **prediction.py - Predicción**
- Formulario con 10 variables principales
- Escenarios de demostración (5 categorías)
- Validación y envío de predicciones
- Variables automáticas generadas por IA

### 📊 **eda.py - Análisis Exploratorio**
- Visualizaciones del dataset (72,960 registros)
- Distribución por horas y feature importance
- Análisis de balance de clases
- Métricas de calidad del dataset

### 🤖 **models.py - Modelos & Ensemble**
- Comparativa de 5 modelos implementados
- Métricas detalladas por clase
- Técnicas de optimización (GridSearchCV, StratifiedKFold)
- Feature importance y pipeline de preprocesamiento

### 📋 **documentation.py - Documentación**
- Guía técnica completa del proyecto
- Arquitectura del sistema
- Escenarios de uso y troubleshooting
- Métricas de rendimiento y rúbrica

## 🔧 Funciones Compartidas (utils.py)

### **Configuración Global:**
- `get_backend_url()` - Detección automática de entorno Docker
- `test_backend_connection()` - Verificación de conectividad
- `get_model_metrics()` - Obtención de métricas del modelo

### **Funciones de Predicción:**
- `generate_default_values()` - Cálculo de 23 variables automáticas
- `create_scenario_data()` - Escenarios predefinidos
- `make_prediction()` - Envío de predicciones al backend

### **Estilos CSS:**
- `get_css_styles()` - Estilos personalizados para toda la app

## 🎨 Mejoras Visuales

### **Navegación Sidebar:**
- Botones de navegación con iconos
- Indicadores de página activa
- Estado del sistema en tiempo real

### **Interfaz Consistente:**
- Header unificado en todas las páginas
- Estilos CSS compartidos
- Layout responsive y moderno

### **Experiencia de Usuario:**
- Navegación intuitiva y fluida
- Carga rápida de páginas
- Información contextual en cada sección

## 🔄 Migración desde app.py

### **Cambios Realizados:**
1. **app.py** → **main.py** (navegación principal)
2. **Pestañas** → **Páginas separadas**
3. **Funciones duplicadas** → **utils.py centralizadas**
4. **CSS y configuración** → **Compartidas globalmente**

### **Compatibilidad:**
- ✅ Mismas funcionalidades que antes
- ✅ Misma API del backend
- ✅ Mismas métricas y visualizaciones
- ✅ Mejores organización y mantenibilidad

## 🐳 Docker

El Dockerfile ha sido actualizado:
```dockerfile
# Antes
COPY frontend/app.py .

# Después
COPY frontend/ .
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🎉 Beneficios de la Nueva Estructura

### **Para Desarrolladores:**
- ✅ Código más fácil de navegar y modificar
- ✅ Separación clara de responsabilidades
- ✅ Reutilización de funciones compartidas
- ✅ Testing más eficiente por módulos

### **Para Usuarios:**
- ✅ Navegación más intuitiva
- ✅ Páginas cargan más rápido
- ✅ Mejor organización de la información
- ✅ Experiencia más profesional

### **Para Mantenimiento:**
- ✅ Actualizaciones por módulo sin afectar otros
- ✅ Debugging más eficiente
- ✅ Escalabilidad mejorada
- ✅ Documentación más clara

## 🚀 Próximos Pasos

1. **Probar la nueva estructura** con `streamlit run main.py`
2. **Verificar todas las funcionalidades** en cada página
3. **Actualizar documentación** si es necesario
4. **Optimizar performance** de carga de páginas

**🎯 La aplicación mantiene toda la funcionalidad original pero con una arquitectura mucho más profesional y mantenible.**
