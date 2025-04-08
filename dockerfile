FROM python:3.10-slim

WORKDIR /app

# Copier le fichier requirements.txt depuis src
COPY src/requirements.txt ./src/requirements.txt

# Installer les dépendances
RUN pip install --upgrade pip && pip install -r /app/src/requirements.txt

# Copier tout le code source dans le container
COPY src/ ./src

# Installer dataprediction en mode "editable"
RUN pip install -e ./src

# Définir le répertoire de travail dans /app/
WORKDIR /app/

# Exposer le port de l'API FastAPI
EXPOSE 8080

# Lancer l'API FastAPI avec uvicorn
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8080"]
