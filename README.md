# 🌙 DreamsEcho - Votre Compagnon d'Exploration des Rêves

**Transformez vos rêves en expériences visuelles et auditives uniques avec l'IA**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 🌟 Présentation

DreamsEcho est une application innovante qui utilise l'intelligence artificielle pour analyser vos rêves et les transformer en expériences multimédias uniques. Enregistrez vos rêves, découvrez leurs significations cachées, et laissez l'IA créer des vidéos artistiques basées sur vos expériences oniriques.

## ✨ Fonctionnalités Principales

### 📝 Journal des Rêves
- Interface intuitive pour enregistrer et organiser vos rêves
- Suivi de la qualité du sommeil et des émotions
- Système de tags et de catégories

### 🧠 Analyse Avancée par IA
- Détection automatique des thèmes et symboles récurrents
- Analyse des émotions et du sentiment global
- Identification des motifs et tendances sur le long terme

### 🎨 Création de Contenu
- Génération d'images uniques avec DALL-E 3
- Création de vidéos personnalisées
- Musique d'ambiance générée en fonction de l'analyse émotionnelle

### 📊 Tableaux de Bord et Rapports
- Visualisation des données de sommeil
- Historique des rêves et analyses
- Export des données et créations

## 🚀 Déploiement sur Render.com

1. **Créer un nouveau service Web** sur [Render Dashboard](https://dashboard.render.com/)
2. **Configurer le service** :
   - Runtime: Python 3
   - Build Command: `chmod a+x deploy.sh && ./deploy.sh`
   - Start Command: `bash deploy.sh`
3. **Variables d'environnement** :
   - `OPENAI_API_KEY` : Votre clé API OpenAI
   - `PORT` : Laissé vide (sera défini par Render)
4. **Déployer**

## 🛠️ Installation

### Prérequis
- Windows 10 ou supérieur
- Python 3.8 ou supérieur (sera installé automatiquement si nécessaire)
- Connexion Internet pour le téléchargement des dépendances
- Droits d'administrateur pour l'installation

### Installation Automatique (Recommandé pour Windows)

1. **Télécharger l'archive**
   - Téléchargez l'archive de l'application
   - Extrayez le contenu dans un dossier de votre choix

2. **Exécuter l'installation**
   - Faites un clic droit sur `Install_DreamsEcho.bat`
   - Sélectionnez "Exécuter en tant qu'administrateur"
   - Suivez les instructions à l'écran
   - L'installation peut prendre plusieurs minutes selon votre connexion Internet

3. **Démarrer l'application**
   - Double-cliquez sur `start_app.bat`
   - L'application devrait s'ouvrir automatiquement dans votre navigateur
   - Si ce n'est pas le cas, ouvrez votre navigateur et allez à l'adresse : http://localhost:8501

### Installation Manuelle (Pour utilisateurs avancés)

1. **Installer Python**
   - Téléchargez Python depuis https://www.python.org/downloads/
   - **Important** : Cochez "Add Python to PATH" lors de l'installation

2. **Ouvrir un terminal**
   - Appuyez sur `Win + X` et sélectionnez "Terminal" ou "PowerShell"
   - Naviguez jusqu'au dossier de l'application :
   ```bash
   cd chemin\vers\le\dossier\de\l'application
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer les variables d'environnement**
   Créez un fichier `.env` à la racine du projet :
   ```
   OPENAI_API_KEY=votre_clé_api_openai
   DATABASE_URL=sqlite:///dreamsecho.db
   DEBUG=True
   ```

5. **Initialiser la base de données**
   ```bash
   python -c "from database import db; db.initialize_db()"
   ```

## 🖥️ Lancement de l'Application

```bash
streamlit run app.py
```

L'application sera accessible à l'adresse : http://localhost:8501

## 🛠️ Structure du Projet

```
dreamsecho/
├── app.py                 # Point d'entrée de l'application Streamlit
├── database.py            # Gestion de la base de données
├── dream_analyzer.py      # Analyse des rêves avec NLP
├── video_generator.py     # Génération de vidéos
├── requirements.txt       # Dépendances du projet
├── .env.example          # Exemple de configuration
└── README.md             # Ce fichier
```

## 🤖 Technologies Utilisées

### Intelligence Artificielle
- **OpenAI GPT-4** - Analyse sémantique des rêves
- **DALL-E 3** - Génération d'images artistiques
- **Transformers** - Traitement du langage naturel
- **spaCy** - Traitement linguistique avancé

### Développement
- **Python 3.9+** - Langage de programmation principal
- **Streamlit** - Interface utilisateur web
- **SQLAlchemy** - ORM pour la base de données
- **MoviePy** - Traitement vidéo
- **gTTS** - Synthèse vocale

## 📚 Documentation

La documentation complète est disponible dans le dossier `/docs`. Pour la générer localement :

```bash
mkdocs serve
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment contribuer :

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Poussez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📝 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Remerciements

- À l'équipe d'OpenAI pour leurs modèles révolutionnaires
- À la communauté open source pour les nombreuses bibliothèques utilisées
- À tous les testeurs et contributeurs qui améliorent ce projet

## 📧 Contact

Pour toute question ou suggestion, n'hésitez pas à nous contacter à contact@dreamsecho.app

---

Fait avec ❤️ par l'équipe DreamsEcho
