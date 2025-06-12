FROM python:3.11-slim

ARG BACKEND=workers        # valor por defecto
ENV BACKEND=${BACKEND}
ENV PORT=8080
ENV HF_HOME=/models        # no hace nada en workers

WORKDIR /code

# Copiamos los dos requirements
COPY requirements*.txt ./

# Instalamos el apropiado
RUN if [ "$BACKEND" = "hf" ]; \
      then pip install --no-cache-dir -r requirements.txt ; \
      else pip install --no-cache-dir -r requirements-workers.txt ; \
    fi

COPY app/ app/
CMD ["uvicorn", "app.main:api", "--host", "0.0.0.0", "--port", "8080", "--workers", "2"]
