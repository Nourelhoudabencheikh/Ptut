# tdah-api

API Flask qui réprésente le back end dans le projet de gestion de l'agitation motrice des enfants atteinds de TDAH.

## Déploiement sur l'ordinateur

Suivez ces étapes si vous souhaitez exécuter cette application sur votre ordinateur.

### Cloner le projet

```bash
git clone https://github.com/ibtraore/tdah-api.git
cd tdah-api
cp .env.example .env
```

### Environnement virtuel et dépendances

Créer un environnement virtuel

Windows

```bash
> py -3 -m venv .venv
```

macOS/Linux

```bash
> python3 -m venv .venv
```

Activer l'environnement virtuel

Windows

```bash
> .venv\Scripts\activate
```

macOS/Linux

```bash
> ..venv/bin/activate
```

Installer les dépendances sur l'environnement virtuel

```bash
pip install -r requirements.txt
```

### Base de données:

Exécution des migrations et insertion de quelques utilisateurs fictifs

```bash
alembic upgrade head
flask fake users 10
```
Exemple de création d'une nouvelle migration 

```bash
alembic revision -m "create table patient"
```

La base de donées par défaut est SQLite, pour modifier il faut définir le paramètre `DATABASE_URL` dans le fichier `.env` comme suit :

MySQL

```bash
pip install mysql-connector-python
DATABASE_URL = "mysql+mysqlconnector://username:password@hostname/database"
```

PostgreSQL

```bash
DATABASE_URL = "postgresql://username:password@hostname/database"
```

### Exécuter l'application avec le serveur web de développement Flask:

```bash
flask run
```

L'application fonctionne sur `localhost:5000`. Vous pouvez accéder à la documentation de l'API
à `http://localhost:5000/docs`.

## Ajouter une nouvelle entité

Pour ajouter une nouvelle entité (Par exemple patient):

1. Créer le fichier `patients.py` dans le dossier api :
    - Définir les endpoints.
    - Définir les permissions necessaires pour accéder aux endpoints.
2. Déclarer l'entité dans le fichier `app.py` :
    - ```bash
        from api.patients import patients
        app.register_blueprint(patients, url_prefix='/api')
        ```
3. Créer la classe de l'entité dans le fichier `models.py`
4. Créer une migration liée à l'entité pour la création dans la base de données
5. Déclarer l'entité dans le fichier `config.py`, comme suit:
    - APIFAIRY_TAGS = ['tokens', 'users', 'patients']
6. Définir les tests dans le dossiers `tests` (Optionel)
7. Exécuter l'application
    
    