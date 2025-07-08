# Script Generator

Cette application transforme un article en cinq segments accompagnés d'une émotion associée. Un front-end HTML appelle une API Flask exposée dans `src/main.py`.

## Installation

1. **Créer un environnement virtuel**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows : venv\Scripts\activate
   ```
2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```
3. **Définir la clé OpenAI**
   ```bash
   export OPENAI_API_KEY="votre-cle"  # Windows : $env:OPENAI_API_KEY="Votre clé API"
   ```
4. **Lancer l'application**
   ```bash
   python src/main.py
   ```
   L'interface est disponible sur [http://localhost:8080](http://localhost:8080).

## Structure

```
src/
  main.py            # Application Flask
  routes/
    script_generator.py
    user.py
  models/
    user.py
  static/            # Fichiers front-end
```
