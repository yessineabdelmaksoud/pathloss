# models/model_loader.py
"""
Module pour le chargement et la gestion du modèle ML
"""

import streamlit as st
import joblib
from config import MODEL_FILENAME, MESSAGES


@st.cache_resource
def load_model():
    """
    Charge le modèle ML avec mise en cache
    
    Returns:
        tuple: (model, status_message)
    """
    try:
        model = joblib.load(MODEL_FILENAME)
        return model, MESSAGES["model_loaded"]
    except FileNotFoundError:
        return None, MESSAGES["model_not_found"]
    except Exception as e:
        return None, MESSAGES["model_load_error"].format(e)


def get_model_status():
    """
    Obtient le statut du modèle et affiche les messages appropriés
    
    Returns:
        tuple: (model, is_loaded)
    """
    model, model_status = load_model()
    
    if model is not None:
        st.success(f"✅ {model_status}")
        return model, True
    else:
        st.error(f"❌ {model_status}")
        st.warning("Veuillez vous assurer que le fichier 'pathloss_predictor.pkl' est dans le même répertoire.")
        return model, False
