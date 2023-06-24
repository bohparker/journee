from flask import Blueprint

bp_views = Blueprint('bp_views', __name__)

from . import views