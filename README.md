# Script Generator

**Script Generator** est une application qui transforme automatiquement un article ou texte libre en **5 segments courts**, chacun enrichi d’une **émotion cohérente**.  
Ces scripts sont optimisés pour la génération audio/vidéo à partir d'avatars IA.

L’interface front-end (HTML) permet de déposer un texte, qui est ensuite traité par une **API Flask** exposée via `src/main.py`.

## Fonctionnalités principales

- Découpage automatique en 5 parties (hook, contenu, CTA)
- Attribution intelligente d’une émotion à chaque bloc
- Appel à l'API OpenAI pour l’analyse sémantique et émotionnelle
- Résultat structuré et prêt pour les modules de synthèse multimédia

---

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

---

## Structure

```
src/
  main.py            # Application Flask
  routes/
    script_generator.py
    user.py
  database/
    app.db
  models/
    user.py
  static/            # Fichiers front-end
```
