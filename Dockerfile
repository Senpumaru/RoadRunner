FROM python:3.12-slim

RUN useradd -m -u 1000 appuser

WORKDIR /project

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install development dependencies
RUN pip install --no-cache-dir watchdog
RUN apt-get update && apt-get install -y kafkacat

COPY ./ /project

RUN chown -R appuser:appuser /project

USER appuser

# Update this line
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]