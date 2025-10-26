# Paso 1: Usar una imagen base de Python pequeña y oficial
FROM python:3.12-slim

# Instalar curl para debugging
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Paso 2: Establecer la carpeta de trabajo (el directorio principal dentro del contenedor)
WORKDIR /app

# Paso 3: Copiar y luego instalar las dependencias
# Esto es eficiente: si requirements.txt no cambia, Docker no repite la instalación
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Paso 4: Copiar el modelo entrenado (el artefacto más crítico)
# Usamos un target específico para este archivo, manteniendo el orden
# La ruta de origen (host) es: ../resources/models/
# La ruta de destino (container) es: /app/resources/models/
RUN mkdir -p resources/models
COPY resources/models/model_RandomForest_FINAL.pkl resources/models/

# Paso 5: Copiar el código de la API
# Copiamos todo el contenido de la carpeta 'backend/' en el host a 'backend/' en el container
COPY backend/ backend/

# Paso 6: Exponer el puerto por el que se comunicará el servidor (FastAPI)
EXPOSE 8000

# Paso 7: El comando para ejecutar la aplicación
# Cuando el contenedor se inicie, ejecutará Uvicorn para servir nuestra app.
# 'backend.api.main' es la ruta del archivo, ':app' es el nombre de la variable FastAPI
CMD ["uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "8000"]