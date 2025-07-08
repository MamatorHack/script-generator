# Générateur de Scripts Émotionnels

## Description

Cette application transforme automatiquement n'importe quel article en script vidéo structuré avec des émotions associées. Elle utilise l'intelligence artificielle (OpenAI GPT-3.5) pour découper le texte en 5 parties optimisées pour la création de vidéos émotionnelles.

## Fonctionnalités

### Structure du Script Généré

L'application génère automatiquement 5 parties :

1. **Partie 1 - Accroche** (50-100 caractères)
   - Phrase captivante pour capter l'attention
   - Émotion généralement "surprised" ou "happy"

2. **Parties 2, 3, 4 - Contenu** (200-250 caractères chacune)
   - Points clés du contenu avec détails
   - Émotions variées selon le contexte

3. **Partie 5 - Appel à l'action** (50-100 caractères)
   - Message engageant pour encourager l'action
   - Émotion généralement "happy" ou "neutral"

### Émotions Disponibles

- **Happy** : Joyeux, enthousiaste
- **Sad** : Triste, mélancolique
- **Angry** : Colère, frustration
- **Fearful** : Peur, inquiétude
- **Disgusted** : Dégoût, répulsion
- **Surprised** : Surprise, étonnement
- **Neutral** : Neutre, calme

## Installation

### Prérequis

- Python 3.11+
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner ou télécharger le projet**
   ```bash
   # Si vous avez git
   git clone <url-du-projet>
   cd script_generator
   
   # Ou extraire l'archive téléchargée
   ```

2. **Créer et activer l'environnement virtuel**
   ```bash
   python -m venv venv
   
   # Sur Windows
   venv\\Scripts\\activate
   
   # Sur macOS/Linux
   source venv/bin/activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration de l'API OpenAI**
   
   L'application utilise une clé API OpenAI intégrée pour la démonstration. Pour une utilisation en production, vous devriez :
   
   - Obtenir votre propre clé API sur [OpenAI Platform](https://platform.openai.com/)
   - Remplacer la clé dans le fichier `src/routes/script_generator.py` ligne 10
   - Ou mieux, utiliser une variable d'environnement :
   
   ```python
   import os
   OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'votre-clé-par-défaut')
   ```

## Utilisation

### Démarrage de l'application

1. **Activer l'environnement virtuel** (si pas déjà fait)
   ```bash
   # Sur Windows
   venv\\Scripts\\activate
   
   # Sur macOS/Linux
   source venv/bin/activate
   ```

2. **Lancer le serveur**
   ```bash
   python src/main.py
   ```

3. **Accéder à l'application**
   
   Ouvrez votre navigateur et allez à : `http://localhost:5000`

### Interface utilisateur

1. **Saisie de l'article**
   - Collez votre article dans la zone de texte
   - Minimum 50 caractères requis
   - Le compteur de caractères s'affiche en temps réel

2. **Génération du script**
   - Cliquez sur "Générer le Script"
   - L'IA analyse votre texte (peut prendre 10-30 secondes)
   - Le script structuré s'affiche avec les émotions

3. **Exploitation des résultats**
   - Visualisez les 5 parties avec leurs émotions
   - Téléchargez le script au format JSON
   - Créez un nouveau script avec "Nouveau Script"

### Format de sortie JSON

```json
{
  "success": true,
  "script": [
    {
      "id": 1,
      "type": "accroche",
      "text": "Votre accroche captivante",
      "emotion": "surprised",
      "character_count": 82,
      "duration_seconds": 12
    },
    // ... autres parties
  ],
  "total_parts": 5,
  "total_duration": 60
}
```

## API REST

L'application expose également une API REST pour l'intégration dans d'autres systèmes :

### Endpoints disponibles

#### POST /api/script/generate
Génère un script à partir d'un article.

**Requête :**
```json
{
  "article": "Votre article ici..."
}
```

**Réponse :**
```json
{
  "success": true,
  "script": [...],
  "total_parts": 5,
  "total_duration": 60
}
```

#### GET /api/script/emotions
Retourne la liste des émotions disponibles.

#### POST /api/script/validate
Valide un script généré.

### Exemples d'utilisation de l'API

