# main.py
"""
Application principale Path Loss Heatmap Generator
Point d'entrée principal pour l'application Streamlit
"""

import streamlit as st
import warnings
from config import STREAMLIT_CONFIG
from models.model_loader import get_model_status
from ui.sidebar import render_sidebar
from ui.main_content import render_main_content
from ui.heatmap_generator import render_heatmap_generation_section

# Supprimer les warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(**STREAMLIT_CONFIG)

# Titre principal
st.title("📡 Path Loss Heatmap Generator")
st.markdown("---")


def main():
    """Fonction principale de l'application"""
    
    # Charger le modèle et afficher le statut
    model, model_loaded = get_model_status()
    
    # Rendre la sidebar et récupérer les paramètres
    params = render_sidebar()
    
    # Rendre le contenu principal et obtenir la position Tx mise à jour
    tx_x_m, tx_y_m = render_main_content(
        params['uploaded_file'], 
        params['real_length_m'], 
        params['real_width_m']
    )
    
    # Mettre à jour les paramètres avec les positions du canvas
    params['tx_x_m'] = tx_x_m
    params['tx_y_m'] = tx_y_m
    
    # Rendre la section de génération de heatmap
    render_heatmap_generation_section(params, model)


if __name__ == "__main__":
    main()
