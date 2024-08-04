FROM python:3.9-slim

RUN useradd -m -u 1000 appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install development dependencies
RUN pip install --no-cache-dir watchdog

COPY ./app /app/app

RUN chown -R appuser:appuser /app

USER appuser

# Remove the CMD instruction as we're now using the command in docker-compose.yml
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]