from flask import Blueprint

main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
pos_bp = Blueprint('pos', __name__)
adm_bp = Blueprint('adm', __name__)

from app.routes import main, auth, pos, adm