FROM python:3.9-slim

RUN useradd -m -u 1000 appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install development dependencies
RUN pip install --no-cache-dir watchdog
RUN apt-get update && apt-get install -y kafkacat

COPY ./backend /app/backend

RUN chown -R appuser:appuser /app

USER appuser

# Update this line
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]