import json
from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from app.models.menu_category import get_main_and_sub_category_by_menu_id, select_main_and_sub_category_by_store_id
from app.routes import store_bp

from app.models import db, Store
from app.models.store import create_store, update_store
from app.models.menu import create_menu, select_main_category, select_menu, select_sub_category, select_menu_option_all, find_all_menu
from app.login_manager import update_store_session


# 매장 생성
@login_required
@store_bp.route('/create_or_update', methods=['GET', 'POST'])
def api_create_or_update_store():
    if request.method == 'GET':
        return render_template('/store_register.html')  # TODO
    
    if request.method == 'POST':
        store_id = request.form.get('store_id')
        user_id = request.form.get('user_id')
        name = request.form.get('name')
        address = request.form.get('address')
        tel = request.form.get('tel')
        manager_name = request.form.get('manager_name')
        manager_tel = request.form.get('manager_tel')
        logo_img = request.form.get('logo_img')
        store_image = request.form.get('username')
        main_description = request.form.get('main_description')
        sub_description = request.form.get('sub_description')

        if store_id is not None:    # update
            store = update_store(store_id, user_id, name, address, tel, manager_name, manager_tel,
                                logo_img, store_image, main_description, sub_description)
        else:                       # create
            store = create_store(user_id, name, address, tel, manager_name, manager_tel,
                                logo_img, store_image, main_description, sub_description)

        print("스토어 성공", store)
        response = jsonify({'message': 'Success'})
        response.status_code = 200
        return response
    

# 매장 리스트
@store_bp.route('/store_list', methods=['GET', 'POST'])
def api_store_list(user_id):
    dummy = [
        {'id':1, 'name':'할맥'},
        {'id':12, 'name':'할맥2'},
    ]

    store_list = []
    store_items = db.session.query(Store).filter(Store.user_id == user_id).all()
    for s in store_items:
        store_list.append({
            'id': s.id,
            'name': s.name
        })

    return store_list


# 매장 클릭 시 세션 접속
@store_bp.route('/session_store', methods=['GET', 'POST'])
def api_update_store_session(store_id):
    res = update_store_session(store_id)

    return res



# @store_bp.route('/')
# def index():
#     return render_template('adm.html');

@store_bp.route('/')
def index():
    return render_template('store.html')


@store_bp.route('/login')
def login():
    return render_template('store_login.html')

@store_bp.route('/create')
def create():
    return render_template('store_create.html')

  
@store_bp.route('/product')
def product():
    return render_template('store_product.html')

# 카테고리, 메뉴, 옵션 관리 페이지
@store_bp.route('/set_menu')
def set_menu():
    return render_template('set_menu_product.html')



@store_bp.route('/get_main_category', methods=['GET'])
def get_main_category():
    '''
    # JSON 파일 경로 설정
    json_file_path = 'app/static/json/setMenuProductMainCategory.json'
    # JSON 파일 로드
    with open(json_file_path, 'r', encoding='UTF-8') as file:
        json_data = json.load(file)
    # JSON 데이터를 프론트에 반환
    return jsonify(json_data)
    '''

    # TODO : store_id 세션에서 받아오기, 현재 임시로 값 넣음
    store_id = 1
<<<<<<< HEAD
=======
    # store_id = current_user.id
>>>>>>> 19752613fc3f9a3c66d51c7c15fb9382cf2e173e
    items = select_main_category(store_id)

    main_category_list = []
    for i in items:
        main_category_list.append({
            'id': i.id,
            "name": i.name,
            "checked": False,
        })

    print("\n\n###main_category_list",main_category_list)
    return main_category_list

@store_bp.route('/get_sub_category', methods=['GET'])
def get_sub_category():
    '''
    # JSON 파일 경로 설정
    json_file_path = 'app/static/json/setMenuProductSubCategory.json'
    # JSON 파일 로드
    with open(json_file_path, 'r', encoding='UTF-8') as file:
        json_data = json.load(file)
    # JSON 데이터를 프론트에 반환
    return jsonify(json_data)
    '''

    main_category_id = request.args.get('main_category_id')

    # 메인카테고리 아무것도 선택 안했을 때 기본값 설정
    if main_category_id is None:
        # TODO : store_id 세션에서 받아오기, 현재 임시로 값 넣음
        store_id = 1
<<<<<<< HEAD
=======
        # store_id = current_user.id
>>>>>>> 19752613fc3f9a3c66d51c7c15fb9382cf2e173e
        main_categorys = select_main_category(store_id)
        main_category_id = main_categorys[0].id

    items = select_sub_category(main_category_id)
    
    sub_category_list = []
    for i in items:
        sub_category_list.append({
            'id': i.id,
            "name": i.name,
            "checked" : False,
        })

    print("\n\n###sub_category_list",sub_category_list)
    return sub_category_list

@store_bp.route('/all_menu_list', methods=['GET'])
def all_menu_list():
    '''
    # JSON 파일 경로 설정
    json_file_path = 'app/static/json/setMenuProductAllMenu.json'
    # JSON 파일 로드
    with open(json_file_path, 'r', encoding='UTF-8') as file:
        json_data = json.load(file)
    # JSON 데이터를 프론트에 반환
    return jsonify(json_data)
    '''

    # TODO : store_id 세션에서 받아오기, 현재 임시로 값 넣음
    store_id = 1
<<<<<<< HEAD
=======
    # store_id = current_user.id
>>>>>>> 19752613fc3f9a3c66d51c7c15fb9382cf2e173e

    menu_items = find_all_menu(store_id)
    # print("@$#", menu_items)

    all_menu_list = []
    for i in menu_items:
        # 옵션 있으면 어떻게?
        option_list = []
        all_option_list = select_menu_option_all(i.id)
        for o in all_option_list:
            option_list.append({
                'option_id': o.id,
                'option_name': o.name,
                'option_price': o.price
            })

        all_menu_list.append({
            'id': i.id,
            'main_category': i.main_category_name,
            'sub_category': i.sub_category_name,
            'name': i.name,
            'price': i.price,
            'option': option_list
        })

    print("@@@", all_menu_list)
    return all_menu_list

# POS관리 -> 상품 정보 등록 페이지
# '추가' 버튼 클릭 시 메뉴 id 생성
@store_bp.route('/create_menu', methods=['POST'])
def api_create_menu():
    if request.method == 'POST':
        # TODO : store_id 세션에서 받아오기, 현재 임시로 값 넣음
        #store_id = 16
        store_data = request.get_json()
        store_id = store_data['store_id']

        print('여기부터 문제라니..?')
        print(store_id)
        menu_category_id = select_main_and_sub_category_by_store_id(store_id)

        menu = create_menu(store_id, menu_category_id)
        print('DB 저장 후 컨트롤러까지 잘 왔음!!! :D')
        print(menu)
        return menu

# 상품 정보 등록 or 수정하기 (미완성)
@login_required
@store_bp.route('/create_product', methods=['POST', 'UPDATE'])
def api_create_product():
    if request.method == 'POST':
        # 상품 이미지(여러개 가능), 메뉴명, 판매가, 메뉴 설명, 카테고리(메인, 서브), 옵션(여러개 가능)
        #store_images = request.form.get('store_images')
        name = request.form.get('name')
        price = request.form.get('price')
        main_category = request.form.get('main_category')
        sub_category = request.form.get('sub_category')
        option = request.form.get('option')

        store = create_product(name, price, main_category, sub_category, option)

        print("상품 등록 성공", store)
        response = jsonify({'message': 'Success'})
        response.status_code = 200
        return response