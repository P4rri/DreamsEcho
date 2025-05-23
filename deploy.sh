#!/bin/bash

# Mise à jour des paquets système
apt-get update && apt-get install -y ffmpeg

# Création du dossier de configuration Streamlit
mkdir -p ~/.streamlit/

# Configuration Streamlit
echo "[server]\n\
headless = true\n\
port = \$PORT\n\
enableCORS = false\n\
\n[browser]\n\
serverAddress = \"0.0.0.0\"\n\
serverPort = \$PORT" > ~/.streamlit/config.toml

# Installation des dépendances Python
pip install -r requirements.txt

# Téléchargement des modèles NLTK
python -c "import nltk; nltk.download('punkt')"

# Initialisation de la base de données
python -c "from database import db; db.initialize_db()"

# Lancement de l'application Streamlit
streamlit run app.py
