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
    3. **� Choisissez** le nombre de points WiFi à placer
    4. **📡 Cliquez** sur l'image pour placer les points WiFi
    5. **🔧 Ajustez** la fréquence et la résolution
    6. **🚀 Cliquez** sur "Générer la Heatmap"
    
    💡 **Astuce**: La heatmap affichera le meilleur signal disponible à chaque point (minimum path loss).
    """)


def render_image_preview_and_placement(uploaded_file, real_length_m, real_width_m, num_wifi):
    """
    Rend l'aperçu de l'image et le placement interactif des points WiFi
    
    Args:
        uploaded_file: Fichier image uploadé
        real_length_m: Longueur réelle en mètres
        real_width_m: Largeur réelle en mètres
        num_wifi: Nombre de points WiFi à placer
        
    Returns:
        list: Liste des positions des transmetteurs [(x1, y1), (x2, y2), ...]
    """
    st.header("🖼️ Aperçu du plan - Placement des points WiFi")
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        img_array = np.array(image.convert('RGB'))  # RGB pour le canvas

        st.subheader(f"🖱️ Cliquez sur le plan pour placer {num_wifi} point(s) WiFi")
        
        # Bouton pour effacer tous les points
        if st.button("🗑️ Effacer tous les points WiFi"):
            if "wifi_positions" in st.session_state:
                del st.session_state.wifi_positions
            st.rerun()

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
        wifi_positions = process_canvas_clicks_multiple(
            canvas_result, img_array, canvas_width, canvas_height,
            real_length_m, real_width_m, num_wifi
        )
        
    else:
        st.info(MESSAGES["upload_image"])
        wifi_positions = [(real_length_m / 2, real_width_m / 2)]  # valeur par défaut
    
    return wifi_positions


def process_canvas_clicks_multiple(canvas_result, img_array, canvas_width, canvas_height,
                                  real_length_m, real_width_m, num_wifi):
    """
    Traite les clics sur le canvas et gère plusieurs points WiFi
    
    Args:
        canvas_result: Résultat du canvas interactif
        img_array: Array de l'image
        canvas_width: Largeur du canvas
        canvas_height: Hauteur du canvas
        real_length_m: Longueur réelle en mètres
        real_width_m: Largeur réelle en mètres
        num_wifi: Nombre de points WiFi à placer
        
    Returns:
        list: Liste des positions WiFi [(x1, y1), (x2, y2), ...]
    """
    # Initialiser la liste des positions WiFi dans la session
    if "wifi_positions" not in st.session_state:
        st.session_state.wifi_positions = []

    # Si l'utilisateur a cliqué pour dessiner des cercles
    if canvas_result.json_data is not None:
        objects = canvas_result.json_data["objects"]
        
        # Convertir tous les objets en positions WiFi
        new_positions = []
        for obj in objects:
            tx_x_px = int(obj["left"] + obj["radius"])
            tx_y_px = int(obj["top"] + obj["radius"])

            # Conversion en mètres (avec facteur d'échelle si l'image est redimensionnée)
            scale_x = img_array.shape[1] / canvas_width
            scale_y = img_array.shape[0] / canvas_height
            
            actual_tx_x_px = int(tx_x_px * scale_x)
            actual_tx_y_px = int(tx_y_px * scale_y)
            
            tx_x_m = (actual_tx_x_px / img_array.shape[1]) * real_length_m
            tx_y_m = (actual_tx_y_px / img_array.shape[0]) * real_width_m
            
            new_positions.append((tx_x_m, tx_y_m))

        # Limiter au nombre de WiFi demandé
        st.session_state.wifi_positions = new_positions[:num_wifi]
        
        # Afficher les positions
        if st.session_state.wifi_positions:
            st.success(f"📍 {len(st.session_state.wifi_positions)} point(s) WiFi placé(s)")
            for i, (x, y) in enumerate(st.session_state.wifi_positions):
                st.info(MESSAGES["wifi_placed"].format(i+1, x, y))
                
            if len(st.session_state.wifi_positions) < num_wifi:
                st.warning(f"⚠️ Il manque {num_wifi - len(st.session_state.wifi_positions)} point(s) WiFi. Cliquez sur l'image pour les placer.")
        else:
            st.warning(MESSAGES["click_to_place"])
    else:
        st.warning(MESSAGES["click_to_place"])
    
    # Retourner les positions ou valeurs par défaut
    if len(st.session_state.wifi_positions) > 0:
        return st.session_state.wifi_positions
    else:
        # Valeurs par défaut distribuées
        default_positions = []
        for i in range(num_wifi):
            x = real_length_m * (i + 1) / (num_wifi + 1)
            y = real_width_m / 2
            default_positions.append((x, y))
        return default_positions


def render_main_content(uploaded_file, real_length_m, real_width_m, num_wifi):
    """
    Rend le contenu principal de l'application
    
    Args:
        uploaded_file: Fichier image uploadé
        real_length_m: Longueur réelle en mètres
        real_width_m: Largeur réelle en mètres
        num_wifi: Nombre de points WiFi à placer
        
    Returns:
        list: Liste des positions des transmetteurs
    """
    col1, col2 = st.columns([1, 1])
    
    with col1:
        render_instructions()
    
    with col2:
        wifi_positions = render_image_preview_and_placement(
            uploaded_file, real_length_m, real_width_m, num_wifi
        )
    
    return wifi_positions
