# Ajoutez ces imports en haut du fichier
from datetime import datetime
import traceback

# Modifiez la fonction main pour gérer les erreurs
def main():
    st.sidebar.header("Navigation")
    page = st.sidebar.selectbox("Choisissez une page", ["Journal des rêves", "Analyse IA", "Galerie", "Statistiques"])
    
    try:
        if page == "Journal des rêves":
            journal_page()
        elif page == "Analyse IA":
            analyse_page()
        elif page == "Galerie":
            galerie_page()
        elif page == "Statistiques":
            stats_page()
    except Exception as e:
        st.error("Une erreur est survenue. Veuillez réessayer.")
        st.error(f"Détails de l'erreur : {str(e)}")
        st.code(traceback.format_exc())

# Modifiez la fonction analyse_page
def analyse_page():
    st.title("Analyse IA des Rêves")
    try:
        dreams = db.get_dreams("user1")  # Remplacez par l'ID utilisateur approprié
        if not dreams:
            st.info("Aucun rêve à analyser pour le moment.")
            return
            
        dream_titles = [f"Rêve du {dream[2]} - {dream[3][:30]}..." for dream in dreams]
        selected_dream = st.selectbox("Sélectionnez un rêve à analyser", dream_titles)
        
        if st.button("Lancer l'analyse"):
            with st.spinner("Analyse en cours..."):
                try:
                    # Votre logique d'analyse ici
                    st.success("Analyse terminée avec succès !")
                except Exception as e:
                    st.error(f"Erreur lors de l'analyse : {str(e)}")
    except Exception as e:
        st.error(f"Erreur lors du chargement des rêves : {str(e)}")

# Modifiez la fonction galerie_page
def galerie_page():
    st.title("Galerie des Rêves")
    try:
        dreams = db.get_dreams("user1")  # Remplacez par l'ID utilisateur approprié
        if not dreams:
            st.info("Aucun rêve à afficher pour le moment.")
            return
            
        for dream in dreams:
            with st.expander(f"Rêve du {dream[2]}"):
                st.write(dream[3])  # Contenu du rêve
    except Exception as e:
        st.error(f"Erreur lors du chargement de la galerie : {str(e)}")

# Modifiez la fonction stats_page
def stats_page():
    st.title("Statistiques des Rêves")
    try:
        dreams = db.get_dreams("user1")  # Remplacez par l'ID utilisateur approprié
        if not dreams:
            st.info("Aucune donnée à afficher pour le moment.")
            return
            
        total_dreams = len(dreams)
        st.metric("Nombre total de rêves", total_dreams)
        
        # Calcul de la qualité moyenne du sommeil
        if total_dreams > 0:
            avg_sleep_quality = sum(dream[4] for dream in dreams if dream[4] is not None) / total_dreams
            st.metric("Qualité moyenne du sommeil", f"{avg_sleep_quality:.1f}/10")
    except Exception as e:
        st.error(f"Erreur lors du calcul des statistiques : {str(e)}")
