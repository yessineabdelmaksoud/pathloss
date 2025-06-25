# test_multi_wifi.py
"""
Test simple pour vérifier le fonctionnement de la structure multi-WiFi
"""

try:
    print("🔄 Test des imports...")
    
    # Test des imports principaux
    from config import DEFAULT_VALUES, LIMITS, MESSAGES
    print("✅ Config imported")
    
    from models.model_loader import load_model
    print("✅ Model loader imported")
    
    from utils.image_processing import compute_LOS_and_walls_corrected
    print("✅ Image processing imported")
    
    from utils.path_loss_calculator import calculate_combined_path_loss
    print("✅ Path loss calculator imported")
    
    from ui.sidebar import render_sidebar
    print("✅ Sidebar imported")
    
    from ui.main_content import render_main_content
    print("✅ Main content imported")
    
    from ui.heatmap_generator import render_heatmap_generation_section
    print("✅ Heatmap generator imported")
    
    print("\n🎉 Tous les modules ont été importés avec succès!")
    print(f"📊 Configuration par défaut : {DEFAULT_VALUES['num_wifi']} WiFi(s)")
    print(f"📏 Limites : {LIMITS['min_wifi']}-{LIMITS['max_wifi']} WiFi(s)")
    
except Exception as e:
    print(f"❌ Erreur lors de l'import: {e}")
    import traceback
    traceback.print_exc()
