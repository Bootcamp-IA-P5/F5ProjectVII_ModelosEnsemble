# CÓDIGO: frontend/Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Copiar el archivo de requisitos DESDE LA RAÍZ (el compose lo gestiona)
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copiar la aplicación
COPY frontend/app.py .

# Streamlit corre por defecto en el puerto 8501
EXPOSE 8501

# Comando de arranque de Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]