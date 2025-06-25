# utils/image_processing.py
"""
Module pour le traitement d'images et les calculs géométriques
"""

import cv2
import numpy as np
from PIL import Image


def compute_LOS_and_walls_corrected(tx, rx, wall_map):
    """
    Calcule LOS et nombre de murs traversés de manière plus précise.
    
    Args:
        tx: Position du transmetteur (x, y)
        rx: Position du récepteur (x, y)
        wall_map: Carte binaire des murs
        
    Returns:
        tuple: (has_LOS, wall_crossings)
    """
    x1, y1 = tx
    x2, y2 = rx

    # Handle case where Tx and Rx are the same point
    if x1 == x2 and y1 == y2:
        return True, 0  # LOS is true, 0 walls

    distance = np.sqrt((x2-x1)**2 + (y2-y1)**2)
    num_points = max(int(distance * 2), 100) if distance > 0 else 100

    x_points = np.linspace(x1, x2, num_points)
    y_points = np.linspace(y1, y2, num_points)

    wall_crossings = 0
    in_wall = False

    for i in range(len(x_points)):
        x_px = int(round(x_points[i]))
        y_px = int(round(y_points[i]))

        if 0 <= x_px < wall_map.shape[1] and 0 <= y_px < wall_map.shape[0]:
            current_is_wall = wall_map[y_px, x_px] == 1

            if current_is_wall and not in_wall:
                wall_crossings += 1
                in_wall = True
            elif not current_is_wall and in_wall:
                in_wall = False

    los = wall_crossings == 0
    return los, wall_crossings


def process_uploaded_image(uploaded_file):
    """
    Traite l'image uploadée et la convertit en carte binaire
    
    Args:
        uploaded_file: Fichier image uploadé
        
    Returns:
        tuple: (binary_image, original_image, error_message)
    """
    try:
        # Lire l'image
        image = Image.open(uploaded_file)
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        
        # Vérifier si l'image est valide
        if img is None:
            return None, None, "Impossible de lire le fichier image."
        
        # Binariser l'image
        if np.all(img == img[0,0]):
            return None, None, "L'image du plan semble vide ou déjà binaire."
        
        _, binary_img = cv2.threshold(img, 127, 1, cv2.THRESH_BINARY_INV)
        
        return binary_img, img, None
        
    except Exception as e:
        return None, None, f"Erreur lors du traitement de l'image: {str(e)}"


def convert_position_to_pixels(position_m, real_dimension_m, img_dimension_px):
    """
    Convertit une position en mètres vers des pixels
    
    Args:
        position_m: Position en mètres
        real_dimension_m: Dimension réelle en mètres
        img_dimension_px: Dimension de l'image en pixels
        
    Returns:
        int: Position en pixels
    """
    return int((position_m / real_dimension_m) * img_dimension_px)


def convert_distance_to_meters(distance_px, real_length_m, real_width_m, img_width, img_height):
    """
    Convertit une distance en pixels vers des mètres
    
    Args:
        distance_px: Distance en pixels
        real_length_m: Longueur réelle en mètres
        real_width_m: Largeur réelle en mètres
        img_width: Largeur de l'image en pixels
        img_height: Hauteur de l'image en pixels
        
    Returns:
        float: Distance en mètres
    """
    avg_scale = (real_length_m / img_width + real_width_m / img_height) / 2
    return distance_px * avg_scale


def validate_tx_position(tx_x_px, tx_y_px, img_width, img_height):
    """
    Valide si la position Tx est dans les limites de l'image
    
    Args:
        tx_x_px: Position X en pixels
        tx_y_px: Position Y en pixels
        img_width: Largeur de l'image
        img_height: Hauteur de l'image
        
    Returns:
        bool: True si la position est valide
    """
    return 0 <= tx_x_px < img_width and 0 <= tx_y_px < img_height
