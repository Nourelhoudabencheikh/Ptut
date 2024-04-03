from apifairy.decorators import other_responses
from apifairy import authenticate, body, response
from flask import Blueprint, abort, request, Response
from flask_httpauth import HTTPBasicAuth
from api.app import db
from api.models import Montre
from api.schemas import MontreSchema, EmptySchema, UpdateMontreSchema
from api.auth import token_auth
from api.decorators import paginated_response
import sys
from io import StringIO
import csv

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
    """Créer un nouvelle montre"""
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
    """Mettre à jour une montre"""
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
    """Supprimer une montre"""
    montre = db.session.get(Montre, id)
    db.session.delete(montre)
    db.session.commit()
    return {}

@montres.route('/montres/check/<int:id>', methods=['GET'])
@other_responses({404: 'montre not found'})
def checkMontre(id):
    montre = db.session.get(Montre, id)
    print(montre,file=sys.stderr)
    if montre:
         return {'exist': True}, 200    
    else:
        return {'exist': False}, 404 

# download the recording sorted by timestamp as a csv file
@montres.route('/montres/download', methods=["GET"])
def download():
    # Request username and token of recording
    username = request.args.get('username')

    # generate CSV file from recording
    def generate(username):
        # get selected data and write them in a list grouped by parenthesis
        with montres.app_context():
            if username != '':
                selectedData = db.query.order_by(db._timestamp).filter_by(_user=username)
    
            else:
                selectedData = db.query.order_by(db._timestamp)

            log = []
            for i in selectedData:
                log.append((i.id, i.montre, i.debut, i.fin, i.etat,
                            i.marque, i.patient_id))

        data = StringIO()
        w = csv.writer(data)

        # write header of CSV
        w.writerow(('id', 'montre', 'debut', 'fin', 'etat', 'marque', 'patient_id'))
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)

        # write each log item
        for item in log:
            w.writerow((
                item[0],
                item[1],
                item[2],
                item[3],
                item[4],
                item[5],
                item[6],
            
            ))
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

    # stream the response as the data is generated
    response = Response(generate(username), mimetype='text/csv')

    # add a filename
    response.headers.set("Content-Disposition", "attachment", filename=username + ".csv")
    return response