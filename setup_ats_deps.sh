#!/usr/bin/env bash
set -e

echo "🔧 Installation des dépendances ATS"
echo "===================================="

# Activer l'environnement virtuel
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    echo "✅ Environnement virtuel activé"
else
    echo "❌ Environnement virtuel non trouvé. Créer d'abord avec: python -m venv .venv"
    exit 1
fi

# Installer pyresparser
echo "📦 Installation de pyresparser..."
pip install pyresparser

# Télécharger les données NLTK
echo "📊 Téléchargement des données NLTK..."
python3 -c "
import nltk
import os
try:
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True) 
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('maxent_ne_chunker', quiet=True)
    nltk.download('words', quiet=True)
    print('✅ Données NLTK téléchargées')
except Exception as e:
    print(f'⚠️  Erreur NLTK: {e}')
"

# Télécharger le modèle spaCy
echo "🧠 Téléchargement du modèle spaCy..."
python -m spacy download en_core_web_sm

# Vérifier pdftotext
if command -v pdftotext &> /dev/null; then
    echo "✅ pdftotext disponible"
else
    echo "⚠️  pdftotext non trouvé. Installer avec: sudo apt install poppler-utils"
fi

echo
echo "🎉 Configuration ATS terminée !"
echo "Vous pouvez maintenant exécuter: ./test_ats_friendly.sh" 