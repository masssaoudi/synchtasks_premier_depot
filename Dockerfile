# ============================================================================
# DOCKERFILE DÉFINITIF SYNCHTASKS - PRODUCTION READY
# ============================================================================
FROM python:3.10-slim

# Métadonnées
LABEL maintainer="SyncTasks Team"
LABEL version="1.0.0"
LABEL description="SyncTasks - Application de gestion de tâches intelligente avec IA"

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# Installation des dépendances système
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Création de l'utilisateur non-root
RUN groupadd -r synchtasks && useradd -r -g synchtasks synchtasks

# Création du répertoire de travail
WORKDIR /app

# Copie des fichiers de dépendances
COPY requirements.txt .

# Installation des dépendances Python
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copie du code source (après l'installation des dépendances pour optimiser le cache)
COPY . .

# Création des répertoires nécessaires
RUN mkdir -p /app/logs /app/data /app/static /app/templates

# Changement des permissions
RUN chown -R synchtasks:synchtasks /app
USER synchtasks

# Exposition du port
EXPOSE 8000

# Commande de démarrage
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 