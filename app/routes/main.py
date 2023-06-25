from flask import render_template
from app.routes import main_bp

@main_bp.route('/')
def index():
    print('실행됨')
    return render_template('index.html')
