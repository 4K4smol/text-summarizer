# text-summarizer-api/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 1) Copiamos solo lo necesario para instalar deps
COPY requirements-workers.txt .

RUN pip install --no-cache-dir -r requirements-workers.txt

# 2) Copiamos el resto del código (el .env está en .dockerignore)
COPY . .

# Variables por defecto (se sobrescriben con las de Render)
ENV BACKEND=workers \
    PORT=8080

EXPOSE 8080

# Arranca uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "2"]
