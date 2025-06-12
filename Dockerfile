FROM python:3.11-slim

ARG BACKEND=workers          # valor por defecto en Render
ENV BACKEND=${BACKEND}
ENV PORT=8080

# solo aplica si BACKEND=hf, pero no estorba en workers
ENV HF_HOME=/models

WORKDIR /code

# Copiamos ambos requirements
COPY requirements*.txt ./

# Instalamos el que corresponda
RUN if [ "$BACKEND" = "hf" ]; \
      then pip install --no-cache-dir -r requirements.txt ; \
      else pip install --no-cache-dir -r requirements-workers.txt ; \
    fi

COPY app/ app/

CMD ["uvicorn", "app.main:api", "--host", "0.0.0.0", "--port", "8080", "--workers", "2"]
