from flask_sqlalchemy import SQLAlchemy

# Instance globale de la base de données
# Elle sera initialisée dans main.py

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

