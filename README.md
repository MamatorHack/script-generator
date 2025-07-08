# Script Generator

Cette application transforme un article en cinq segments accompagnés d'une émotion associée. Un front-end HTML appelle une API Flask exposée dans `src/main.py`.

## Installation

1. **Créer un environnement virtuel**
   ```bat
   py -m venv venv
   venv\Scripts\activate
   ```
2. **Installer les dépendances**
   ```bat
   pip install -r requirements.txt
   ```
3. **Définir la clé OpenAI**
   ```bat
   set OPENAI_API_KEY="votre-cle"
   ```
4. **Lancer l'application**
   ```bat
   python src\main.py
   ```
   L'interface est disponible sur [http://localhost:8080](http://localhost:8080).
   Vous pouvez également lancer `start.bat` pour automatiser ces étapes.

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
