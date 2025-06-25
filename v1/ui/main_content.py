# ui/main_content.py
"""
Module pour le contenu principal et le canvas interactif
"""

import streamlit as st
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from config import LIMITS, MESSAGES


def render_instructions():
    """Affiche les instructions d'utilisation"""
    st.header("📋 Instructions")
    st.markdown("""
    1. **📤 Téléchargez** votre plan d'étage dans la sidebar
    2. **📏 Entrez** les dimensions réelles du plan
    3. **📡 Définissez** la position du transmetteur (Tx)
    4. **🔧 Ajustez** la fréquence et la résolution
    5. **🚀 Cliquez** sur "Générer la Heatmap"
    """)


def render_image_preview_and_placement(uploaded_file, real_length_m, real_width_m):
    """
    Rend l'aperçu de l'image et le placement interactif du WiFi
    
    Args:
        uploaded_file: Fichier image uploadé
        real_length_m: Longueur réelle en mètres
        real_width_m: Largeur réelle en mètres
        
    Returns:
        tuple: (tx_x_m, tx_y_m) - Position du transmetteur en mètres
    """
    st.header("🖼️ Aperçu du plan - Placement WiFi")
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        img_array = np.array(image.convert('RGB'))  # RGB pour le canvas

        st.subheader("🖱️ Cliquez sur le plan pour placer le WiFi (Tx)")

        # Calculer les dimensions du canvas
        canvas_height = min(img_array.shape[0], LIMITS["max_canvas_height"])
        canvas_width = min(img_array.shape[1], LIMITS["max_canvas_width"])

        # Canvas interactif
        canvas_result = st_canvas(
            fill_color="rgba(255, 0, 0, 0.3)",  # Couleur des cercles
            stroke_width=3,
            stroke_color="#FF0000",
            background_image=image,
            update_streamlit=True,
            height=canvas_height,
            width=canvas_width,
            drawing_mode="circle",
            point_display_radius=5,
            key="canvas",
        )

        # Traitement des clics sur le canvas
        tx_x_m, tx_y_m = process_canvas_clicks(
            canvas_result, img_array, canvas_width, canvas_height,
            real_length_m, real_width_m
        )
        
    else:
        st.info(MESSAGES["upload_image"])
        tx_x_m = real_length_m / 2  # valeur par défaut
        tx_y_m = real_width_m / 2   # valeur par défaut
    
    return tx_x_m, tx_y_m


def process_canvas_clicks(canvas_result, img_array, canvas_width, canvas_height,
                         real_length_m, real_width_m):
    """
    Traite les clics sur le canvas et calcule la position du transmetteur
    
    Args:
        canvas_result: Résultat du canvas interactif
        img_array: Array de l'image
        canvas_width: Largeur du canvas
        canvas_height: Hauteur du canvas
        real_length_m: Longueur réelle en mètres
        real_width_m: Largeur réelle en mètres
        
    Returns:
        tuple: (tx_x_m, tx_y_m) - Position en mètres
    """
    # Si l'utilisateur a cliqué pour dessiner un cercle
    if canvas_result.json_data is not None:
        objects = canvas_result.json_data["objects"]
        if len(objects) > 0:
            last_obj = objects[-1]  # dernier cercle ajouté
            tx_x_px = int(last_obj["left"] + last_obj["radius"])
            tx_y_px = int(last_obj["top"] + last_obj["radius"])
            st.success(f"📍 Position Tx choisie: ({tx_x_px}px, {tx_y_px}px)")

            # Conversion en mètres (avec facteur d'échelle si l'image est redimensionnée)
            scale_x = img_array.shape[1] / canvas_width
            scale_y = img_array.shape[0] / canvas_height
            
            actual_tx_x_px = int(tx_x_px * scale_x)
            actual_tx_y_px = int(tx_y_px * scale_y)
            
            tx_x_m = (actual_tx_x_px / img_array.shape[1]) * real_length_m
            tx_y_m = (actual_tx_y_px / img_array.shape[0]) * real_width_m
            st.info(f"📏 Position Tx réelle: ({tx_x_m:.2f}m, {tx_y_m:.2f}m)")

            # Mettre à jour les valeurs dans la session (optionnel)
            st.session_state.tx_x_m = tx_x_m
            st.session_state.tx_y_m = tx_y_m

            return tx_x_m, tx_y_m
        else:
            st.warning(MESSAGES["click_to_place"])
    else:
        st.warning(MESSAGES["click_to_place"])
    
    # Valeurs par défaut si pas de clic
    return real_length_m / 2, real_width_m / 2


def render_main_content(uploaded_file, real_length_m, real_width_m):
    """
    Rend le contenu principal de l'application
    
    Args:
        uploaded_file: Fichier image uploadé
        real_length_m: Longueur réelle en mètres
        real_width_m: Largeur réelle en mètres
        
    Returns:
        tuple: (tx_x_m, tx_y_m) - Position du transmetteur
    """
    col1, col2 = st.columns([1, 1])
    
    with col1:
        render_instructions()
    
    with col2:
        tx_x_m, tx_y_m = render_image_preview_and_placement(
            uploaded_file, real_length_m, real_width_m
        )
    
    return tx_x_m, tx_y_m
