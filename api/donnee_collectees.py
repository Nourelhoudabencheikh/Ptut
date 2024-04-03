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
import pandas as pd
import numpy as np
from pickle import load

donnee_collectees = Blueprint('donnee_collectees', __name__)
donnee_collectee_schema = Donnee_collecteesSchema()
donnee_collectees_schema = Donnee_collecteesSchema(many=True)
update_montre_schema = UpdateDonnee_collecteesSchema(partial=True)

# Utiliser HTTPBasicAuth pour protéger les endpoints
auth = HTTPBasicAuth()

x_list=[]
y_list=[]
z_list=[]
j=0
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


@donnee_collectees.route('/donnee_collectees/json', methods=['POST'])
def json_post():


    if request.is_json:
        req= request.get_json()
        for i in range(len(req)):
            _timestamp=req[i]['timestamp']
            _montre_id=req[i]['montre_id']
            _accX=req[i]['accX']
            _accY=req[i]['accY']
            _accZ=req[i]['accZ']
            _gyrX=req[i]['gyrX']
            _gyrY=req[i]['gyrY']
            _gyrZ=req[i]['gyrZ']
            _bpm=req[i]['bpm']

            

            global x_list, y_list, z_list, j

            x_list.append(_accX)
            y_list.append(_accY)
            z_list.append(_accZ)

            if j==30:
                df=pd.DataFrame()
                df=calculate_time_features(df, x_list, y_list, z_list)
                j=0


            donnee = Donnee_collectees(dateTime=_timestamp, 
                                       accX=_accX,accY=_accY,accZ=_accZ,gyrX=_gyrX,gyrY=_gyrY,gyrZ=_gyrZ,bpm=_bpm,montre_id=_montre_id)
            db.session.add(donnee)
            db.session.commit()

        return {'message': 'données reçues avec succées '}, 200    
    else: 
        return {'message': 'erreur de reception de données  '}, 400  




def calculate_time_features(data, x_list, y_list, z_list):
    #mean
    data['x_mean'] = pd.Series(x_list).apply(lambda x: x.mean())
    data['y_mean'] = pd.Series(y_list).apply(lambda x: x.mean())
    data['z_mean'] = pd.Series(z_list).apply(lambda x: x.mean())
    #std dev
    data['x_std'] = pd.Series(x_list).apply(lambda x: x.std())
    data['y_std'] = pd.Series(y_list).apply(lambda x: x.std())
    data['z_std'] = pd.Series(z_list).apply(lambda x: x.std())
    #min
    data['x_min'] = pd.Series(x_list).apply(lambda x: x.min())
    data['y_min'] = pd.Series(y_list).apply(lambda x: x.min())
    data['z_min'] = pd.Series(z_list).apply(lambda x: x.min())
    #max
    data['x_max'] = pd.Series(x_list).apply(lambda x: x.max())
    data['y_max'] = pd.Series(y_list).apply(lambda x: x.max())
    data['z_max'] = pd.Series(z_list).apply(lambda x: x.max())
    #covariance
    data['x_cov'] = pd.Series(x_list).apply(lambda x: x.cov())
    data['y_cov'] = pd.Series(y_list).apply(lambda x: x.cov())
    data['z_cov'] = pd.Series(z_list).apply(lambda x: x.cov())
    #10th Percentile
    data['x_10_perc'] = pd.Series(x_list).apply(lambda x: np.percentile(x, 10))
    data['y_10_perc'] = pd.Series(y_list).apply(lambda x: np.percentile(x, 10))
    data['z_10_perc'] = pd.Series(z_list).apply(lambda x: np.percentile(x, 10))
    #75th Percentile
    data['x_75_perc'] = pd.Series(x_list).apply(lambda x: np.percentile(x, 75))
    data['y_75_perc'] = pd.Series(y_list).apply(lambda x: np.percentile(x, 75))
    data['z_75_perc'] = pd.Series(z_list).apply(lambda x: np.percentile(x, 75))
    #90th Percentile
    data['x_90_perc'] = pd.Series(x_list).apply(lambda x: np.percentile(x, 90))
    data['y_90_perc'] = pd.Series(y_list).apply(lambda x: np.percentile(x, 90))
    data['z_90_perc'] = pd.Series(z_list).apply(lambda x: np.percentile(x, 90))
    return data
