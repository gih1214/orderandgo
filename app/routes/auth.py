from flask import render_template, request, jsonify
from flask_login import current_user, login_required
from app.routes import auth_bp

from app.models.user import create_admin_user, create_store_user, get_store_user_login, get_admin_user_login, update_store_logo_img

import os

# 로그인
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        if request.form.get('admin_tel') is not None:       # 관리자 로그인
            tel = request.form.get('admin_tel')
            password = request.form.get('password')
            print(tel, password)
            result = get_admin_user_login(tel, password)
        else:                                           # 스토어 로그인
            store_id = request.form.get('store_id')
            password = request.form.get('password')
            result = get_store_user_login(store_id, password)

        if result == False:
            print("로그인 실패")
            response = jsonify({'message': '로그인 실패, 일치하는 정보가 없습니다.'})
            response.status_code = 400
            return response
        
        print("@#$@#$@#", current_user.id)
        print("로그인 성공", result)
        response = jsonify({'message': 'Success'})
        response.status_code = 200

        return response


# 관리자 회원가입
@auth_bp.route("/register_admin", methods=['GET', 'POST'])
def register_admin_user():
    if request.method == 'GET':
        return render_template('/register.html')
    
    if request.method == 'POST':
        tel = request.form.get('tel')
        password = request.form.get('password')
        result = create_admin_user(tel, password)

        if result == False:
            print("회원가입 실패")
            response = jsonify({'message': '회원가입 실패'})
            response.status_code = 400
            return response
        
        print("회원가입 성공", result)
        response = jsonify({'message': 'Success'})
        response.status_code = 200
        return response
    

# 스토어 회원가입
@login_required
@auth_bp.route("/register_store", methods=['GET', 'POST'])
def register_store_user():
    if request.method == 'GET':
        return render_template('/store_create.html')
    
    if request.method == 'POST':
        user_id = current_user.id
        store_id = request.form.get('store_id')
        name = request.form.get('name')
        password = request.form.get('password')
        logo_img = ''
        result = create_store_user(user_id, store_id, password, name, logo_img)

        # store 이미지 넣기
        store_image = request.files['store_image']
        UPLOAD_FOLDER = 'app/static/images/user/'
        upload_path = '{}{}/{}/store_img'.format(UPLOAD_FOLDER, user_id, result.id)
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)        
        store_image.save(os.path.join(upload_path, store_image))
        store_image_path = '{}/{}'.format(upload_path, store_image.filename)

        update_store_logo_img(result, upload_path)

        if result == False:
            print("회원가입 실패")
            response = jsonify({'message': '회원가입 실패'})
            response.status_code = 400
            return response
        
        print("회원가입 성공", result)
        response = jsonify({'message': 'Success'})
        response.status_code = 200
        return response
    
