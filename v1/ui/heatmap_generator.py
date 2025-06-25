# ui/heatmap_generator.py
"""
Module pour la génération et l'affichage des heatmaps
"""

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import io
import traceback
from utils.image_processing import (
    process_uploaded_image, 
    convert_position_to_pixels, 
    validate_tx_position
)
from utils.path_loss_calculator import (
    generate_rx_data, 
    predict_path_loss, 
    create_interpolated_grid
)
from config import MESSAGES


def check_generation_requirements(uploaded_file, model, real_length_m, real_width_m,
                                tx_x_m, tx_y_m, frequency_mhz, step):
    """
    Vérifie si tous les prérequis pour la génération sont remplis
    
    Returns:
        tuple: (can_generate, issues_list)
    """
    issues = []
    
    if uploaded_file is None:
        issues.append("❌ Aucun fichier image téléchargé")
    if model is None:
        issues.append("❌ Modèle ML non chargé")
    if not (0 <= tx_x_m <= real_length_m):
        issues.append("❌ Position X du transmetteur hors limites")
    if not (0 <= tx_y_m <= real_width_m):
        issues.append("❌ Position Y du transmetteur hors limites")
    if not (100 <= frequency_mhz <= 10000):
        issues.append("❌ Fréquence hors de la plage valide")
    if step <= 0:
        issues.append("❌ Résolution invalide")
    
    can_generate = len(issues) == 0
    return can_generate, issues


def create_heatmap_plot(binary_img, original_img, grid_x, grid_y, grid_path_loss,
                       path_loss_values, tx_x_px, tx_y_px, img_width, img_height):
    """
    Crée le plot matplotlib de la heatmap
    
    Returns:
        matplotlib.figure.Figure: Figure de la heatmap
    """
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Afficher le plan d'étage en arrière-plan
    ax.imshow(original_img, cmap='gray', alpha=0.6, extent=[0, img_width, img_height, 0])
    
    # Afficher la heatmap interpolée
    im = ax.imshow(grid_path_loss.T, extent=[0, img_width, img_height, 0],
                  cmap='jet', alpha=0.7, origin='upper',
                  vmin=path_loss_values.min() if path_loss_values.size > 0 else None,
                  vmax=path_loss_values.max() if path_loss_values.size > 0 else None)
    
    # Ajouter la barre de couleur
    plt.colorbar(im, label='Path Loss (dB)')
    
    # Visualisation Tx améliorée
    ax.scatter(tx_x_px, tx_y_px, color='red', s=200, marker='*',
              edgecolors='black', linewidth=2, label='Tx (WiFi)')
    ax.text(tx_x_px, tx_y_px - 10, 'Tx', color='red', fontsize=14, ha='center')
    
    # Ajouter des contours si possible
    if path_loss_values.size > 50 and np.std(path_loss_values) > 1:
        try:
            min_pl = path_loss_values.min() if path_loss_values.size > 0 else 30
            max_pl = path_loss_values.max() if path_loss_values.size > 0 else 150
            levels = np.linspace(min_pl, max_pl, 10)
            
            CS = ax.contour(grid_x, grid_y, grid_path_loss, levels=levels, 
                           colors='white', alpha=0.5)
            ax.clabel(CS, inline=1, fontsize=10, colors='white', fmt='%1.0f dB')
        except Exception:
            pass  # Continuer sans contours si le tracé échoue
    
    ax.set_title('Path Loss Heatmap')
    ax.set_xlabel('Position X (pixels)')
    ax.set_ylabel('Position Y (pixels)')
    ax.legend()
    plt.tight_layout()
    
    return fig


