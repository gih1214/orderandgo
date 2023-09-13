from flask import render_template, jsonify, request, session
import os

from app.routes import adm_bp
from app.models import db, Store, TableCategory, Table
# from app.models.user import create_user
from app.models.menu_category import create_main_category, create_sub_category
from app.models.store import create_store, delete_store, update_store
from app.models.menu import create_menu, create_menu_option, delete_menu, update_menu

@adm_bp.route('/')
def index():
    return render_template('adm.html')

####################
### 유저 시작 ###

'''
# 회원가입(유저 생성)
@adm_bp.route('/user', methods=['GET', 'POST'])
def create_user_py():
    # 회원가입 페이지로 옮긴 후 path 수정 필요
    #if request.method == 'GET':
    #    return render_template('/register.html')

    if request.method == 'POST':
        #print('Received JSON data:', user_data)
        user_data = request.get_json()
        
        user_id = user_data['user_id']
        password = user_data['password']
        name = user_data['name']
        birthday = user_data['birthday']
        tel = user_data['tel']
        email = user_data['email']
        address = user_data['address']
        user = create_user(user_id, password, name, birthday, tel, email, address)
        print("회원가입 성공", user)
        response = jsonify({'message': 'Success'})
        response.status_code = 200
        return response
        #return jsonify({'message': '사용자가 성공적으로 생성되었습니다.'}), 201
'''
        
@adm_bp.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    # 유저 조회 로직 수행
    # ...
    user_data = {'id': user_id, 'name': 'John Doe', 'email': 'john@example.com'}  # 예시 데이터
    return jsonify(user_data), 200

@adm_bp.route('/user/<user_id>', methods=['PATCH'])
def update_user(user_id):
    # 유저 업데이트 로직 수행
    # ...
    return jsonify({'message': 'User updated successfully'}), 200

@adm_bp.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    # 유저 삭제 로직 수행
    # ...
    return jsonify({'message': 'User deleted successfully'}), 204
### 유저 끝 ###
####################

####################
### 스토어 시작 ###


'''
#  스토어 생성
@adm_bp.route('/store', methods=['GET', 'POST'])
def create_store_py():
    # 매장 생성 페이지로 옮긴 후 path 수정 필요
    # if request.method == 'GET':
    #    return render_template('/register.html')

    if request.method == 'POST':
        store_data = request.get_json()
        
        #user_id = store_data['user_id']
        # 유저 아이디 코드 수정 필요 !!!
        user_id = 14
        name = store_data['name']
        address = store_data['address']
        tel = store_data['tel']
        manager_name = store_data['manager_name']
        manager_tel = store_data['manager_tel']
        logo_img = store_data['logo_img']
        store_image = store_data['store_image']
        main_description = store_data['main_description']
        sub_description = store_data['sub_description']

        store = create_store(user_id, name, address, tel, manager_name, manager_tel, logo_img, store_image, main_description, sub_description)
        print("매장생성 1차 성공", store)

        # # store 이미지 다시 넣기
        # store_image = request.files['store_image']
        # UPLOAD_FOLDER = 'app/static/images/user/'
        # upload_path = '{}{}/{}/store_img'.format(UPLOAD_FOLDER, user_id, store.id)
        # if not os.path.exists(upload_path):
        #     os.makedirs(upload_path)        
        # store_image.save(os.path.join(upload_path, store_image))
        # store_image_path = '{}/{}'.format(upload_path, store_image.filename)

        response = jsonify({'message': 'Success'})
        response.status_code = 200
        print('Received JSON data:', store_data)
        return response
        #return jsonify({'message': '매장이 성공적으로 생성되었습니다.'}), 201
'''

        
@adm_bp.route('/store/<store_id>', methods=['GET'])
def get_store_py(store_id):
    # 스토어 조회 로직 수행
    store_data = {'id': store_id, 'name': 'John Doe', 'email': 'john@example.com'}  # 예시 데이터
    return jsonify(store_data), 200

