import sqlite3
from datetime import datetime
from dotenv import load_dotenv
import os

class DreamManager:
    def __init__(self):
        load_dotenv()
        self.db_name = os.getenv('DB_NAME', 'dreamsecho.db')
        self.conn = None
        self.cursor = None
        self.initialize_db()

    def initialize_db(self):
        """Initialise la base de données"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        
        # Création de la table des rêves
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS dreams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                date TEXT,
                dream_text TEXT,
                sleep_quality INTEGER,
                mood TEXT,
                tags TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        
        # Création de la table des analyses
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                analysis_date TEXT,
                themes TEXT,
                emotions TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        
        self.conn.commit()

    def add_dream(self, user_id, date, dream_text, sleep_quality, mood=None, tags=None):
        """Ajoute un rêve à la base de données"""
        current_time = datetime.now().isoformat()
        self.cursor.execute('''
            INSERT INTO dreams (user_id, date, dream_text, sleep_quality, mood, tags, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, date, dream_text, sleep_quality, mood, tags, current_time, current_time))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_dream(self, dream_id, **kwargs):
        """Met à jour un rêve existant"""
        update_fields = []
        params = []
        
        for key, value in kwargs.items():
            if key in ['dream_text', 'sleep_quality', 'mood', 'tags']:
                update_fields.append(f"{key} = ?")
                params.append(value)
        
        if not update_fields:
            return False
        
        params.append(dream_id)
        update_fields.append("updated_at = ?")
        params.append(datetime.now().isoformat())
        
        query = f"UPDATE dreams SET {', '.join(update_fields)} WHERE id = ?"
        self.cursor.execute(query, params)
        self.conn.commit()
        return True

    def get_dreams(self, user_id=None, date=None, limit=100):
        """Récupère les rêves selon les critères"""
        query = "SELECT * FROM dreams WHERE 1=1"
        params = []
        
        if user_id:
            query += " AND user_id = ?"
            params.append(user_id)
        if date:
            query += " AND date = ?"
            params.append(date)
        
        query += " ORDER BY date DESC LIMIT ?"
        params.append(limit)
        
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def get_dream_by_id(self, dream_id):
        """Récupère un rêve spécifique par son ID"""
        self.cursor.execute('SELECT * FROM dreams WHERE id = ?', (dream_id,))
        return self.cursor.fetchone()

    def delete_dream(self, dream_id):
        """Supprime un rêve"""
        self.cursor.execute('DELETE FROM dreams WHERE id = ?', (dream_id,))
        self.conn.commit()
        return True

    def add_analysis(self, user_id, analysis_date, themes, emotions):
        """Ajoute une analyse à la base de données"""
        current_time = datetime.now().isoformat()
        self.cursor.execute('''
            INSERT INTO analyses (user_id, analysis_date, themes, emotions, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, analysis_date, themes, emotions, current_time, current_time))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_analyses(self, user_id=None, limit=100):
        """Récupère les analyses selon les critères"""
        query = "SELECT * FROM analyses WHERE 1=1"
        params = []
        
        if user_id:
            query += " AND user_id = ?"
            params.append(user_id)
        
        query += " ORDER BY analysis_date DESC LIMIT ?"
        params.append(limit)
        
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        """Ferme la connexion à la base de données"""
        if self.conn:
            self.conn.close()

# Instance unique du gestionnaire de rêves
dream_manager = DreamManager()
