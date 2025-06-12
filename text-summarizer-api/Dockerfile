FROM python:3.11-slim

WORKDIR /app
COPY requirements-workers.txt .
RUN pip install --no-cache-dir -r requirements-workers.txt

COPY . .

# En Render Free trabaja en 512 MB, solo backends I/O-bound
ENV BACKEND=workers
ENV PORT=8080

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "2"]
