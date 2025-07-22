import os
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_login import current_user

from .api import *
from .api import blueprints

# from .api import (
#     companies,
#     stores,
#     users,
#     menus,
#     coas,
#     vendors,
#     recipes,
#     tables,
#     users_stores
#     )

# https://flask.palletsprojects.com/en/2.0.x/patterns/appfactories/


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    CORS(app)


    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='postgresql://postgres:postgres@db:5432/erp_main',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=False
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

    # capture current user for change audit => db
    @app.before_request
    def set_audit_user():
        if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
            db.session.execute("SET LOCAL app.current_user = %s", [str(current_user.id)])   


    for bp in blueprints:
        app.register_blueprint(bp)
    # app.register_blueprint(users.bp)
    # app.register_blueprint(menus.bp)
    # app.register_blueprint(coas.bp)
    # app.register_blueprint(products.bp)
    # app.register_blueprint(locations.bp)
    # app.register_blueprint(recipes.bp)
    # app.register_blueprint(companies.bp)
    # app.register_blueprint(stores.bp)
    # app.register_blueprint(vendors.bp)
    # app.register_blueprint(tables.bp)
    # app.register_blueprint(users_stores.bp)


    def list_routes(app):
        import urllib
        output = []
        for rule in app.url_map.iter_rules():
            methods = ','.join(rule.methods)
            line = urllib.parse.unquote(f"{rule.endpoint:30s} {methods:20s} {str(rule)}")
            output.append(line)
        for line in sorted(output):
            print(line)

    # After app creation and blueprint registration:
    list_routes(app)

    return app
