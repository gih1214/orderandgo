from flask import render_template, redirect, url_for
from app.routes import main_bp
from app.models.store import create_store, update_store
from flask_login import current_user, login_required


@main_bp.route('/')
@login_required
def index():
    return render_template('index.html')

