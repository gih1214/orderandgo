from flask import Blueprint, render_template, request, session, jsonify
from app.routes import auth_bp
from app.models import User
from app.models.user import create_user

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        return 'response'

@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('/register.html')
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        print(username, email, password)
        user = create_user(username, email, password)
        print("회원가입 성공", user)
        response = jsonify({'message': 'Success'})
        response.status_code = 200
        return response