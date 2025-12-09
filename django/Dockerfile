# Image Python officielle
FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Définit le répertoire de travail dans le container
WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copie les requirements d'abord (optimisation du cache Docker)
COPY requirements.txt .

# Installe les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Port exposé par Django
# EXPOSE 8000

WORKDIR /app/code/pointageProject

# Commande de démarrage
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]