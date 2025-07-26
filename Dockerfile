# Backend Dockerfile (FastAPI) - Production Ready
FROM python:3.11-slim as builder

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage de production
FROM python:3.11-slim

WORKDIR /app

# Créer un utilisateur non-root
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copier les dépendances installées
COPY --from=builder /root/.local /home/appuser/.local

# Copier le code de l'application
COPY . .

# Changer les permissions
RUN chown -R appuser:appuser /app

# Passer à l'utilisateur non-root
USER appuser

# Ajouter le répertoire local au PATH
ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 