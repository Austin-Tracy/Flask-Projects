# pm_app/blueprints/__init__.py
from flask import Blueprint

bp = Blueprint("main", __name__)

from pm_app.blueprints import routes