```python
import requests

# Générer un script
response = requests.post('http://localhost:5000/api/script/generate', 
                        json={'article': 'Votre article...'})
script = response.json()

# Obtenir les émotions
emotions = requests.get('http://localhost:5000/api/script/emotions').json()
```

```javascript
// Générer un script en JavaScript
fetch('/api/script/generate', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({article: 'Votre article...'})
})
.then(response => response.json())
.then(data => console.log(data));
```

## Architecture technique

### Structure du projet

```
script_generator/
├── src/
│   ├── main.py              # Point d'entrée de l'application
│   ├── routes/
│   │   ├── script_generator.py  # API de génération de scripts
│   │   └── user.py          # Routes utilisateur (template)
│   ├── models/
│   │   └── user.py          # Modèles de données (template)
│   ├── static/
│   │   ├── index.html       # Interface utilisateur
│   │   ├── styles.css       # Styles CSS
│   │   └── script.js        # Logique JavaScript
│   └── database/
│       └── app.db           # Base de données SQLite
├── venv/                    # Environnement virtuel
├── requirements.txt         # Dépendances Python
├── test_api.py             # Tests de l'API
└── README.md               # Cette documentation
```

### Technologies utilisées

- **Backend** : Flask (Python)
- **Frontend** : HTML5, CSS3, JavaScript (Vanilla)
- **IA** : OpenAI GPT-3.5 Turbo
- **Base de données** : SQLite (pour les extensions futures)
- **Styling** : CSS moderne avec variables et animations

### Logique de génération

1. **Analyse du texte** : L'IA analyse le contenu et identifie les points clés
2. **Découpage intelligent** : Le texte est divisé en 5 parties selon les contraintes
3. **Ajustement des longueurs** : Chaque partie est ajustée pour respecter les limites de caractères
4. **Attribution d'émotions** : L'IA assigne des émotions cohérentes selon le contenu
5. **Validation** : Le système vérifie que toutes les contraintes sont respectées

## Dépannage

### Problèmes courants

1. **Erreur "Module not found"**
   - Vérifiez que l'environnement virtuel est activé
   - Réinstallez les dépendances : `pip install -r requirements.txt`

2. **Erreur de connexion OpenAI**
   - Vérifiez votre connexion internet
   - Vérifiez que la clé API est valide
   - Consultez les logs du serveur pour plus de détails

3. **Port déjà utilisé**
   - Changez le port dans `src/main.py` ligne 46
   - Ou arrêtez le processus utilisant le port 5000

4. **Interface ne se charge pas**
   - Vérifiez que le serveur Flask est démarré
   - Consultez la console du navigateur pour les erreurs JavaScript

### Logs et débogage

- Les logs du serveur s'affichent dans le terminal
- Activez le mode debug en modifiant `debug=True` dans `main.py`
- Utilisez les outils de développement du navigateur (F12)

## Limitations

- **Quota OpenAI** : L'utilisation intensive peut atteindre les limites de l'API
- **Langue** : Optimisé pour le français, peut fonctionner en anglais
- **Longueur** : Articles recommandés entre 200 et 2000 caractères
- **Connexion** : Nécessite une connexion internet pour l'API OpenAI

## Évolutions possibles

### Fonctionnalités futures

1. **Support multilingue** : Détection automatique de la langue
2. **Personnalisation** : Ajustement des longueurs de parties
3. **Templates** : Modèles prédéfinis selon le type de contenu
4. **Historique** : Sauvegarde des scripts générés
5. **Export** : Formats supplémentaires (PDF, Word, etc.)
6. **Intégration** : Connexion directe avec les outils de montage vidéo

### Améliorations techniques

1. **Base de données** : Stockage des scripts et utilisateurs
2. **Authentification** : Système de comptes utilisateur
3. **Cache** : Mise en cache des résultats pour améliorer les performances
4. **Tests** : Suite de tests automatisés complète
5. **Docker** : Conteneurisation pour un déploiement facile

## Support

Pour toute question ou problème :

1. Consultez cette documentation
2. Vérifiez les logs d'erreur
3. Testez avec un article simple
4. Contactez le support technique

## Licence

Ce projet est fourni à des fins de démonstration. Veuillez respecter les conditions d'utilisation d'OpenAI pour l'API.

---

**Version** : 1.0  
**Date** : Juillet 2025  
**Auteur** : Script Generator AI Team

