#!/usr/bin/env python3
import requests
import json
import sys
import os

# Ajouter le chemin du projet
sys.path.insert(0, os.path.dirname(__file__))

def test_script_generation():
    """Test de la génération de scripts"""
    
    # Article de test
    article = """
    L'intelligence artificielle révolutionne notre quotidien. Les algorithmes d'apprentissage automatique 
    permettent aux machines de comprendre et d'analyser des données complexes à une vitesse inégalée. 
    Cette technologie transforme déjà de nombreux secteurs, de la médecine à l'automobile, en passant par 
    la finance et l'éducation. Les assistants virtuels deviennent plus intelligents et plus utiles chaque jour. 
    Il est temps d'embrasser cette révolution technologique pour améliorer notre productivité et notre qualité de vie.
    """
    
    # Test direct de la fonction sans serveur
    try:
        from src.routes.script_generator import split_text_into_parts, assign_emotions_to_parts
        
        print("=== Test de découpage de texte ===")
        parts = split_text_into_parts(article.strip())
        
        if parts:
            print("✅ Découpage réussi !")
            for i, (key, text) in enumerate(parts.items(), 1):
                print(f"Partie {i} ({key}): {len(text)} caractères")
                print(f"  Texte: {text[:100]}...")
                print()
            
            print("=== Test d'assignation d'émotions ===")
            emotions = assign_emotions_to_parts(parts)
            
            if emotions:
                print("✅ Assignation d'émotions réussie !")
                for key, emotion in emotions.items():
                    print(f"{key}: {emotion}")
                
                # Construire le résultat final
                script_result = []
                for i in range(1, 6):
                    part_key = f'partie{i}'
                    script_result.append({
                        'id': i,
                        'type': 'accroche' if i == 1 else 'call_to_action' if i == 5 else 'content',
                        'text': parts[part_key],
                        'emotion': emotions[part_key],
                        'character_count': len(parts[part_key]),
                        'duration_seconds': 12
                    })
                
                print("\n=== Résultat final ===")
                print(json.dumps(script_result, indent=2, ensure_ascii=False))
                
                return True
            else:
                print("❌ Erreur lors de l'assignation d'émotions")
                return False
        else:
            print("❌ Erreur lors du découpage")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_script_generation()
    sys.exit(0 if success else 1)