# 스토어 수정
@adm_bp.route('/store/<store_id>', methods=['PATCH'])
def update_store_py(store_id):
    # 스토어 업데이트 로직 수행
    if request.method == 'PATCH':
        store_data = request.get_json()
        
        #user_id = store_data['user_id']
        user_id = 14 # temp
        store_id = 2 # temp
        name = store_data['name']
        address = store_data['address']
        tel = store_data['tel']
        manager_name = store_data['manager_name']
        manager_tel = store_data['manager_tel']
        logo_img = store_data['logo_img']
        store_image = store_data['store_image']
        main_description = store_data['main_description']
        sub_description = store_data['sub_description']

        store = update_store(user_id, store_id, name, address, tel, manager_name, manager_tel, logo_img, store_image, main_description, sub_description)
        print("스토어 수정 1차 성공", store)

        response = jsonify({'message': 'Success'})
        response.status_code = 200
        print('Received JSON data:', store_data)
    return jsonify({'message': '스토어가 성공적으로 업데이트되었습니다.'}), 200

# 스토어 삭제
@adm_bp.route('/store/<store_id>', methods=['DELETE'])
def delete_store_py(store_id):
    if request.method == 'DELETE':
        delete_store(store_id)
        print('스토어 삭제 성공')
    return jsonify({'message': '스토어가 성공적으로 삭제되었습니다.'}), 204
### 스토어 끝 ###
####################


####################
### 메뉴 시작 ###

# 메뉴 생성
@adm_bp.route('/menu', methods=['GET', 'POST'])
def create_menu_py():
    # 메뉴 생성 페이지로 옮긴 후 path 수정 필요
    # if request.method == 'GET':
    #    return render_template('/register.html')

    if request.method == 'POST':
        menu_data = request.get_json()

        # store_id, menu_category_id 수정 필요
        name = menu_data['name']
        price = menu_data['price']
        image = menu_data['image']
        main_description = menu_data['main_description']
        sub_description = menu_data['sub_description']
        is_soldout = menu_data['is_soldout']
        store_id = 1 #menu_data['store_id']
        menu_category_id = menu_data['menu_category_id']
        menu = create_menu(name, price, image, main_description, sub_description, is_soldout, store_id, menu_category_id)
        print("메뉴생성 성공", menu)
        response = jsonify({'message': 'Success'})
        response.status_code = 200
        print('Received JSON data:', menu_data)
        return response

# 메뉴 조회
@adm_bp.route('/menu/<menu_id>', methods=['GET'])
def get_menu(menu_id):
    # 메뉴 조회 로직 수행
    # ...
    menu_data = {'id': menu_id, 'name': 'John Doe', 'email': 'john@example.com'}  # 예시 데이터
    return jsonify(menu_data), 200

# 메뉴 수정
@adm_bp.route('/menu/<menu_id>', methods=['PATCH'])
def update_menu_py(menu_id):
    if request.method == 'PATCH':
        menu_data = request.get_json()

        menu_id = 5 # temp

        name = menu_data['name']
        price = menu_data['price']
        image = menu_data['image']
        main_description = menu_data['main_description']
        sub_description = menu_data['sub_description']
        is_soldout = menu_data['is_soldout']
        menu = update_menu(menu_id, name, price, image, main_description, sub_description, is_soldout)
        
        print("메뉴수정 성공", menu)

        response = jsonify({'message': 'Success'})
        response.status_code = 200
        print('Received JSON data:', menu_data)

    return jsonify({'message': '메뉴가 성공적으로 업데이트되었습니다.'}), 200

# 메뉴 삭제
@adm_bp.route('/menu/<menu_id>', methods=['DELETE'])
def delete_menu_py(menu_id):
    if request.method == 'DELETE':
        delete_menu(menu_id)
        print('메뉴 삭제 성공')
        return jsonify({'message': '메뉴가 성공적으로 삭제되었습니다.'}), 204
### 메뉴 끝 ###
####################



