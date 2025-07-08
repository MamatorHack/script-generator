#!/bin/bash

# Script de démarrage pour le Générateur de Scripts Émotionnels
# Usage: ./start.sh

echo "🚀 Démarrage du Générateur de Scripts Émotionnels..."
echo ""

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Vérifier si l'environnement virtuel existe
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Erreur lors de la création de l'environnement virtuel."
        exit 1
    fi
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances si nécessaire
if [ ! -f "venv/pyvenv.cfg" ] || [ ! -d "venv/lib" ]; then
    echo "📚 Installation des dépendances..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ Erreur lors de l'installation des dépendances."
        exit 1
    fi
fi

# Vérifier que le fichier principal existe
if [ ! -f "src/main.py" ]; then
    echo "❌ Le fichier src/main.py n'existe pas."
    exit 1
fi

echo "✅ Environnement prêt !"
echo ""
echo "🌐 Démarrage du serveur..."
echo "📱 L'application sera accessible à l'adresse : http://localhost:8080"
echo ""
echo "Pour arrêter le serveur, appuyez sur Ctrl+C"
echo ""

# Démarrer l'application
python src/main.py

