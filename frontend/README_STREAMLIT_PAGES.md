# 🚀 Frontend Nativo de Streamlit - Smart City Energy Predictor

## 📁 Estructura Nativa de Páginas de Streamlit

El frontend ha sido completamente reestructurado utilizando la **estructura nativa de páginas de Streamlit**, que es la forma más limpia y recomendada de crear aplicaciones multipágina.

```
frontend/
├── main.py                    # 🏠 Página principal (Inicio)
├── pages/
│   ├── 01_🏠_Home.py         # Dashboard y métricas principales
│   ├── 02_🔮_Prediction.py   # Formulario de predicción
│   ├── 03_📊_EDA.py          # Análisis exploratorio de datos
│   ├── 04_🤖_Models.py       # Modelos y técnicas de ensemble
│   └── 05_📋_Documentation.py # Documentación técnica completa
├── utils.py                   # 🔧 Funciones compartidas
├── __init__.py               # 📦 Paquete Python
└── Dockerfile               # 🐳 Containerización
```

## 🎯 Características de la Estructura Nativa

### ✅ **Navegación Automática**
- Streamlit detecta automáticamente todos los archivos en `/pages`
- Los números al inicio (01_, 02_, etc.) definen el orden en el sidebar
- Los emojis en el nombre aparecen en la navegación
- **Sin código de routing personalizado necesario**

### ✅ **URLs Limpias**
- Cada página tiene su propia URL: `/pages/Nombre_Página`
- Navegación intuitiva con el sidebar izquierdo
- Estado de página preservado automáticamente

### ✅ **Independencia de Páginas**
- Cada página es un archivo Python independiente
- Configuración de página individual (título, icono, layout)
- Imports y dependencias por página

## 🚀 Cómo Funciona

### **1. Detección Automática**
```python
# Streamlit busca automáticamente en /pages
# Los archivos deben seguir el patrón: NÚMERO_EMOJI_NOMBRE.py
01_🏠_Home.py        # → Aparece primero en el sidebar
02_🔮_Prediction.py  # → Aparece segundo
03_📊_EDA.py         # → Aparece tercero
# etc...
```

### **2. Navegación en Sidebar**
Streamlit genera automáticamente:
```
📱 Sidebar
├── 🏠 Inicio
├── 🔮 Predicción
├── 📊 EDA & Análisis
├── 🤖 Modelos & Ensemble
└── 📋 Documentación
```

### **3. Funciones Principales**
Cada página debe tener una función `main()`:
```python
def main():
    st.set_page_config(page_title="Título", page_icon="🔮")
    # Contenido de la página
    st.header("Mi Página")
    # ...

if __name__ == "__main__":
    main()
```

## 📋 Páginas Disponibles

### **🏠 01_🏠_Home.py - Dashboard Principal**
- Métricas principales del sistema
- Introducción al proyecto
- Estado del backend
- Navegación general

### **🔮 02_🔮_Prediction.py - Predicción en Tiempo Real**
- Formulario con 10 variables principales
- Escenarios de demostración (5 categorías)
- Validación y envío de predicciones
- Variables automáticas generadas por IA

### **📊 03_📊_EDA.py - Análisis Exploratorio**
- Visualizaciones del dataset (72,960 registros)
- Distribución temporal por horas
- Feature importance con gráficos
- Análisis de balance de clases

### **🤖 04_🤖_Models.py - Modelos & Ensemble**
- Comparativa de 5 modelos implementados
- Métricas detalladas por clase
- GridSearchCV y StratifiedKFold documentados
- Pipeline de preprocesamiento

### **📋 05_📋_Documentation.py - Documentación**
- Guía técnica completa
- Arquitectura del sistema
- Troubleshooting y recursos
- Métricas de rendimiento

## 🔧 Funciones Compartidas (utils.py)

### **Configuración Global:**
- `get_backend_url()` - Detección automática de Docker
- `test_backend_connection()` - Verificación de conectividad
- `get_model_metrics()` - Métricas del modelo

### **Funciones de Predicción:**
- `generate_default_values()` - 23 variables automáticas
- `create_scenario_data()` - Escenarios predefinidos
- `make_prediction()` - Envío al backend

### **Estilos CSS:**
- `get_css_styles()` - Estilos compartidos

## 🚀 Cómo Ejecutar

### **Desarrollo Local:**
```bash
cd frontend
streamlit run main.py

# Streamlit detectará automáticamente las páginas en /pages
# y creará la navegación en el sidebar
```

### **Con Docker:**
```bash
# Ya configurado para la nueva estructura
docker compose up --build

# El Dockerfile copia todo el directorio frontend/
# y Streamlit maneja la navegación automáticamente
```

## 🎨 Mejoras Implementadas

### **✅ Navegación Nativa**
- Sin código de routing personalizado
- URLs limpias y SEO-friendly
- Sidebar automático generado por Streamlit

### **✅ Performance Mejorada**
- Carga más rápida de páginas
- Mejor gestión de memoria
- Sin estado global innecesario

### **✅ Mantenibilidad**
- Estructura estándar de la comunidad
- Fácil agregar nuevas páginas
- Código más limpio y organizado

### **✅ Compatibilidad**
- Compatible con todas las versiones de Streamlit
- Funciona en desarrollo y producción
- Integración perfecta con Docker

## 🔄 Migración desde la Estructura Anterior

### **Cambios Realizados:**
1. **Estructura modular** → **Estructura nativa de Streamlit**
2. **Navegación personalizada** → **Navegación automática**
3. **Imports complejos** → **Imports por página**
4. **Funciones placeholder** → **Funciones independientes**

### **Ventajas de la Nueva Estructura:**
- ✅ **Más simple**: Sin código de routing
- ✅ **Más rápido**: Mejor performance
- ✅ **Más estándar**: Patrón oficial de Streamlit
- ✅ **Más mantenible**: Estructura clara
- ✅ **Más escalable**: Fácil agregar páginas

## 🐳 Docker

El Dockerfile está actualizado:
```dockerfile
# Copia todo el directorio frontend
COPY frontend/ .

# Streamlit detectará automáticamente /pages
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🎯 Resultado Final

**🏆 Estructura Profesional y Nativa de Streamlit**

- ✅ **Navegación automática** en el sidebar
- ✅ **5 páginas funcionales** con contenido completo
- ✅ **URLs limpias** y amigables
- ✅ **Performance optimizada** con la estructura nativa
- ✅ **Código limpio** sin routing personalizado
- ✅ **Estándar de la comunidad** seguido

**🎉 La aplicación ahora utiliza la mejor práctica de Streamlit para múltiples páginas, resultando en una experiencia más profesional, mantenible y escalable.**