####################
### 메뉴옵션 시작 ###
@adm_bp.route('/menu_option', methods=['POST'])
def create_menu_option_py():
    if request.method == 'POST':
        menu_option_data = request.get_json()
        # create_menu_option(name, price, description, store_id)
        name = menu_option_data['optionName']
        price = menu_option_data['optionPrice']
        description = menu_option_data['optionDescription']
        store_id = 1 #menu_option_data['store_id']
        menu_option = create_menu_option(name, price, description,store_id)
        print("메뉴생성 성공", menu_option)
        print('Received JSON data:', menu_option_data)
        return jsonify({'message': '메뉴 옵션이 성공적으로 생성되었습니다.'}), 201

@adm_bp.route('/menu_option/<menu_option_id>', methods=['GET'])
def get_menu_option(menu_option_id):
    # 메뉴옵션 조회 로직 수행
    # ...
    menu_option_data = {'id': menu_option_id, 'name': 'John Doe', 'email': 'john@example.com'}  # 예시 데이터
    return jsonify(menu_option_data), 200

@adm_bp.route('/menu_option/<menu_option_id>', methods=['PATCH'])
def update_menu_option(menu_option_id):
    # 메뉴옵션 업데이트 로직 수행
    # ...
    return jsonify({'message': '메뉴 옵션을 성공적으로 업데이트되었습니다.'}), 200

@adm_bp.route('/menu_option/<menu_option_id>', methods=['DELETE'])
def delete_menu_option(menu_option_id):
    # 메뉴옵션 삭제 로직 수행
    # ...
    return jsonify({'message': '메뉴 옵션을 성공적으로 삭제되었습니다.'}), 204
### 메뉴옵션 끝 ###
####################


####################
### 메뉴 메인 카테고리 시작 ###
@adm_bp.route('/menu_main_category', methods=['POST'])
def create_menu_main_category():
    # 메뉴 메인 카테고리 생성 로직 수행
    if request.method == 'POST':
        menu_main_category_data = request.get_json()
        # store_id  = menu_main_category_data['store_id']
        store_id = 1    # temp
        name = menu_main_category_data['mainCategoryName']
        main_category = create_main_category(store_id, name)
        #create_sub_category(main_category.id, '{}-1'.format(main_category.name))

    return jsonify({'message': '메뉴 메인 카테고리를 성공적으로 생성되었습니다.'}), 201

@adm_bp.route('/menu_main_category/<menu_main_category_id>', methods=['GET'])
def get_menu_main_category(menu_main_category_id):
    # 메뉴 메인 카테고리 조회 로직 수행
    # ...
    menu_main_category_data = {'id': menu_main_category_id, 'name': 'John Doe', 'email': 'john@example.com'}  # 예시 데이터
    return jsonify(menu_main_category_data), 200

@adm_bp.route('/menu_main_category/<menu_main_category_id>', methods=['PATCH'])
def update_menu_main_category(menu_main_category_id):
    # 메뉴 메인 카테고리 업데이트 로직 수행
    # ...
    return jsonify({'message': '메뉴 메인 카테고리를 성공적으로 업데이트되었습니다.'}), 200

@adm_bp.route('/menu_main_category/<menu_main_category_id>', methods=['DELETE'])
def delete_menu_main_category(menu_main_category_id):
    # 메뉴 메인 카테고리 삭제 로직 수행
    # ...
    return jsonify({'message': '메뉴 메인 카테고리를 성공적으로 삭제되었습니다.'}), 204
### 메뉴 메인 카테고리 끝 ###
####################

####################
### 메뉴 서브 카테고리 시작 ###
@adm_bp.route('/menu_sub_category', methods=['POST'])
def create_menu_sub_category():
    # 메뉴 서브 카테고리 생성 로직 수행
    menu_sub_category_data = request.get_json()
    main_category_id = menu_sub_category_data['mainCategoryId']
    name = menu_sub_category_data['subCategoryName']
    create_sub_category(main_category_id, name)

    return jsonify({'message': '메뉴 서브 카테고리를 성공적으로 생성되었습니다.'}), 201

@adm_bp.route('/menu_sub_category/<menu_sub_category_id>', methods=['GET'])
def get_menu_sub_category(menu_sub_category_id):
    # 메뉴 서브 카테고리 조회 로직 수행
    # ...
    menu_sub_category_data = {'id': menu_sub_category_id, 'name': 'John Doe', 'email': 'john@example.com'}  # 예시 데이터
    return jsonify(menu_sub_category_data), 200

