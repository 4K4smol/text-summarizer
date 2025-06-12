FROM python:3.11-slim
ENV HF_HOME=/models
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/ app/
CMD ["uvicorn", "app.main:api", "--host", "0.0.0.0", "--port", "8080", "--workers", "2"]
