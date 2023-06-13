from flask import render_template
from app.routes import pos_bp

@pos_bp.route('/pos')
def index():
    return render_template('pos.html')