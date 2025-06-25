# Path Loss Heatmap Generator - Version Multi-WiFi

## 🆕 Nouvelles Fonctionnalités

### ✨ **Support Multi-WiFi**
- **Placement multiple** : Placez jusqu'à 10 points WiFi sur votre plan
- **Heatmap combinée** : Visualisez le meilleur signal disponible à chaque point
- **Interface intuitive** : Cliquez sur l'image pour placer les points WiFi
- **Couleurs distinctes** : Chaque point WiFi a sa propre couleur sur la carte

## 🎯 Guide d'Utilisation

### 1. **Configuration Initiale**
```bash
# Lancer l'application
streamlit run main.py
```

### 2. **Paramètres dans la Sidebar**
- 📁 **Télécharger le plan d'étage** (PNG, JPG, etc.)
- 📏 **Dimensions réelles** (longueur et largeur en mètres)
- 🔢 **Nombre de points WiFi** (1 à 10)
- 📡 **Fréquence du signal** (100-10000 MHz)
- 🎯 **Résolution de la heatmap** (1-50 pixels)

### 3. **Placement des Points WiFi**
- 🖱️ **Cliquez sur l'image** pour placer les points WiFi
- 📍 **Positions affichées** en temps réel en mètres
- 🗑️ **Bouton d'effacement** pour recommencer
- ⚠️ **Indicateur de progression** (points manquants)

### 4. **Génération de la Heatmap**
- ✅ **Vérification automatique** des prérequis
- 🔄 **Traitement en arrière-plan** avec barre de progression
- 🌡️ **Heatmap combinée** affichant le meilleur signal
- 💾 **Téléchargement** en haute résolution (PNG 300 DPI)

## 🔧 Fonctionnalités Techniques

### **Algorithme Multi-WiFi**
1. **Calcul individual** : Path loss calculé pour chaque point WiFi
2. **Sélection optimale** : Minimum path loss retenu pour chaque position
3. **Interpolation** : Grille lissée avec méthode cubique
4. **Visualisation** : Contours et échelle de couleurs

### **Gestion des Obstacles**
- **Détection des murs** : Analyse pixel par pixel
- **Calcul LOS** : Line-of-Sight entre transmetteurs et récepteurs
- **Comptage des traversées** : Nombre de murs traversés
- **Pénalité adaptative** : Impact sur le path loss

## 📁 Structure des Fichiers

```
v1/
├── main.py                     # 🚀 Point d'entrée (NOUVEAU)
├── config.py                   # ⚙️ Configuration multi-WiFi
├── test_multi_wifi.py         # 🧪 Tests des imports
├── 
├── models/
│   └── model_loader.py        # 🤖 Chargement ML
│
├── utils/
│   ├── image_processing.py    # 🖼️ Traitement d'images
│   └── path_loss_calculator.py # 📊 Calculs multi-WiFi (MODIFIÉ)
│
└── ui/
    ├── sidebar.py             # 📋 Interface paramètres (MODIFIÉ)
    ├── main_content.py        # 🖱️ Canvas multi-WiFi (MODIFIÉ)
    └── heatmap_generator.py   # 🌡️ Génération heatmaps (MODIFIÉ)
```

## 🎨 Interface Utilisateur

### **Sidebar Améliorée**
- 🔢 **Sélecteur de nombre de WiFi** (1-10)
- 📊 **Paramètres globaux** (fréquence, résolution)
- ✅ **Validation en temps réel**

### **Canvas Interactif**
- 🎯 **Mode multi-placement** avec cercles colorés
- 📍 **Affichage des coordonnées** en mètres
- 🗑️ **Effacement sélectif** ou total
- ⚠️ **Indicateurs visuels** de progression

### **Heatmap Évoluée**
- 🌈 **Légende colorée** pour chaque WiFi
- ⭐ **Symboles distinctifs** (étoiles colorées)
- 📏 **Échelle path loss** (dB)
- 🔍 **Contours isovaleurs** optionnels

## 🔍 Messages et Validation

### **Contrôles de Qualité**
- ❌ **Validation des fichiers** (formats supportés)
- 📐 **Vérification des dimensions** (limites raisonnables)
- 📍 **Contrôle des positions** (dans les limites du plan)
- 🔢 **Validation du nombre de WiFi** (entre 1 et 10)

### **Messages Informatifs**
- 📍 "WiFi 1 placé à: (3.45m, 2.78m)"
- ⚠️ "Il manque 2 point(s) WiFi. Cliquez sur l'image pour les placer."
- ✅ "3 point(s) WiFi placé(s)"
- 🛑 "Cliquez sur l'image pour placer les points WiFi."

## 💡 Conseils d'Utilisation

### **Optimisation des Performances**
- 🎯 **Résolution modérée** : Commencez avec step=5
- 📊 **Nombre raisonnable** : 2-4 WiFi pour la plupart des cas
- 🖼️ **Images optimisées** : Résolution 800x600 recommandée

### **Placement Stratégique**
- 🏢 **Répartition géographique** : Évitez les regroupements
- 🚪 **Évitez les murs épais** : Placez en espaces ouverts  
- 📡 **Couverture complémentaire** : Zones de faible signal différentes

### **Interprétation des Résultats**
- 🟢 **Vert/Bleu** : Excellent signal (faible path loss)
- 🟡 **Jaune/Orange** : Signal correct
- 🔴 **Rouge** : Signal faible (path loss élevé)
- ⚫ **Zones noires** : Murs (pas de signal)

## 🐛 Dépannage

### **Problèmes Courants**
- **"Points WiFi manquants"** → Cliquez sur l'image pour compléter
- **"Position hors limites"** → Vérifiez les dimensions du plan
- **"Aucun espace libre trouvé"** → Vérifiez la binarisation de l'image
- **"Modèle ML non chargé"** → Assurez-vous que `pathloss_predictor.pkl` existe

### **Performance**
- **Génération lente** → Réduisez la résolution (step plus grand)
- **Mémoire insuffisante** → Réduisez la taille de l'image
- **Erreur d'interpolation** → Augmentez le nombre de points (step plus petit)

## 🚀 Améliorations Futures

- 🔄 **Mode temps réel** : Mise à jour automatique lors du déplacement
- 🎛️ **Puissances variables** : Différentes puissances par WiFi
- 📱 **Export mobile** : Formats compatibles smartphones
- 🌐 **Mode 3D** : Heatmaps multi-étages
- 🤖 **Placement auto** : Algorithme d'optimisation automatique
