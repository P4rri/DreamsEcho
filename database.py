import sqlite3
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    _instance = None
    
    def __new__(cls, db_name='dreamsecho.db'):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance
        
    def __init__(self, db_name=None):
        if not hasattr(self, 'initialized') or not self.initialized:
            self.db_name = db_name or os.getenv('DB_NAME', 'dreamsecho.db')
            self.conn = None
            self.cursor = None
            self.initialize_db()
            self.initialized = True

    def initialize_db(self):
        """Initialise la base de données et crée les tables si elles n'existent pas"""
        try:
            self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
            self.cursor = self.conn.cursor()
            
            # Activer les clés étrangères
            self.cursor.execute('PRAGMA foreign_keys = ON')
            
            # Création de la table des rêves
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS dreams (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    date TEXT,
                    dream_text TEXT,
                    sleep_quality INTEGER DEFAULT 5,
                    mood TEXT DEFAULT 'neutre',
                    tags TEXT,
                    created_at TEXT,
                    updated_at TEXT
                )
            ''')
            
            # Création de la table des analyses
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS analyses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dream_id INTEGER,
                    analysis_date TEXT,
                    themes TEXT,
                    emotions TEXT,
                    created_at TEXT,
                    updated_at TEXT,
                    FOREIGN KEY (dream_id) REFERENCES dreams (id) ON DELETE CASCADE
                )
            ''')
            
            self.conn.commit()
            print("Base de données initialisée avec succès")
            
        except Exception as e:
            print(f"Erreur lors de l'initialisation de la base de données: {str(e)}")
            raise

    def add_dream(self, user_id, date, dream_text, sleep_quality=5, mood='neutre', tags=None):
        """Ajoute un nouveau rêve à la base de données"""
        try:
            current_time = datetime.now().isoformat()
            self.cursor.execute('''
                INSERT INTO dreams (user_id, date, dream_text, sleep_quality, mood, tags, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (str(user_id), date, dream_text, sleep_quality, mood, tags, current_time, current_time))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Erreur lors de l'ajout d'un rêve: {str(e)}")
            self.conn.rollback()
            raise

    def get_dreams(self, user_id=None):
        """Récupère tous les rêves ou ceux d'un utilisateur spécifique"""
        try:
            if user_id:
                self.cursor.execute('SELECT * FROM dreams WHERE user_id = ? ORDER BY date DESC', (str(user_id),))
            else:
                self.cursor.execute('SELECT * FROM dreams ORDER BY date DESC')
            return self.cursor.fetchall() or []  # Retourne une liste vide si aucun résultat
        except Exception as e:
            print(f"Erreur lors de la récupération des rêves: {str(e)}")
            return []

    def close(self):
        """Ferme la connexion à la base de données"""
        try:
            if self.conn:
                self.conn.close()
                self.conn = None
                self.cursor = None
        except Exception as e:
            print(f"Erreur lors de la fermeture de la base de données: {str(e)}")

# Instance unique de la base de données
db = Database()
