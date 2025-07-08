from flask import Blueprint, request, jsonify
from openai import OpenAI
import re
import json

script_bp = Blueprint('script', __name__)

# Configuration OpenAI
OPENAI_API_KEY = "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"
client = OpenAI(api_key=OPENAI_API_KEY)

# Liste des émotions officielles
EMOTIONS = ["happy", "sad", "angry", "fearful", "disgusted", "surprised", "neutral"]

def split_text_into_parts(text):
    """
    Découpe le texte en 5 parties selon les spécifications :
    - Partie 1 (accroche) : 50-100 caractères
    - Parties 2, 3, 4 (contenu) : 200-250 caractères chacune
    - Partie 5 (appel à l'action) : 50-100 caractères
    """
    
    # Utiliser OpenAI pour découper intelligemment le texte
    prompt = f"""
    Tu dois découper le texte suivant en exactement 5 parties selon ces critères STRICTS :
    
    1. Partie 1 (accroche) : EXACTEMENT entre 50 et 100 caractères - Une phrase d'accroche captivante
    2. Partie 2 (contenu) : EXACTEMENT entre 200 et 250 caractères - Premier point principal du contenu
    3. Partie 3 (contenu) : EXACTEMENT entre 200 et 250 caractères - Deuxième point principal du contenu
    4. Partie 4 (contenu) : EXACTEMENT entre 200 et 250 caractères - Troisième point principal du contenu
    5. Partie 5 (appel à l'action) : EXACTEMENT entre 50 et 100 caractères - Un appel à l'action engageant
    
    IMPORTANT : 
    - Respecte ABSOLUMENT les limites de caractères pour chaque partie
    - Compte les caractères avec précision
    - Si nécessaire, reformule ou ajoute du contenu pour atteindre les bonnes longueurs
    - Assure-toi que chaque partie soit complète et cohérente
    
    Texte à découper :
    {text}
    
    Réponds uniquement avec un JSON contenant les 5 parties :
    {{
        "partie1": "texte de l'accroche (50-100 caractères)",
        "partie2": "texte du contenu 1 (200-250 caractères)",
        "partie3": "texte du contenu 2 (200-250 caractères)", 
        "partie4": "texte du contenu 3 (200-250 caractères)",
        "partie5": "texte de l'appel à l'action (50-100 caractères)"
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        result = json.loads(response.choices[0].message.content)
        
        # Vérifier les contraintes de longueur
        validation_errors = []
        for i, (key, text_part) in enumerate(result.items(), 1):
            char_count = len(text_part)
            if i in [1, 5]:  # Accroche et appel à l'action
                if char_count < 50 or char_count > 100:
                    validation_errors.append(f"{key}: {char_count} caractères (attendu 50-100)")
            else:  # Contenu
                if char_count < 200 or char_count > 250:
                    validation_errors.append(f"{key}: {char_count} caractères (attendu 200-250)")
        
        if validation_errors:
            print(f"Erreurs de validation : {validation_errors}")
            # Essayer une deuxième fois avec des instructions plus strictes
            return split_text_into_parts_retry(text, validation_errors)
        
        return result
    except Exception as e:
        print(f"Erreur lors du découpage : {e}")
        return None

def split_text_into_parts_retry(text, previous_errors):
    """
    Deuxième tentative de découpage avec des instructions plus strictes
    """
    prompt = f"""
    ATTENTION : La tentative précédente a échoué avec ces erreurs : {previous_errors}
    
    Tu DOIS découper le texte suivant en exactement 5 parties avec des longueurs PARFAITEMENT respectées :
    
    1. Partie 1 (accroche) : OBLIGATOIREMENT entre 50 et 100 caractères (ni plus, ni moins)
    2. Partie 2 (contenu) : OBLIGATOIREMENT entre 200 et 250 caractères (ni plus, ni moins)
    3. Partie 3 (contenu) : OBLIGATOIREMENT entre 200 et 250 caractères (ni plus, ni moins)
    4. Partie 4 (contenu) : OBLIGATOIREMENT entre 200 et 250 caractères (ni plus, ni moins)
    5. Partie 5 (appel à l'action) : OBLIGATOIREMENT entre 50 et 100 caractères (ni plus, ni moins)
    
    STRATÉGIE :
    - Compte manuellement les caractères de chaque partie avant de répondre
    - Ajoute des mots ou reformule si c'est trop court
    - Raccourcis ou supprime des mots si c'est trop long
    - Assure-toi que le sens reste cohérent
    
    Texte à découper :
    {text}
    
    Réponds uniquement avec un JSON :
    {{
        "partie1": "texte exact avec 50-100 caractères",
        "partie2": "texte exact avec 200-250 caractères",
        "partie3": "texte exact avec 200-250 caractères", 
        "partie4": "texte exact avec 200-250 caractères",
        "partie5": "texte exact avec 50-100 caractères"
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3  # Moins de créativité, plus de précision
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        print(f"Erreur lors de la deuxième tentative : {e}")
        return None

def assign_emotions_to_parts(parts):
    """
    Assigne des émotions cohérentes à chaque partie en utilisant OpenAI
    """
    
    prompt = f"""
    Tu dois assigner une émotion appropriée à chaque partie de ce script vidéo.
    
    Émotions disponibles : {', '.join(EMOTIONS)}
    
    Parties du script :
    1. Accroche : "{parts['partie1']}"
    2. Contenu 1 : "{parts['partie2']}"
    3. Contenu 2 : "{parts['partie3']}"
    4. Contenu 3 : "{parts['partie4']}"
    5. Appel à l'action : "{parts['partie5']}"
    
    Assigne une émotion cohérente et appropriée au contenu de chaque partie.
    L'accroche devrait généralement être "surprised" ou "happy" pour capter l'attention.
    L'appel à l'action devrait être "happy" ou "neutral" pour encourager l'engagement.
    
    Réponds uniquement avec un JSON :
    {{
        "partie1": "emotion",
        "partie2": "emotion",
        "partie3": "emotion",
        "partie4": "emotion",
        "partie5": "emotion"
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        print(f"Erreur lors de l'assignation d'émotions : {e}")
        return None

@script_bp.route('/generate', methods=['POST'])
def generate_script():
    """
    Endpoint principal pour générer un script à partir d'un article
    """
    try:
        data = request.get_json()
        
        if not data or 'article' not in data:
            return jsonify({'error': 'Article manquant dans la requête'}), 400
        
        article = data['article']
        
        if len(article.strip()) < 50:
            return jsonify({'error': 'L\'article doit contenir au moins 50 caractères'}), 400
        
        # Étape 1 : Découper le texte en 5 parties
        parts = split_text_into_parts(article)
        if not parts:
            return jsonify({'error': 'Erreur lors du découpage du texte'}), 500
        
        # Étape 2 : Assigner des émotions à chaque partie
        emotions = assign_emotions_to_parts(parts)
        if not emotions:
            return jsonify({'error': 'Erreur lors de l\'assignation des émotions'}), 500
        
        # Étape 3 : Construire le résultat final
        script_result = []
        for i in range(1, 6):
            part_key = f'partie{i}'
            script_result.append({
                'id': i,
                'type': 'accroche' if i == 1 else 'call_to_action' if i == 5 else 'content',
                'text': parts[part_key],
                'emotion': emotions[part_key],
                'character_count': len(parts[part_key]),
                'duration_seconds': 12  # Durée estimée de 10-15 secondes
            })
        
        return jsonify({
            'success': True,
            'script': script_result,
            'total_parts': 5,
            'total_duration': 60  # 5 parties × 12 secondes
        })
        
    except Exception as e:
        return jsonify({'error': f'Erreur interne : {str(e)}'}), 500

@script_bp.route('/emotions', methods=['GET'])
def get_emotions():
    """
    Retourne la liste des émotions disponibles
    """
    return jsonify({
        'emotions': EMOTIONS,
        'description': {
            'happy': 'Joyeux, enthousiaste',
            'sad': 'Triste, mélancolique',
            'angry': 'Colère, frustration',
            'fearful': 'Peur, inquiétude',
            'disgusted': 'Dégoût, répulsion',
            'surprised': 'Surprise, étonnement',
            'neutral': 'Neutre, calme'
        }
    })

@script_bp.route('/validate', methods=['POST'])
def validate_script():
    """
    Valide un script généré et vérifie les contraintes
    """
    try:
        data = request.get_json()
        
        if not data or 'script' not in data:
            return jsonify({'error': 'Script manquant dans la requête'}), 400
        
        script = data['script']
        validation_errors = []
        
        for part in script:
            part_id = part.get('id')
            text = part.get('text', '')
            emotion = part.get('emotion')
            part_type = part.get('type')
            
            # Vérifier les contraintes de longueur
            char_count = len(text)
            if part_type in ['accroche', 'call_to_action']:
                if char_count < 50 or char_count > 100:
                    validation_errors.append(f"Partie {part_id}: longueur incorrecte ({char_count} caractères, attendu 50-100)")
            elif part_type == 'content':
                if char_count < 200 or char_count > 250:
                    validation_errors.append(f"Partie {part_id}: longueur incorrecte ({char_count} caractères, attendu 200-250)")
            
            # Vérifier l'émotion
            if emotion not in EMOTIONS:
                validation_errors.append(f"Partie {part_id}: émotion invalide '{emotion}'")
        
        return jsonify({
            'valid': len(validation_errors) == 0,
            'errors': validation_errors,
            'total_parts': len(script)
        })
        
    except Exception as e:
        return jsonify({'error': f'Erreur lors de la validation : {str(e)}'}), 500

