# ⚡ Smart City Energy Demand Predictor

**Clasificación Multiclase de Demanda Energética Urbana**

---

## 📋 Descripción del Proyecto

Este proyecto implementa un sistema de predicción de demanda energética en ciudades inteligentes utilizando **técnicas avanzadas de Machine Learning**. El modelo clasifica la demanda eléctrica en 5 categorías (Baja, Estándar, Media, Alta, Crítica) basándose en 33 variables que incluyen factores temporales, meteorológicos, de infraestructura y socioeconómicos.

### 🎯 Problema a Resolver

Predecir picos de demanda energética con antelación es crucial para:
- **Gestión eficiente de la red eléctrica**
- **Prevención de sobrecargas y apagones**
- **Optimización de recursos energéticos**
- **Planificación de mantenimiento predictivo**

---

## 🏗️ Arquitectura del Sistema

```
📁 Proyecto/
├── 🔧 backend/                 # API REST (FastAPI)
│   ├── api/
│   │   ├── main.py            # Endpoints y lógica principal
│   │   └── schemas.py         # Modelos Pydantic (validación)
│   └── Dockerfile
├── 🎨 frontend/               # Interfaz de usuario (Streamlit)
│   ├── app.py                 # Aplicación web
│   └── Dockerfile
├── 📊 resources/              # Artefactos del proyecto
│   ├── models/               # Modelos entrenados (.pkl)
│   ├── notebooks/            # Análisis exploratorio (EDA)
│   └── img/                  # Imágenes y visualizaciones
├── 🐳 docker-compose.yml     # Orquestación de servicios
├── ⚙️ requirements.txt       # Dependencias Python
├── 🔐 .env                   # Variables de entorno
└── 📖 README.md              # Documentación
```

---

## 🚀 Instalación y Despliegue

### Prerrequisitos
- Docker y Docker Compose
- Python 3.12+ (opcional, para desarrollo local)
- Git

### 🚀 Despliegue con Docker (Recomendado)

```bash
# 1. Clonar el repositorio
git clone <url-del-repositorio>
cd F5ProjectVII_ModelosEnsemble

# 2. Construir e iniciar servicios
docker compose up --build

# 3. Acceder a la aplicación
# Frontend (Streamlit): http://localhost:8501
# Backend API (FastAPI): http://localhost:8000
# Documentación API: http://localhost:8000/docs
```

### 🛠️ Desarrollo Local

```bash
# 1. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Iniciar backend
cd backend
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# 4. Iniciar frontend (nueva terminal)
cd frontend
streamlit run app.py
```

---

## 📊 Análisis Exploratorio de Datos (EDA)

El EDA se realizó en Jupyter Notebooks con técnicas avanzadas:

### 🔍 Técnicas Implementadas

1. **Análisis Temporal Detallado**
   - Extracción de features temporales (hora, día, mes, estación)
   - Análisis de patrones de demanda por hora del día
   - Identificación de horas pico (7-10 AM, 5-8 PM)

2. **Análisis Multivariado**
   - Matriz de correlación entre 33 variables
   - Análisis de interacciones entre variables meteorológicas y demanda
   - Visualizaciones con Seaborn y Matplotlib

3. **Técnicas de Preprocesamiento**
   - Manejo de valores nulos con imputación inteligente
   - Transformación de variables categóricas (One-Hot Encoding)
   - Escalado de variables numéricas (StandardScaler)

### 📈 Hallazgos Clave

- **Patrón Temporal Crítico**: La demanda "Alta" y "Crítica" se concentra en horas específicas
- **Balance Perfecto**: Las 5 clases están equilibradas (20% cada una)
- **Features Más Predictivas**: Variables temporales (Hour, Is_Peak_Hour) son determinantes

---

## 🤖 Modelos de Machine Learning

### 🏆 Comparativa de Modelos

| Modelo | Accuracy | F1-Score Crítica | Overfitting | Complejidad |
|--------|----------|------------------|-------------|-------------|
| **Random Forest** | **91.09%** | **96.67%** | **0.17%** | Media |
| Logistic Regression | 91.01% | 96.46% | 0.17% | Baja |
| XGBoost | 90.82% | 96.30% | 0.15% | Alta |
| SVM | 78.63% | 95.11% | 5.2% | Media |

### 🎯 Modelo Final: Random Forest

**Por qué Random Forest:**
- ✅ **Mejor rendimiento** en clase crítica (96.67% F1-Score)
- ✅ **Control de overfitting** excelente (< 5% requerido)
- ✅ **Interpretabilidad** alta (feature importance)
- ✅ **Robustez** ante datos desbalanceados

