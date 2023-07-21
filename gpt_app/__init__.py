# gpt_app/__init__.py
from flask import Blueprint

gpt_blueprint = Blueprint('gpt', __name__, template_folder='templates')

from gpt_app.blueprints import routes