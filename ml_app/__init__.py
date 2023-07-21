# ml_app/__init__.py
from flask import Blueprint

ml_app_blueprint = Blueprint('ml_app', __name__, template_folder='templates', static_folder='static')

from ml_app.blueprints import routes