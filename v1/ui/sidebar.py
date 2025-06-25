# ui/sidebar.py
"""
Module pour l'interface sidebar
"""

import streamlit as st
from config import DEFAULT_VALUES, LIMITS, ACCEPTED_IMAGE_TYPES, MESSAGES


def render_sidebar():
    """
    Rend l'interface de la sidebar avec tous les paramètres
    
    Returns:
        dict: Dictionnaire contenant tous les paramètres de la sidebar
    """
    with st.sidebar:
        st.header("⚙️ Paramètres")
        
        # Upload du fichier
        uploaded_file = st.file_uploader(
            "Télécharger le plan d'étage",
            type=ACCEPTED_IMAGE_TYPES,
            help="Téléchargez une image du plan d'étage"
        )
        
        if uploaded_file is not None:
            st.success(MESSAGES["file_uploaded"])
        
        # Dimensions réelles
        st.subheader("📏 Dimensions réelles")
        real_length_m = st.number_input(
            "Longueur du plan (mètres)",
            min_value=LIMITS["min_dimension"],
            value=DEFAULT_VALUES["real_length_m"],
            step=0.01,
            help="Longueur réelle du plan en mètres"
        )
        
        real_width_m = st.number_input(
            "Largeur du plan (mètres)",
            min_value=LIMITS["min_dimension"],
            value=DEFAULT_VALUES["real_width_m"],
            step=0.01,
            help="Largeur réelle du plan en mètres"
        )
        
        # Position du transmetteur
        st.subheader("📡 Configuration des transmetteurs WiFi")
        
        # Nombre de points WiFi
        num_wifi = st.number_input(
            "Nombre de points WiFi",
            min_value=LIMITS["min_wifi"],
            max_value=LIMITS["max_wifi"],
            value=DEFAULT_VALUES["num_wifi"],
            step=1,
            help="Nombre de points WiFi à placer sur le plan"
        )
        
        # Paramètres de fréquence et résolution
        st.subheader("🔧 Paramètres de calcul")
        frequency_mhz = st.number_input(
            "Fréquence (MHz)",
            min_value=LIMITS["min_frequency"],
            max_value=LIMITS["max_frequency"],
            value=DEFAULT_VALUES["frequency_mhz"],
            step=1,
            help="Fréquence du signal en MHz"
        )
        
        step = st.number_input(
            "Résolution de la heatmap (pas en pixels)",
            min_value=LIMITS["min_step"],
            max_value=LIMITS["max_step"],
            value=DEFAULT_VALUES["step"],
            step=1,
            help="Plus petit = plus précis mais plus lent"
        )
    
    return {
        'uploaded_file': uploaded_file,
        'real_length_m': real_length_m,
        'real_width_m': real_width_m,
        'num_wifi': num_wifi,
        'frequency_mhz': frequency_mhz,
        'step': step
    }
