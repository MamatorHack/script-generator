from flask import Blueprint, jsonify

user_bp = Blueprint('user', __name__)

@user_bp.route('/ping')
def ping():
    """Endpoint de test pour vérifier que l'API fonctionne."""
    return jsonify({'message': 'pong'})