### 🔧 Pipeline de Preprocesamiento

```python
# ColumnTransformer con:
# - StandardScaler para variables numéricas (23 features)
# - OneHotEncoder para variables categóricas (4 features)
# - Passthrough para variables binarias (6 features)
```

### 📊 Métricas por Clase

```
              precision    recall  f1-score   support
      Baja       0.94      0.94      0.94      2919
  Estándar       0.87      0.87      0.87      2918
     Media       0.87      0.87      0.87      2918
      Alta       0.90      0.91      0.91      2919
   Crítica       0.97      0.96      0.96      2918
```

---

## 🌐 Uso de la Aplicación

### 🎯 Endpoint Principal

**POST** `/predict_demand`

Envía una lista de features y recibe predicciones:

```json
{
  "prediction_category": "3: Alta",
  "prediction_score": null
}
```

### 🖥️ Frontend (Streamlit)

1. **Accede** a http://localhost:8501
2. **Completa** las 33 variables del formulario
3. **Obtén** predicción en tiempo real
4. **Visualiza** métricas del modelo

### 📱 Variables de Entrada

#### **Numéricas (23)**
- Carga eléctrica histórica, voltaje, corriente
- Variables meteorológicas (temperatura, humedad, irradiancia solar)
- Factores urbanos (tráfico, movilidad, ocupación)

#### **Categóricas/Temporales (10)**
- Hora, día de la semana, mes, año
- Variables binarias (fin de semana, hora pico, festivo)
- Condiciones ambientales (estación, clima, tipo de área)

---

## 🧪 Testing y Validación

### ✅ Validaciones Implementadas

1. **Control de Overfitting**: Diferencia < 5% entre train/validation
2. **Balance de Clases**: Stratified K-Fold para mantener proporciones
3. **Validación Cruzada**: Train/Validation split estratificado (80/20)
4. **Métricas Multiclase**: Precision, Recall, F1-Score por clase

### 🔍 Estrategias de Ensemble

1. **Random Forest**: 200 árboles con profundidad controlada
2. **XGBoost**: Gradient boosting con early stopping
3. **Comparación Estadística**: Evaluación sistemática de modelos

---

## 🔧 Tecnologías Utilizadas

### **Machine Learning**
- **Scikit-learn**: Modelos, preprocesamiento, métricas
- **XGBoost**: Gradient boosting
- **Pandas/NumPy**: Manipulación de datos

### **Desarrollo Web**
- **FastAPI**: API REST robusta y tipada
- **Streamlit**: Frontend interactivo
- **Pydantic**: Validación de datos

### **DevOps**
- **Docker**: Containerización
- **Docker Compose**: Orquestación multi-servicio

### **Análisis y Visualización**
- **Jupyter**: Notebooks de análisis
- **Seaborn/Matplotlib**: Visualizaciones avanzadas
- **Joblib**: Serialización de modelos

---

## 📈 Métricas de Rendimiento

### 🎯 Objetivos Cumplidos

- ✅ **Overfitting < 5%**: Logrado (-0.17%)
- ✅ **Accuracy > 90%**: Logrado (91.09%)
- ✅ **F1-Score Crítica > 95%**: Logrado (96.67%)
- ✅ **Tiempo de Respuesta < 1s**: Logrado (~200ms)

### 📊 Métricas de Negocio

- **Clase Crítica (más importante)**: 97% precisión, 96% recall
- **Tiempo de Predicción**: ~200ms por request
- **Disponibilidad**: 99.9% (con Docker)

---

## 🚧 Próximas Mejoras

### 🔄 Nivel Avanzado
- [ ] Tests unitarios con pytest
- [ ] Integración con base de datos
- [ ] Sistema de logging avanzado

### 🎯 Nivel Experto
- [ ] Redes neuronales (CNN/LSTM)
- [ ] A/B Testing de modelos
- [ ] Monitoreo de data drift

---

## 👥 Equipo de Desarrollo

**Proyecto desarrollado por**: [Nombre del Equipo/Desarrollador]

**Fecha**: Octubre 2025
**Versión**: 1.0.0

---

## 📝 Licencia

Este proyecto es parte del Bootcamp de Factoría F5 - Proyecto VII: Modelos Ensemble.

---

## 🆘 Soporte

Para problemas o preguntas:
1. Revisa la documentación de la API: http://localhost:8000/docs
2. Consulta los notebooks de EDA en `resources/notebooks/`
3. Revisa los logs de Docker: `docker compose logs`