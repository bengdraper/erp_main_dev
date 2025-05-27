import os
from flask import Flask
from flask_migrate import Migrate

from .api import *

from .api import (
    menus_test,
    companies,
    stores,
    users
    )

# https://flask.palletsprojects.com/en/2.0.x/patterns/appfactories/


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='postgresql://postgres:postgres@db:5432/erp_main',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .models import db
    db.init_app(app)
    migrate = Migrate(app, db)

    # from .api import users
    app.register_blueprint(users.bp)
    app.register_blueprint(menus_test.bp)
    app.register_blueprint(companies.bp)
    app.register_blueprint(stores.bp)

    return app
