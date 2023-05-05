from flask import Blueprint, render_template
from app.routes import auth_bp

@auth_bp.route('/login')
def login():
    return render_template('login.html')