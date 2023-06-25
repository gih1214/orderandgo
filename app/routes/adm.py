from flask import render_template, jsonify, request
from app.routes import adm_bp

@adm_bp.route('/')
def index():
    return render_template('adm.html')

####################
### 유저 시작 ###

# 회원가입(유저 생성)
# 회원가입 페이지로 옮긴 후 path 수정 필요 !!
@adm_bp.route('/user', methods=['GET', 'POST'])
def create_user():
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
        #print(birthday)
        print('여기까진 옴')
        user = create_user(user_id, password, name, birthday, tel, email, address)
        print("회원가입 성공", user)
        response = jsonify({'message': 'Success'})
        response.status_code = 200
        return response
        #return jsonify({'message': '사용자가 성공적으로 생성되었습니다.'}), 201

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
@adm_bp.route('/store', methods=['POST'])
def create_store():
    # 스토어 생성 로직 수행
    # ...
    store_data = request.get_json()
    print('Received JSON data:', store_data)
    return jsonify({'message': '사용자가 성공적으로 생성되었습니다.'}), 201

@adm_bp.route('/store/<store_id>', methods=['GET'])
def get_store(store_id):
    # 스토어 조회 로직 수행
    # ...
    store_data = {'id': store_id, 'name': 'John Doe', 'email': 'john@example.com'}  # 예시 데이터
    return jsonify(store_data), 200

@adm_bp.route('/store/<store_id>', methods=['PATCH'])
def update_store(store_id):
    # 스토어 업데이트 로직 수행
    # ...
    return jsonify({'message': '스토어가 성공적으로 업데이트되었습니다.'}), 200

@adm_bp.route('/store/<store_id>', methods=['DELETE'])
def delete_store(store_id):
    # 스토어 삭제 로직 수행
    # ...
    return jsonify({'message': '스토어가 성공적으로 삭제되었습니다.'}), 204
### 스토어 끝 ###
####################


####################
### 메뉴 시작 ###
@adm_bp.route('/menu', methods=['POST'])
def create_menu():
    # 메뉴 생성 로직 수행
    # ...
    menu_data = request.get_json()
    print('Received JSON data:', menu_data)
    return jsonify({'message': '메뉴가 성공적으로 생성되었습니다.'}), 201

@adm_bp.route('/menu/<menu_id>', methods=['GET'])
def get_menu(menu_id):
    # 메뉴 조회 로직 수행
    # ...
    menu_data = {'id': menu_id, 'name': 'John Doe', 'email': 'john@example.com'}  # 예시 데이터
    return jsonify(menu_data), 200

@adm_bp.route('/menu/<menu_id>', methods=['PATCH'])
def update_menu(menu_id):
    # 메뉴 업데이트 로직 수행
    # ...
    return jsonify({'message': '메뉴가 성공적으로 업데이트되었습니다.'}), 200

@adm_bp.route('/menu/<menu_id>', methods=['DELETE'])
def delete_menu(menu_id):
    # 메뉴 삭제 로직 수행
    # ...
    return jsonify({'message': '메뉴가 성공적으로 삭제되었습니다.'}), 204
### 메뉴 끝 ###
####################



####################
### 메뉴옵션 시작 ###
@adm_bp.route('/menu_option', methods=['POST'])
def create_menu_option():
    # 메뉴옵션 생성 로직 수행
    # ...
    menu_option_data = request.get_json()
    print('Received JSON data:', menu_option_data)
    return jsonify({'message': '메뉴 옵션을 성공적으로 생성되었습니다.'}), 201

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
    # ...
    menu_main_category_data = request.get_json()
    print('Received JSON data:', menu_main_category_data)
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
    # ...
    menu_sub_category_data = request.get_json()
    print('Received JSON data:', menu_sub_category_data)
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
    # ...
    table_category_data = request.get_json()
    print('Received JSON data:', table_category_data)
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
    # ...
    table_data = request.get_json()
    print('Received JSON data:', table_data)
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
