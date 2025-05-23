import sqlite3
import json
from datetime import datetime
import os
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional

load_dotenv()

class Database:
    def __init__(self):
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
                created_at TEXT
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
                created_at TEXT
            )
        ''')
        
        self.conn.commit()

    def add_dream(self, user_id: str, date: str, dream_text: str, 
                 sleep_quality: int, mood: str = None, tags: str = None) -> int:
        """
        Ajoute un rêve à la base de données
        
        Args:
            user_id: ID de l'utilisateur
            date: Date du rêve (format YYYY-MM-DD)
            dream_text: Texte du rêve
            sleep_quality: Qualité du sommeil (1-5)
            mood: Humeur de l'utilisateur
            tags: Tags du rêve (séparés par des virgules)
            
        Returns:
            int: ID du rêve créé
        """
        created_at = datetime.now().isoformat()
        
        self.cursor.execute('''
            INSERT INTO dreams 
            (user_id, date, dream_text, sleep_quality, mood, tags, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, date, dream_text, sleep_quality, mood, tags, created_at))
        
        self.conn.commit()
        return self.cursor.lastrowid

    def get_dreams(self, user_id: str = None):
        """
        Récupère les rêves d'un utilisateur
        
        Args:
            user_id: ID de l'utilisateur (optionnel, tous les rêves si None)
            
        Returns:
            list: Liste des rêves
        """
        if user_id:
            self.cursor.execute('''
                SELECT * FROM dreams 
                WHERE user_id = ? 
                ORDER BY date DESC
            ''', (user_id,))
        else:
            self.cursor.execute('''
                SELECT * FROM dreams 
                ORDER BY date DESC
            ''')
        return self.cursor.fetchall()

    def update_dream(self, dream_id: int, dream_text: str = None, 
                    sleep_quality: int = None, mood: str = None, tags: str = None):
        """
        Met à jour un rêve existant
        
        Args:
            dream_id: ID du rêve à mettre à jour
            dream_text: Nouveau texte du rêve
            sleep_quality: Nouvelle qualité de sommeil
            mood: Nouvelle humeur
            tags: Nouveaux tags
        """
        # Récupérer les valeurs actuelles
        self.cursor.execute('SELECT * FROM dreams WHERE id = ?', (dream_id,))
        dream = self.cursor.fetchone()
        
        if not dream:
            raise ValueError(f"Aucun rêve trouvé avec l'ID {dream_id}")
        
        # Préparer les mises à jour
        updates = []
        params = []
        
        if dream_text is not None:
            updates.append("dream_text = ?")
            params.append(dream_text)
            
        if sleep_quality is not None:
            updates.append("sleep_quality = ?")
            params.append(sleep_quality)
            
        if mood is not None:
            updates.append("mood = ?")
            params.append(mood)
            
        if tags is not None:
            updates.append("tags = ?")
            params.append(tags)
        
        if not updates:
            return  # Aucune mise à jour nécessaire
            
        # Construire et exécuter la requête
        query = f"""
            UPDATE dreams 
            SET {', '.join(updates)}
            WHERE id = ?
        """
        params.append(dream_id)
        
        self.cursor.execute(query, params)
        self.conn.commit()

    def add_analysis(self, user_id: str, analysis_date: str, themes: str, emotions: str = "") -> int:
        """
        Ajoute une analyse à la base de données
        
        Args:
            user_id: ID de l'utilisateur
            analysis_date: Date de l'analyse (format YYYY-MM-DD)
            themes: Thèmes détectés
            emotions: Émotions détectées
            
        Returns:
            int: ID de l'analyse créée
        """
        created_at = datetime.now().isoformat()
        
        self.cursor.execute('''
            INSERT INTO analyses 
            (user_id, analysis_date, themes, emotions, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, analysis_date, themes, emotions, created_at))
        
        self.conn.commit()
        return self.cursor.lastrowid

    def get_analyses(self, user_id: str = None):
        """
        Récupère les analyses
        
        Args:
            user_id: ID de l'utilisateur (optionnel, toutes les analyses si None)
            
        Returns:
            list: Liste des analyses
        """
        if user_id:
            self.cursor.execute('''
                SELECT * FROM analyses 
                WHERE user_id = ? 
                ORDER BY analysis_date DESC
            ''', (user_id,))
        else:
            self.cursor.execute('''
                SELECT * FROM analyses 
                ORDER BY analysis_date DESC
            ''')
        return self.cursor.fetchall()

    def close(self):
        """Ferme la connexion à la base de données"""
        if self.conn:
            self.conn.close()

# Instance unique de la base de données
db = Database()
