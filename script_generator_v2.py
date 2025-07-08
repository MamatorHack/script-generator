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
    
    # Première étape : demander à OpenAI de créer le contenu pour chaque partie
    prompt = f"""
    À partir du texte suivant, tu dois créer 5 parties distinctes pour un script vidéo :

    Texte source : {text}

    Crée 5 parties avec le contenu suivant :
    1. Une accroche captivante qui résume l'idée principale
    2. Le premier point clé du contenu avec des détails
    3. Le deuxième point clé du contenu avec des détails  
    4. Le troisième point clé du contenu avec des détails
    5. Un appel à l'action engageant

    Réponds avec un JSON contenant le contenu de chaque partie (sans te soucier de la longueur pour l'instant) :
    {{
        "accroche": "contenu de l'accroche",
        "contenu1": "premier point détaillé",
        "contenu2": "deuxième point détaillé",
        "contenu3": "troisième point détaillé", 
        "appel_action": "appel à l'action"
    }}
    """
    
    try:
        # Étape 1 : Générer le contenu
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        content = json.loads(response.choices[0].message.content)
        
        # Étape 2 : Ajuster chaque partie pour respecter les contraintes de longueur
        final_parts = {}
        
        # Ajuster l'accroche (50-100 caractères)
        final_parts["partie1"] = adjust_text_length(content["accroche"], 50, 100, "accroche captivante")
        
        # Ajuster les contenus (200-250 caractères)
        final_parts["partie2"] = adjust_text_length(content["contenu1"], 200, 250, "contenu détaillé")
        final_parts["partie3"] = adjust_text_length(content["contenu2"], 200, 250, "contenu détaillé")
        final_parts["partie4"] = adjust_text_length(content["contenu3"], 200, 250, "contenu détaillé")
        
        # Ajuster l'appel à l'action (50-100 caractères)
        final_parts["partie5"] = adjust_text_length(content["appel_action"], 50, 100, "appel à l'action")
        
        return final_parts
        
    except Exception as e:
        print(f"Erreur lors du découpage : {e}")
        return None

def adjust_text_length(text, min_chars, max_chars, text_type):
    """
    Ajuste la longueur d'un texte pour respecter les contraintes
    """
    current_length = len(text)
    
    if min_chars <= current_length <= max_chars:
        return text
    
    if current_length < min_chars:
        # Texte trop court, demander à OpenAI de l'étendre
        prompt = f"""
        Le texte suivant est trop court ({current_length} caractères). 
        Tu dois l'étendre pour qu'il fasse EXACTEMENT entre {min_chars} et {max_chars} caractères.
        
        Type de texte : {text_type}
        Texte actuel : "{text}"
        
        Étends ce texte en gardant le même sens et le même style, mais en ajoutant des détails pertinents.
        Réponds uniquement avec le texte étendu, sans guillemets ni explications.
        """
    else:
        # Texte trop long, demander à OpenAI de le raccourcir
        prompt = f"""
        Le texte suivant est trop long ({current_length} caractères).
        Tu dois le raccourcir pour qu'il fasse EXACTEMENT entre {min_chars} et {max_chars} caractères.
        
        Type de texte : {text_type}
        Texte actuel : "{text}"
        
        Raccourcis ce texte en gardant l'essentiel du message et le même impact.
        Réponds uniquement avec le texte raccourci, sans guillemets ni explications.
        """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        
        adjusted_text = response.choices[0].message.content.strip()
        
        # Vérifier si l'ajustement a fonctionné
        if min_chars <= len(adjusted_text) <= max_chars:
            return adjusted_text
        else:
            # Si ça n'a pas marché, faire un ajustement manuel simple
            if len(adjusted_text) > max_chars:
                return adjusted_text[:max_chars-3] + "..."
            elif len(adjusted_text) < min_chars:
                # Ajouter des points de suspension ou répéter la fin
                padding_needed = min_chars - len(adjusted_text)
                return adjusted_text + " " * padding_needed
            
    except Exception as e:
        print(f"Erreur lors de l'ajustement : {e}")
        # Fallback : ajustement manuel
        if current_length > max_chars:
            return text[:max_chars-3] + "..."
        else:
            padding_needed = min_chars - current_length
            return text + " " * padding_needed

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

