from apifairy.decorators import other_responses
from flask import Blueprint, abort
from apifairy import authenticate, body, response
from flask import Blueprint, abort, request
from flask_httpauth import HTTPBasicAuth
from api.app import db
from api.models import Montre
from api.schemas import MontreSchema, EmptySchema, UpdateMontreSchema
from api.auth import token_auth
from api.decorators import paginated_response
import sys

montres = Blueprint('montres', __name__)
montre_schema = MontreSchema()
montres_schema = MontreSchema(many=True)
update_montre_schema = UpdateMontreSchema(partial=True)

# Utiliser HTTPBasicAuth pour protéger les endpoints
auth = HTTPBasicAuth()

# Définir les permissions nécessaires pour accéder aux endpoints
# @auth.verify_password
# def verify_password(username, password):
#     montre = montre.query.filter_by(username=username).first()
#     if montre is None:
#         return False
#     if montre.verify_password(password):
#         return montre
#     return False

# Endpoint pour créer un nouveau montre
@montres.route('/montres', methods=['POST'])
@body(montre_schema)
@authenticate(token_auth)
@response(montre_schema, 201)
def new(args):
    """Créer un nouveau montre"""
    montre = Montre(**args)
    print(montre,file=sys.stderr)
    db.session.add(montre)
    db.session.commit()
    return montre

# Endpoint pour récupérer tous les montres
@montres.route('/montres', methods=['GET'])
@authenticate(token_auth)
@paginated_response(montres_schema)
def all():
    """Récupérer tous les montres"""
    return Montre.select()

# Endpoint pour récupérer un montre par son ID
@montres.route('/montres/<int:id>', methods=['GET'])
@authenticate(token_auth)
@response(montre_schema)
@other_responses({404: 'Montre not found'})
def get(id):
    """Récupérer une montre par son ID"""
    return db.session.get(Montre, id) or abort(404)

# Endpoint pour mettre à jour un montre
@montres.route('/montres/<int:id>', methods=['PUT'])
@authenticate(token_auth)
@response(montre_schema)
@body(update_montre_schema)
def update(data, id):
    """Mettre à jour un montre"""
    montre = db.session.get(Montre, id)
    montre.update(data)
    db.session.commit()
    return montre

# Endpoint pour supprimer un montre
@montres.route('/montres/<int:id>', methods=['DELETE'])
@authenticate(token_auth)
@response(EmptySchema, 204)
@other_responses({404: 'montre not found'})
def delete(id):
    """Supprimer un montre"""
    montre = db.session.get(Montre, id)
    db.session.delete(montre)
    db.session.commit()
    return {}