from flask import render_template, request, jsonify
from app.routes import auth_bp

from app.models.user import create_user, get_user_login

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = get_user_login(username, password)
        if user == False:
            print("로그인 실패")
            response = jsonify({'message': '로그인 실패, 일치하는 정보가 없습니다.'})
            response.status_code = 200
            return response
        print("로그인 성공", user)
        response = jsonify({'message': 'Success'})
        response.status_code = 200
        return response

@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        
        return render_template('/register.html')
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user = create_user(username, email, password)
        print("회원가입 성공", user)
        response = jsonify({'message': 'Success'})
        response.status_code = 200
        return response