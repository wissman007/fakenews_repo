# Utiliser l'image officielle Python
FROM python:3.9

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires
COPY api/app.py requirements.txt /app/
COPY dataprediction /app/dataprediction/

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port 8000 pour FastAPI
EXPOSE 8000

# Lancer l'API avec Uvicorn
CMD ["uvicorn", "api/app:app", "--host", "0.0.0.0", "--port", "8000"]
