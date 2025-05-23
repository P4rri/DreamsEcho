import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os
from dotenv import load_dotenv
import openai
from PIL import Image
import requests
from io import BytesIO
import json
from dream_manager import dream_manager

# Configuration
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Titre de l'application
st.title("DreamsEcho - Votre Journal de Rêves IA")

# Interface utilisateur
def main():
    st.sidebar.header("Navigation")
    page = st.sidebar.selectbox("Choisissez une page", ["Journal des rêves", "Analyse IA", "Galerie", "Statistiques"])

    if page == "Journal des rêves":
        journal_page()
    elif page == "Analyse IA":
        analyse_page()
    elif page == "Galerie":
        galerie_page()
    elif page == "Statistiques":
        stats_page()

def journal_page():
    st.header("Journal des rêves")
    
    # Formulaire pour un nouveau rêve
    with st.form("dream_form"):
        date = st.date_input("Date du rêve", datetime.now().date())
        dream_text = st.text_area("Décrivez votre rêve", height=200)
        sleep_quality = st.slider("Qualité du sommeil", 1, 5, 3)
        mood = st.selectbox("Humeur", ["Joyeux", "Triste", "Neutre", "Anxieux", "Calme"])
        tags = st.text_input("Tags (séparés par des virgules)")
        submit = st.form_submit_button("Enregistrer le rêve")

        if submit and dream_text:
            # Sauvegarde du rêve
            dream_id = dream_manager.add_dream(
                user_id=st.session_state.get('user_id', 'default_user'),
                date=date.strftime('%Y-%m-%d'),
                dream_text=dream_text,
                sleep_quality=sleep_quality,
                mood=mood,
                tags=tags
            )
            st.success("Rêve enregistré avec succès!")

    # Affichage des rêves précédents
    dreams = dream_manager.get_dreams()
    
    if dreams:
        st.subheader("Vos rêves précédents")
        for dream in dreams:
            with st.expander(f"Rêve du {dream[1]}"):
                st.write(dream[2])  # dream_text
                st.write(f"Qualité du sommeil: {dream[3]}/5")  # sleep_quality
                st.write(f"Humeur: {dream[5]}")  # mood
                st.write(f"Tags: {dream[6]}")  # tags
                
                # Bouton pour modifier
                if st.button("Modifier", key=f"edit_{dream[0]}"):
                    # Ouvrir un formulaire de modification
                    with st.form(f"edit_dream_{dream[0]}"):
                        new_dream_text = st.text_area("Modifier le rêve", value=dream[2], height=200)
                        new_sleep_quality = st.slider("Nouvelle qualité du sommeil", 1, 5, dream[3])
                        new_mood = st.selectbox("Nouvelle humeur", ["Joyeux", "Triste", "Neutre", "Anxieux", "Calme"], index=["Joyeux", "Triste", "Neutre", "Anxieux", "Calme"].index(dream[5]))
                        new_tags = st.text_input("Modifier les tags", value=dream[6])
                        submit = st.form_submit_button("Sauvegarder les modifications")
                        
                        if submit:
                            dream_manager.update_dream(
                                dream[0],
                                dream_text=new_dream_text,
                                sleep_quality=new_sleep_quality,
                                mood=new_mood,
                                tags=new_tags
                            )
                            st.success("Rêve mis à jour avec succès!")
                            st.rerun()

def analyse_page():
    st.header("Analyse IA de vos rêves")
    
    # Récupération des rêves
    dreams = dream_manager.get_dreams()
    
    if not dreams:
        st.warning("Aucun rêve enregistré pour l'analyse")
        return

    if st.button("Analyser vos rêves"):
        with st.spinner("Analyse en cours..."):
            # Préparation du texte pour l'analyse
            dreams_text = "\n\n".join([d[2] for d in dreams])
            
            # Analyse avec OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Tu es un expert en analyse des rêves. Analyse le texte suivant et identifie les thèmes récurrents, symboles et émotions dominantes."
                    },
                    {"role": "user", "content": dreams_text}
                ]
            )
            
            analysis = response.choices[0].message.content
            
            # Sauvegarde de l'analyse
            dream_manager.add_analysis(
                user_id=st.session_state.get('user_id', 'default_user'),
                analysis_date=datetime.now().strftime('%Y-%m-%d'),
                themes=analysis,
                emotions=""
            )
            
            st.subheader("Analyse de vos rêves")
            st.write(analysis)

def galerie_page():
    st.header("Galerie des rêves")
    
    # Récupération des rêves
    dreams = dream_manager.get_dreams()
    
    if not dreams:
        st.warning("Aucun rêve enregistré pour la galerie")
        return

    # Génération d'images basées sur les rêves
    if st.button("Générer une image artistique"):
        with st.spinner("Création de l'image artistique..."):
            # Préparation du texte pour l'image
            dreams_text = "\n\n".join([d[2] for d in dreams])
            
            # Utilisation de DALL-E pour générer l'image
            response = openai.Image.create(
                prompt=f"Une image artistique représentant les thèmes suivants: {dreams_text}",
                n=1,
                size="512x512"
            )
            
            image_url = response['data'][0]['url']
            
            # Affichage de l'image
            st.image(image_url, caption="Votre rêve visualisé")

def stats_page():
    st.header("Statistiques de vos rêves")
    
    # Récupération des rêves
    dreams = dream_manager.get_dreams()
    
    if not dreams:
        st.warning("Aucun rêve enregistré pour les statistiques")
        return

    # Statistiques de base
    st.subheader("Statistiques générales")
    
    # Nombre total de rêves
    total_dreams = len(dreams)
    st.metric("Total des rêves", total_dreams)
    
    # Qualité moyenne du sommeil
    avg_sleep_quality = sum(d[3] for d in dreams) / total_dreams
    st.metric("Qualité moyenne du sommeil", f"{avg_sleep_quality:.1f}/5")
    
    # Distribution des humeurs
    st.subheader("Distribution des humeurs")
    moods = [d[5] for d in dreams]
    mood_counts = {mood: moods.count(mood) for mood in set(moods)}
    st.bar_chart(mood_counts)

if __name__ == "__main__":
    main()
