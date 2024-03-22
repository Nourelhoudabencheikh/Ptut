from apifairy.decorators import other_responses
from flask import Blueprint, abort
from apifairy import authenticate, body, response
from flask import Blueprint, abort, request
from flask_httpauth import HTTPBasicAuth
from api.app import db
from api.models import Resultat_journaliers
from api.schemas import Resultat_journaliersSchema, EmptySchema, UpdateResultat_journaliersSchema
from api.auth import token_auth
from api.decorators import paginated_response
import sys

resultat_journaliers = Blueprint('resultat_journaliers', __name__)
resultat_journalier_schema = Resultat_journaliersSchema()
resultat_journaliers_schema = Resultat_journaliersSchema(many=True)
update_resultat_journalier_schema = UpdateResultat_journaliersSchema(partial=True)

# Utiliser HTTPBasicAuth pour protéger les endpoints
auth = HTTPBasicAuth()


# Endpoint pour créer un nouveau resultat_journaliers
@resultat_journaliers.route('/resultat_journaliers', methods=['POST'])
@body(resultat_journalier_schema)
@authenticate(token_auth)
@response(resultat_journalier_schema, 201)
def new(args):
    """Créer des donnees_collectees"""
    resultat_journalier = Resultat_journaliers(**args)
    print(resultat_journalier,file=sys.stderr)
    db.session.add(resultat_journalier)
    db.session.commit()
    return resultat_journalier

# Endpoint pour récupérer tous les montres
@resultat_journaliers.route('/resultat_journaliers', methods=['GET'])
@authenticate(token_auth)
@paginated_response(resultat_journaliers_schema)
def all():
    """Récupérer tous les donnees_collectees"""
    return Resultat_journaliers.select()

# Endpoint pour récupérer un resultat_journalier par son ID
@resultat_journaliers.route('/resultat_journaliers/<int:id>', methods=['GET'])
@authenticate(token_auth)
@response(resultat_journalier_schema)
@other_responses({404: 'resultat_journalier not found'})
def get(id):
    """Récupérer une resultat_journalier par son ID"""
    return db.session.get(Resultat_journaliers, id) or abort(404)



