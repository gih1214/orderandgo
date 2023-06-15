from flask import render_template
from app.routes import adm_bp

@adm_bp.route('/adm',methods=['GET','POST'])
def index():
    return render_template('adm.html')