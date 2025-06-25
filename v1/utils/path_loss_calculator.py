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


def generate_rx_data_multiple_wifi(binary_img, wifi_positions_px, real_length_m, real_width_m, 
                                  frequency_mhz, step):
    """
    Génère les données des points récepteurs pour plusieurs points WiFi
    
    Args:
        binary_img: Image binaire du plan
        wifi_positions_px: Liste des positions WiFi en pixels [(x1, y1), (x2, y2), ...]
        real_length_m: Longueur réelle en mètres
        real_width_m: Largeur réelle en mètres
        frequency_mhz: Fréquence en MHz
        step: Pas de la grille en pixels
        
    Returns:
        pd.DataFrame: Données des récepteurs avec path loss pour chaque WiFi
    """
    img_height, img_width = binary_img.shape
    rx_data = []
    
    for rx_y in range(0, img_height, step):
        for rx_x in range(0, img_width, step):
            # Vérifier si le point est dans un espace libre
            if (0 <= rx_x < img_width and 0 <= rx_y < img_height and 
                binary_img[rx_y, rx_x] == 0):
                
                # Pour chaque point WiFi, calculer le path loss
                min_path_loss = float('inf')
                best_wifi_idx = 0
                
                for wifi_idx, (tx_x_px, tx_y_px) in enumerate(wifi_positions_px):
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
                    
                    # Créer un DataFrame temporaire pour la prédiction
                    temp_data = pd.DataFrame([{
                        'num_walls': num_walls,
                        'distance': distance_m,
                        'frequency': frequency_mhz
                    }])
                    
                    # Note: On calculera le path loss plus tard avec le modèle
                    # Pour l'instant, on stocke juste les paramètres du meilleur WiFi
                    # (celui avec la distance la plus courte comme approximation)
                    if distance_m < min_path_loss:
                        min_path_loss = distance_m
                        best_wifi_idx = wifi_idx
                        best_distance = distance_m
                        best_num_walls = num_walls
                
                rx_data.append({
                    'RX_x': rx_x,
                    'RX_y': rx_y,
                    'distance': best_distance,
                    'num_walls': best_num_walls,
                    'frequency': frequency_mhz,
                    'best_wifi_idx': best_wifi_idx
                })
    
    return pd.DataFrame(rx_data)


def calculate_combined_path_loss(binary_img, wifi_positions_px, real_length_m, real_width_m,
                               frequency_mhz, step, model):
    """
    Calcule le path loss combiné pour plusieurs points WiFi
    
    Args:
        binary_img: Image binaire du plan
        wifi_positions_px: Liste des positions WiFi en pixels
        real_length_m: Longueur réelle en mètres
        real_width_m: Largeur réelle en mètres
        frequency_mhz: Fréquence en MHz
        step: Pas de la grille en pixels
        model: Modèle ML
        
    Returns:
        pd.DataFrame: DataFrame avec les path loss combinés
    """
    img_height, img_width = binary_img.shape
    rx_data = []
    
    for rx_y in range(0, img_height, step):
        for rx_x in range(0, img_width, step):
            # Vérifier si le point est dans un espace libre
            if (0 <= rx_x < img_width and 0 <= rx_y < img_height and 
                binary_img[rx_y, rx_x] == 0):
                
                # Calculer le path loss pour chaque WiFi
                path_losses = []
                
                for tx_x_px, tx_y_px in wifi_positions_px:
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
                    
                    # Prédire le path loss pour ce WiFi
                    features = pd.DataFrame([{
                        'num_walls': num_walls,
                        'distance': distance_m,
                        'frequency': frequency_mhz
                    }])
                    
                    path_loss = model.predict(features)[0]
                    path_losses.append(path_loss)
                
                # Prendre le minimum path loss (meilleur signal)
                min_path_loss = min(path_losses)
                best_wifi_idx = path_losses.index(min_path_loss)
                
                rx_data.append({
                    'RX_x': rx_x,
                    'RX_y': rx_y,
                    'Path_Loss_Predicted': min_path_loss,
                    'best_wifi_idx': best_wifi_idx
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
