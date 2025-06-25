# utils/path_loss_calculator.py
"""
Module pour les calculs de path loss et les prédictions
"""

import numpy as np
import pandas as pd
from scipy.interpolate import griddata
from utils.image_processing import (
    compute_LOS_and_walls_corrected, 
    convert_distance_to_meters
)


def generate_rx_data(binary_img, tx_x_px, tx_y_px, real_length_m, real_width_m, 
                    frequency_mhz, step):
    """
    Génère les données des points récepteurs pour le calcul du path loss
    
    Args:
        binary_img: Image binaire du plan
        tx_x_px: Position X du transmetteur en pixels
        tx_y_px: Position Y du transmetteur en pixels
        real_length_m: Longueur réelle en mètres
        real_width_m: Largeur réelle en mètres
        frequency_mhz: Fréquence en MHz
        step: Pas de la grille en pixels
        
    Returns:
        pd.DataFrame: Données des récepteurs avec caractéristiques calculées
    """
    img_height, img_width = binary_img.shape
    rx_data = []
    
    for rx_y in range(0, img_height, step):
        for rx_x in range(0, img_width, step):
            # Vérifier si le point est dans un espace libre
            if (0 <= rx_x < img_width and 0 <= rx_y < img_height and 
                binary_img[rx_y, rx_x] == 0):
                
                # Calculer la distance en pixels
                distance_px = np.sqrt((rx_x - tx_x_px)**2 + (rx_y - tx_y_px)**2)
                
                # Convertir en mètres
                distance_m = convert_distance_to_meters(
                    distance_px, real_length_m, real_width_m, img_width, img_height
                )
                
                # Éviter les distances nulles
                if distance_m < 1e-6:
                    distance_m = 1e-6
                
                # Calculer le nombre de murs traversés
                _, num_walls = compute_LOS_and_walls_corrected(
                    (tx_x_px, tx_y_px), (rx_x, rx_y), binary_img
                )
                
                rx_data.append({
                    'RX_x': rx_x,
                    'RX_y': rx_y,
                    'distance': distance_m,
                    'num_walls': num_walls,
                    'frequency': frequency_mhz
                })
    
    return pd.DataFrame(rx_data)


def predict_path_loss(rx_df, model):
    """
    Prédit le path loss pour tous les points récepteurs
    
    Args:
        rx_df: DataFrame avec les données des récepteurs
        model: Modèle ML entraîné
        
    Returns:
        pd.DataFrame: DataFrame avec les prédictions ajoutées
    """
    if rx_df.empty:
        return rx_df
    
    features_for_model = ['num_walls', 'distance', 'frequency']
    X_predict = rx_df[features_for_model]
    rx_df = rx_df.copy()
    rx_df['Path_Loss_Predicted'] = model.predict(X_predict)
    
    return rx_df


def create_interpolated_grid(rx_df, img_width, img_height, binary_img):
    """
    Crée une grille interpolée pour la heatmap
    
    Args:
        rx_df: DataFrame avec les prédictions
        img_width: Largeur de l'image
        img_height: Hauteur de l'image
        binary_img: Image binaire pour masquer les murs
        
    Returns:
        tuple: (grid_x, grid_y, grid_path_loss)
    """
    if rx_df.empty:
        return None, None, None
    
    # Extraire les coordonnées et valeurs
    rx_x_coords = rx_df['RX_x'].values
    rx_y_coords = rx_df['RX_y'].values
    path_loss_values = rx_df['Path_Loss_Predicted'].values
    
    # Créer une grille régulière pour l'interpolation
    grid_x, grid_y = np.mgrid[0:img_width, 0:img_height]
    
    # Interpoler les valeurs de perte de trajet
    grid_path_loss = griddata(
        (rx_x_coords, rx_y_coords), path_loss_values, (grid_x, grid_y),
        method='cubic',
        fill_value=np.nan
    )
    
    # Masquer les murs
    grid_path_loss[binary_img.T == 1] = np.nan
    
    return grid_x, grid_y, grid_path_loss
