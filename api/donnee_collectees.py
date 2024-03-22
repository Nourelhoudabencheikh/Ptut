from apifairy.decorators import other_responses
from flask import Blueprint, abort
from apifairy import authenticate, body, response
from flask import Blueprint, abort, request
from flask_httpauth import HTTPBasicAuth
from api.app import db
from api.models import Donnee_collectees
from api.schemas import Donnee_collecteesSchema, EmptySchema, UpdateDonnee_collecteesSchema
from api.auth import token_auth
from api.decorators import paginated_response
import sys

donnee_collectees = Blueprint('donnee_collectees', __name__)
donnee_collectee_schema = Donnee_collecteesSchema()
donnee_collectees_schema = Donnee_collecteesSchema(many=True)
update_montre_schema = UpdateDonnee_collecteesSchema(partial=True)

# Utiliser HTTPBasicAuth pour protéger les endpoints
auth = HTTPBasicAuth()


# Endpoint pour créer un nouveau Donnee_collectees
@donnee_collectees.route('/donnee_collectees', methods=['POST'])
@body(donnee_collectee_schema)
@authenticate(token_auth)
@response(donnee_collectee_schema, 201)
def new(args):
    """Créer des donnees_collectees"""
    donnee_collectee = Donnee_collectees(**args)
    print(donnee_collectee,file=sys.stderr)
    db.session.add(donnee_collectee)
    db.session.commit()
    return donnee_collectee

# Endpoint pour récupérer tous les montres
@donnee_collectees.route('/donnee_collectees', methods=['GET'])
@authenticate(token_auth)
@paginated_response(donnee_collectees_schema)
def all():
    """Récupérer tous les donnees_collectees"""
    return Donnee_collectees.select()

# Endpoint pour récupérer un donnee_collectee par son ID
@donnee_collectees.route('/donnee_collectees/<int:id>', methods=['GET'])
@authenticate(token_auth)
@response(donnee_collectee_schema)
@other_responses({404: 'donnee_collectee not found'})
def get(id):
    """Récupérer une donnee_collectee par son ID"""
    return db.session.get(Donnee_collectees, id) or abort(404)



# Endpoint pour supprimer un donnee_collectee
@donnee_collectees.route('/donnee_collectees/<int:id>', methods=['DELETE'])
@authenticate(token_auth)
@response(EmptySchema, 204)
@other_responses({404: 'donnee_collectee not found'})
def delete(id):
    """Supprimer une donnee_collectee"""
    donnee_collectee = db.session.get(Donnee_collectees, id)
    db.session.delete(donnee_collectee)
    db.session.commit()
    return {}