# Dockerfile para la aplicación ECS Demo con Flask
FROM python:3.13-alpine

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements
COPY app/requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY app/ .

# Exponer puerto
EXPOSE 8080

# Variables de entorno por defecto
ENV PORT=8080
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=main.py

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')"

# Comando para ejecutar la aplicación con Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "4", "--timeout", "60", "main:app"]
