# Path Loss Heatmap Generator - Structure Modulaire

## 📁 Structure du Projet

```
v1/
├── main.py                          # Point d'entrée principal
├── config.py                        # Configuration et constantes
├── pathloss_predictor.pkl          # Modèle ML (à conserver)
├── run_app.py                      # Script original (peut être supprimé)
├── streamlit_app.py                # Code original (peut être renommé en backup)
│
├── models/                         # Gestion des modèles ML
│   ├── __init__.py
│   └── model_loader.py            # Chargement et cache du modèle
│
├── utils/                          # Utilitaires et calculs
│   ├── __init__.py
│   ├── image_processing.py        # Traitement d'images et géométrie
│   └── path_loss_calculator.py    # Calculs de path loss
│
└── ui/                            # Interface utilisateur
    ├── __init__.py
    ├── sidebar.py                 # Interface de la sidebar
    ├── main_content.py           # Contenu principal et canvas
    └── heatmap_generator.py      # Génération des heatmaps
```

## 🚀 Utilisation

### Lancer l'application :
```bash
streamlit run main.py
```

### Ancien fichier :
Pour utiliser l'ancien fichier monolithique :
```bash
streamlit run streamlit_app.py
```

## 📋 Description des Modules

### 🎛️ `config.py`
- Configuration Streamlit
- Constantes de l'application
- Valeurs par défaut
- Messages et limites

### 🤖 `models/model_loader.py`
- Chargement du modèle ML avec cache
- Gestion des erreurs de modèle
- Affichage du statut du modèle

### 🖼️ `utils/image_processing.py`
- Traitement des images uploadées
- Calculs géométriques (LOS, murs)
- Conversions pixels ↔ mètres
- Validation des positions

### 📊 `utils/path_loss_calculator.py`
- Génération des données récepteurs
- Prédictions ML du path loss
- Interpolation des grilles
- Création des heatmaps

### 🎨 `ui/sidebar.py`
- Interface des paramètres
- Upload de fichiers
- Contrôles des dimensions
- Paramètres de calcul

### 🖱️ `ui/main_content.py`
- Instructions d'utilisation
- Canvas interactif
- Placement du transmetteur
- Aperçu de l'image

### 🌡️ `ui/heatmap_generator.py`
- Génération des heatmaps
- Visualisation matplotlib
- Validation des prérequis
- Téléchargement des résultats

## ✅ Avantages de cette Structure

1. **🧩 Modularité** : Code organisé par fonctionnalités
2. **🔄 Réutilisabilité** : Modules indépendants
3. **🧪 Testabilité** : Fonctions isolées testables
4. **📈 Maintenabilité** : Plus facile à déboguer et améliorer
5. **👥 Collaboration** : Différents développeurs peuvent travailler sur différents modules
6. **📚 Lisibilité** : Code plus clair et documenté

## 🔧 Maintenance

- Chaque module a une responsabilité claire
- Les imports sont organisés et documentés
- Configuration centralisée dans `config.py`
- Interface séparée de la logique métier
