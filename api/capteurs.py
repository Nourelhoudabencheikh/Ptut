from apifairy.decorators import other_responses
from flask import Blueprint, abort
from apifairy import authenticate, body, response
from flask import Blueprint, abort, request
from flask_httpauth import HTTPBasicAuth
from api.app import db
from api.models import Capteur
from api.schemas import CapteurSchema, CapteurSchema, UpdateCapteurSchema, EmptySchema
from api.auth import token_auth
from api.decorators import paginated_response
import sys

capteurs = Blueprint('capteurs', __name__)
capteur_schema = CapteurSchema()
capteurs_schema = CapteurSchema(many=True)
update_capteur_schema = UpdateCapteurSchema(partial=True)

# Utiliser HTTPBasicAuth pour protéger les endpoints
auth = HTTPBasicAuth()

# Définir les permissions nécessaires pour accéder aux endpoints
# @auth.verify_password
# def verify_password(username, password):
#     capteur = capteur.query.filter_by(username=username).first()
#     if capteur is None:
#         return False
#     if capteur.verify_password(password):
#         return capteur
#     return False

# Endpoint pour créer un nouveau capteur
@capteurs.route('/capteurs', methods=['POST'])
@body(capteur_schema)
@authenticate(token_auth)
@response(capteur_schema, 201)
def new(args):
    """Créer un nouveau capteur"""
    capteur = Capteur(**args)
    print(capteur,file=sys.stderr)
    db.session.add(capteur)
    db.session.commit()
    return capteur

# Endpoint pour récupérer tous les capteurs
@capteurs.route('/capteurs', methods=['GET'])
@authenticate(token_auth)
@paginated_response(capteurs_schema)
def all():
    """Récupérer tous les capteurs"""
    return Capteur.select()

# Endpoint pour récupérer un capteur par son ID
@capteurs.route('/capteurs/<int:id>', methods=['GET'])
@authenticate(token_auth)
@response(capteur_schema)
@other_responses({404: 'capteur not found'})
def get(id):
    """Récupérer un capteur par son ID"""
    return db.session.get(Capteur, id) or abort(404)

# Endpoint pour mettre à jour un capteur
@capteurs.route('/capteurs/<int:id>', methods=['PUT'])
@authenticate(token_auth)
@response(capteur_schema)
@body(update_capteur_schema)
def update(data, id):
    """Mettre à jour un capteur"""
    capteur = db.session.get(Capteur, id)
    capteur.update(data)
    db.session.commit()
    return capteur

# Endpoint pour supprimer un capteur
@capteurs.route('/capteurs/<int:id>', methods=['DELETE'])
@authenticate(token_auth)
@response(EmptySchema, 204)
@other_responses({404: 'capteur not found'})
def delete(id):
    """Supprimer un capteur"""
    capteur = db.session.get(Capteur, id)
    db.session.delete(capteur)
    db.session.commit()
    return {}