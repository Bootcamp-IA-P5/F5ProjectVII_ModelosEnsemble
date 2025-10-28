# CÓDIGO: frontend/Dockerfile
FROM python:3.12-slim

# Instalar curl para debugging
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar el archivo de requisitos DESDE LA RAÍZ (el compose lo gestiona)
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copiar toda la aplicación frontend modular
COPY frontend/ .

# Streamlit corre por defecto en el puerto 8501
EXPOSE 8501

# Comando de arranque de Streamlit con el nuevo main.py
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]