@adm_bp.route('/menu_sub_category/<menu_sub_category_id>', methods=['PATCH'])
def update_menu_sub_category(menu_sub_category_id):
    # 메뉴 서브 카테고리 업데이트 로직 수행
    # ...
    return jsonify({'message': '메뉴 서브 카테고리를 성공적으로 업데이트되었습니다.'}), 200

@adm_bp.route('/menu_sub_category/<menu_sub_category_id>', methods=['DELETE'])
def delete_menu_sub_category(menu_sub_category_id):
    # 메뉴 서브 카테고리 삭제 로직 수행
    # ...
    return jsonify({'message': '메뉴 서브 카테고리를 성공적으로 삭제되었습니다.'}), 204
### 메뉴 서브 카테고리 끝 ###
####################

####################
### 테이블 카테고리 시작 ###
@adm_bp.route('/table_category', methods=['POST'])
def create_table_category():
    # 테이블 카테고리 생성 로직 수행
    table_category_data = request.get_json()
    store_id = int(table_category_data['storeId'])
    category_name = table_category_data['categoryName']
    print('Received JSON data:', table_category_data)

    store_id = 1    # temp

    table_category = TableCategory(store_id=store_id, category_name=category_name)
    db.session.add(table_category)
    db.session.commit()

    return jsonify({'message': '테이블 카테고리를 성공적으로 생성되었습니다.'}), 201

@adm_bp.route('/table_category/<table_category_id>', methods=['GET'])
def get_table_category(table_category_id):
    # 테이블 카테고리 조회 로직 수행
    # ...
    table_category_data = {'id': table_category_id, 'name': 'John Doe', 'email': 'john@example.com'}  # 예시 데이터
    return jsonify(table_category_data), 200

@adm_bp.route('/table_category/<table_category_id>', methods=['PATCH'])
def update_table_category(table_category_id):
    # 테이블 카테고리 업데이트 로직 수행
    # ...
    return jsonify({'message': '테이블 카테고리를 성공적으로 업데이트되었습니다.'}), 200

@adm_bp.route('/table_category/<table_category_id>', methods=['DELETE'])
def delete_table_category(table_category_id):
    # 테이블 카테고리 삭제 로직 수행
    # ...
    return jsonify({'message': '테이블 카테고리를 성공적으로 삭제되었습니다.'}), 204
### 테이블 카테고리 끝 ###
####################

####################
### 테이블 시작 ###
@adm_bp.route('/table', methods=['POST'])
def create_table():
    # 테이블 생성 로직 수행
    table_data = request.get_json()
    print('Received JSON data:', table_data)

    name = table_data['tableName']
    number = table_data['tableNumber']
    seat_count = table_data['seatCount']
    table_category_id = table_data['tableCategory']

    store_id = 1    # temp
    x_axis = 1    # temp
    y_axis = 1    # temp
    page = 1    # temp
    table_category_id=1 #temp

    table = Table(name=name, number=number, seat_count=seat_count, x_axis=x_axis, y_axis=y_axis, page=page, table_category_id=table_category_id)
    db.session.add(table)
    db.session.commit()

    return jsonify({'message': '테이블을 성공적으로 생성되었습니다.'}), 201

@adm_bp.route('/table/<table_id>', methods=['GET'])
def get_table(table_id):
    # 테이블 조회 로직 수행
    # ...
    table_data = {'id': table_id, 'name': 'John Doe', 'email': 'john@example.com'}  # 예시 데이터
    return jsonify(table_data), 200

@adm_bp.route('/table/<table_id>', methods=['PATCH'])
def update_table(table_id):
    # 테이블 업데이트 로직 수행
    # ...
    return jsonify({'message': '테이블을 성공적으로 업데이트되었습니다.'}), 200

@adm_bp.route('/table/<table_id>', methods=['DELETE'])
def delete_table(table_id):
    # 테이블 삭제 로직 수행
    # ...
    return jsonify({'message': '테이블을 성공적으로 삭제되었습니다.'}), 204
### 테이블 끝 ###
####################
