from flask import Blueprint

main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
pos_bp = Blueprint('pos', __name__, url_prefix='/pos')
adm_bp = Blueprint('adm', __name__, url_prefix='/adm')

from app.routes import main, auth, pos, adm