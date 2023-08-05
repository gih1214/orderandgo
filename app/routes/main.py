from flask import render_template
from app.routes import main_bp
from app.models.store import create_store, update_store

@main_bp.route('/')
def index():
    return render_template('index.html')
