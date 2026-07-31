# ---- Etapa 1: construir dependencias y descargar el modelo ----

FROM python:3.11-slim AS builder



WORKDIR /app



RUN apt-get update && apt-get install -y --no-install-recommends \

    gcc \

    libpq-dev \

    curl \

    && rm -rf /var/lib/apt/lists/*



# Entorno virtual aislado, evita el problema de instalar como root en /root/.local

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"



COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt



# Descargar el modelo entrenado (63MB) desde GitHub Releases

RUN curl -L -o rf_model.pkl https://github.com/sauzuniga/GameVisionIA/releases/download/model-v1.0.0/rf_model.pkl



# ---- Etapa 2: imagen final, más liviana ----

FROM python:3.11-slim



WORKDIR /app



RUN apt-get update && apt-get install -y --no-install-recommends \

    libpq5 \

    && rm -rf /var/lib/apt/lists/*



# Logs de uvicorn en tiempo real, sin archivos .pyc innecesarios

ENV PYTHONUNBUFFERED=1

ENV PYTHONDONTWRITEBYTECODE=1



# Usuario sin privilegios, en vez de correr la app como root

RUN useradd --create-home --shell /bin/bash appuser



# Copiar el entorno virtual ya armado desde la etapa anterior

COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"



# Copiar el modelo ya descargado

COPY --from=builder /app/rf_model.pkl .



# Copiar el código de la aplicación

COPY . .



# Ceder la propiedad de los archivos al usuario sin privilegios

RUN chown -R appuser:appuser /app



USER appuser



EXPOSE 8000



CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"] 