def process_and_generate_heatmap(uploaded_file, real_length_m, real_width_m, 
                               tx_x_m, tx_y_m, frequency_mhz, step, model):
    """
    Traite l'image et génère la heatmap complète
    
    Returns:
        tuple: (figure, error_message)
    """
    try:
        # Traiter l'image
        binary_img, original_img, error = process_uploaded_image(uploaded_file)
        if error:
            return None, error
        
        img_height, img_width = binary_img.shape
        
        # Convertir la position Tx en pixels
        tx_x_px = convert_position_to_pixels(tx_x_m, real_length_m, img_width)
        tx_y_px = convert_position_to_pixels(tx_y_m, real_width_m, img_height)
        
        # Vérifier les limites
        if not validate_tx_position(tx_x_px, tx_y_px, img_width, img_height):
            return None, "La position Tx est hors des limites de l'image."
        
        # Générer les données Rx
        rx_df = generate_rx_data(binary_img, tx_x_px, tx_y_px, real_length_m, 
                               real_width_m, frequency_mhz, step)
        
        if rx_df.empty:
            return None, "Aucun espace libre trouvé."
        
        # Prédire le Path Loss
        rx_df = predict_path_loss(rx_df, model)
        
        # Créer la grille interpolée
        grid_x, grid_y, grid_path_loss = create_interpolated_grid(
            rx_df, img_width, img_height, binary_img
        )
        
        if grid_path_loss is None:
            return None, "Erreur lors de la création de la grille interpolée."
        
        # Créer la heatmap
        path_loss_values = rx_df['Path_Loss_Predicted'].values
        fig = create_heatmap_plot(binary_img, original_img, grid_x, grid_y, 
                                grid_path_loss, path_loss_values, tx_x_px, tx_y_px,
                                img_width, img_height)
        
        return fig, None
        
    except Exception as e:
        error_msg = f"Erreur lors du traitement: {str(e)}"
        traceback.print_exc()
        return None, error_msg


def render_heatmap_generation_section(params, model):
    """
    Rend la section de génération de heatmap
    
    Args:
        params: Dictionnaire des paramètres de l'application
        model: Modèle ML chargé
    """
    st.markdown("---")
    st.header("🎯 Génération de la Heatmap")
    
    # Vérifications avant génération
    can_generate, issues = check_generation_requirements(
        params['uploaded_file'], model, params['real_length_m'], 
        params['real_width_m'], params['tx_x_m'], params['tx_y_m'],
        params['frequency_mhz'], params['step']
    )
    
    if st.button("🚀 Générer la Heatmap", disabled=not can_generate, type="primary"):
        if not can_generate:
            st.error("❌ Veuillez vérifier tous les paramètres avant de générer la heatmap.")
        else:
            with st.spinner("🔄 Génération de la heatmap en cours..."):
                try:
                    fig, error = process_and_generate_heatmap(
                        params['uploaded_file'], params['real_length_m'], 
                        params['real_width_m'], params['tx_x_m'], params['tx_y_m'],
                        params['frequency_mhz'], params['step'], model
                    )
                    
                    if error:
                        st.error(f"❌ Erreur: {error}")
                    else:
                        st.success(MESSAGES["heatmap_generated"])
                        
                        # Afficher la heatmap
                        st.pyplot(fig)
                        
                        # Bouton de téléchargement
                        render_download_button(fig)
                        
                        plt.close(fig)  # Fermer la figure pour libérer la mémoire
                        
                except Exception as e:
                    st.error(f"❌ Erreur inattendue: {str(e)}")
                    with st.expander("🔍 Détails de l'erreur"):
                        st.code(traceback.format_exc())
    
    # Informations supplémentaires
    if not can_generate:
        with st.expander("ℹ️ Pourquoi le bouton est-il désactivé?"):
            for issue in issues:
                st.write(issue)


def render_download_button(fig):
    """
    Rend le bouton de téléchargement de la heatmap
    
    Args:
        fig: Figure matplotlib à télécharger
    """
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)
    
    st.download_button(
        label="💾 Télécharger la Heatmap",
        data=buf,
        file_name="path_loss_heatmap.png",
        mime="image/png"
    )
