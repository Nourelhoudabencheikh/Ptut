from marshmallow import validate, validates, validates_schema, \
    ValidationError, post_dump, fields
from api import ma, db
from api.auth import token_auth
from api.models import Patient, User, Montre, Capteur,Donnee_collectees, Resultat_journaliers
from datetime import datetime



paginated_schema_cache = {}


class EmptySchema(ma.Schema):
    pass


class DateTimePaginationSchema(ma.Schema):
    class Meta:
        ordered = True

    limit = ma.Integer()
    offset = ma.Integer()
    after = ma.DateTime(load_only=True)
    count = ma.Integer(dump_only=True)
    total = ma.Integer(dump_only=True)

    @validates_schema
    def validate_schema(self, data, **kwargs):
        if data.get('offset') is not None and data.get('after') is not None:
            raise ValidationError('Cannot specify both offset and after')


class StringPaginationSchema(ma.Schema):
    class Meta:
        ordered = True

    limit = ma.Integer()
    offset = ma.Integer()
    after = ma.String(load_only=True)
    count = ma.Integer(dump_only=True)
    total = ma.Integer(dump_only=True)

    @validates_schema
    def validate_schema(self, data, **kwargs):
        if data.get('offset') is not None and data.get('after') is not None:
            raise ValidationError('Cannot specify both offset and after')


def PaginatedCollection(schema, pagination_schema=StringPaginationSchema):
    if schema in paginated_schema_cache:
        return paginated_schema_cache[schema]

    class PaginatedSchema(ma.Schema):
        class Meta:
            ordered = True

        pagination = ma.Nested(pagination_schema)
        data = ma.Nested(schema, many=True)

    PaginatedSchema.__name__ = 'Paginated{}'.format(schema.__class__.__name__)
    paginated_schema_cache[schema] = PaginatedSchema
    return PaginatedSchema


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        ordered = True

    id = ma.auto_field(dump_only=True)
    nom = ma.auto_field(required=True,
                             validate=validate.Length(min=3, max=64))
    prenom = ma.auto_field(required=True,
                             validate=validate.Length(min=3, max=64))
    dateNaissance = ma.auto_field(required=True,
                             validate=validate.Length(min=3, max=64))
    etat = ma.auto_field(required=True,
                             validate=validate.Length(min=3, max=64))

    email = ma.auto_field(required=True, validate=[validate.Length(max=120),
                                                   validate.Email()])
    password = ma.String(required=True, load_only=True,
                         validate=validate.Length(min=3))
    has_password = ma.Boolean(dump_only=True)
    

    @validates('nom')
    def validate_nom(self, value):
        if not value[0].isalpha():
            raise ValidationError('nom must start with a letter')
        user = token_auth.current_user()
        old_nom = user.nom if user else None
        if value != old_nom and \
                db.session.scalar(User.select().filter_by(nom=value)):
            raise ValidationError('Use a different nom.')

    @validates('email')
    def validate_email(self, value):
        user = token_auth.current_user()
        old_email = user.email if user else None
        if value != old_email and \
                db.session.scalar(User.select().filter_by(email=value)):
            raise ValidationError('Use a different email.')

    @post_dump
    def fix_datetimes(self, data, **kwargs):
        # data['first_seen'] += 'Z'
        # data['last_seen'] += 'Z'
        return data


class UpdateUserSchema(UserSchema):
    old_password = ma.String(load_only=True, validate=validate.Length(min=3))

    @validates('old_password')
    def validate_old_password(self, value):
        if not token_auth.current_user().verify_password(value):
            raise ValidationError('Password is incorrect')
        


class TokenSchema(ma.Schema):
    class Meta:
        ordered = True

    access_token = ma.String(required=True)
    refresh_token = ma.String()


class PasswordResetRequestSchema(ma.Schema):
    class Meta:
        ordered = True

    email = ma.String(required=True, validate=[validate.Length(max=120),
                                               validate.Email()])


class PasswordResetSchema(ma.Schema):
    class Meta:
        ordered = True

    token = ma.String(required=True)
    new_password = ma.String(required=True, validate=validate.Length(min=3))


class OAuth2Schema(ma.Schema):
    code = ma.String(required=True)
    state = ma.String(required=True)


class PatientSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Patient
        ordered = True

    id = ma.auto_field(dump_only=True)
    nom = ma.String(required=True)
    prenom = ma.String(required=True)
    dateNaissance = ma.auto_field(required=True)
    etat = ma.String(required=True)
    classe = ma.String(required=True)
    poids = ma.Float(required=True)
    taille = ma.Float(required=True)


class UpdatePatientSchema(PatientSchema):
    #id = ma.Integer()
    nom = ma.String(required=True)
    prenom = ma.String(required=True)
    dateNaissance = ma.auto_field(required=True)
    etat = ma.String(required=True)
    classe = ma.String(required=True)
    poids = ma.Float(required=True)
    taille = ma.Float(required=True)



class MontreSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Montre
        ordered = True

    id = ma.auto_field(dump_only=True)
    montre = ma.String(required=True)
    debut = ma.String(required=True)
    fin = ma.String(required=True)
    etat = ma.String(required=True)
    marque = ma.String(required=True)
    patient_id = ma.Integer(required=True)

  


class UpdateMontreSchema(MontreSchema):
    montre = ma.String(required=True)
    debut = ma.String(required=True)
    fin = ma.String(required=True)
    etat = ma.String(required=True)
    marque = ma.String(required=True)

class CapteurSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Capteur
        ordered = True

    id = ma.auto_field(dump_only=True)
    typeCapteur = ma.String(required=True)
    freqEchantillon = ma.Integer(required=True)
    montre_id = ma.Integer(required=True)

  


class UpdateCapteurSchema(CapteurSchema):
    typeCapteur = ma.String(required=True)
    freqEchantillon = ma.Integer(required=True)


class Donnee_collecteesSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Donnee_collectees
        ordered = True

    id = ma.auto_field(dump_only=True)
    dateTime = ma.String(required=True)
    accX = ma.Float(required=True)
    accY = ma.Float(required=True)
    accZ = ma.Float(required=True)
    gyrX = ma.Float(required=True)
    gyrY = ma.Float(required=True)
    gyrZ = ma.Float(required=True)
    bpm = ma.Float(required=True)
    montre_id = ma.Integer(required=True)

  


class UpdateDonnee_collecteesSchema(Donnee_collecteesSchema):
    accX = ma.Float(required=True)
    accY = ma.Float(required=True)
    accZ = ma.Float(required=True)
    gyrX = ma.Float(required=True)
    gyrY = ma.Float(required=True)
    gyrZ = ma.Float(required=True)
    bpm = ma.Float(required=True)

class Resultat_journaliersSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Resultat_journaliers
        ordered = True

    id = ma.auto_field(dump_only=True)
    nbAlerte = ma.Integer(required=True)
    intensiteSed = ma.Float(required=True)
    intensiteLeg = ma.Float(required=True)
    intesiteMod = ma.Float(required=True)
    intensiteVig = ma.Float(required=True)
    dureeHorsLigne = ma.Float(required=True)
    dureePort = ma.Float(required=True)
    date = ma.String(required=True)

    patient_id = ma.Integer(required=True)

  


class UpdateResultat_journaliersSchema(Resultat_journaliersSchema):
    nbAlerte = ma.Integer(required=True)
    intensiteSed = ma.Float(required=True)
    intensiteLeg = ma.Float(required=True)
    intesiteMod = ma.Float(required=True)
    intensiteVig = ma.Float(required=True)
    dureeHorsLigne = ma.Float(required=True)
    dureePort = ma.Float(required=True)
    date = ma.String(required=True)