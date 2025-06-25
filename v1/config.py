# config.py
"""
Configuration et constantes pour l'application Path Loss Heatmap Generator
"""

# Configuration Streamlit
STREAMLIT_CONFIG = {
    "page_title": "Path Loss Heatmap Generator",
    "page_icon": "📡",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Constantes pour l'application
MODEL_FILENAME = 'pathloss_predictor.pkl'

# Limites et valeurs par défaut
DEFAULT_VALUES = {
    "real_length_m": 10.0,
    "real_width_m": 8.0,
    "frequency_mhz": 2400,
    "step": 5,
}

LIMITS = {
    "min_dimension": 0.01,
    "min_frequency": 100,
    "max_frequency": 10000,
    "min_step": 1,
    "max_step": 50,
    "max_canvas_height": 400,
    "max_canvas_width": 600,
}

# Types de fichiers acceptés
ACCEPTED_IMAGE_TYPES = ['png', 'jpg', 'jpeg', 'bmp', 'tiff']

# Messages
MESSAGES = {
    "model_loaded": "Modèle ML chargé avec succès!",
    "model_not_found": "ERREUR: Modèle 'pathloss_predictor.pkl' non trouvé.",
    "model_load_error": "ERREUR: Erreur lors du chargement du modèle: {}",
    "file_uploaded": "✅ Fichier téléchargé avec succès!",
    "heatmap_generated": "✅ Heatmap générée avec succès!",
    "click_to_place": "🛑 Cliquez sur l'image pour placer le WiFi (Tx).",
    "upload_image": "📁 Téléchargez une image pour voir l'aperçu",
}
