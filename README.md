# Patch 1 - Fichiers Essentiels

Ce dossier contient tous les fichiers nécessaires au bon fonctionnement de l'application DreamsEcho.

## Fichiers inclus :

1. `app.py` - L'application principale Streamlit
2. `database.py` - Gestion de la base de données
3. `dream_manager.py` - Logique métier de l'application
4. `requirements.txt` - Dépendances Python nécessaires
5. `deploy.sh` - Script de déploiement pour Render
6. `runtime.txt` - Version de Python requise
7. `.env.example` - Exemple de fichier de configuration

## Instructions d'installation :

1. Copiez ces fichiers à la racine de votre projet
2. Renommez `.env.example` en `.env` et configurez vos variables d'environnement
3. Exécutez `pip install -r requirements.txt` pour installer les dépendances
4. Pour le déploiement, suivez les instructions dans `deploy.sh`
