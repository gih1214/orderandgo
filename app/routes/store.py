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
    # store_id = current_user.id
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

    main_category_id = request.args.get('main_category_id')

    # 메인카테고리 아무것도 선택 안했을 때 기본값 설정
    if main_category_id is None:
        # TODO : store_id 세션에서 받아오기, 현재 임시로 값 넣음
        store_id = 1
        # store_id = current_user.id
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

    # TODO : store_id 세션에서 받아오기, 현재 임시로 값 넣음
    store_id = 1
    # store_id = current_user.id

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

@store_bp.route('/get_menu', methods=['GET'])
def get_menu():
    menu_id = request.args.get('menu_id')
    menu = select_menu(menu_id)[0]
    options = select_menu_option_all(menu_id)
    option_data = []
    if options:
        for option in options:
            option_data.append({
                'name' : option.name,
                'price' : option.price
            })
    menu_data = {}
    
    cur_main_category, cur_sub_category = get_main_and_sub_category_by_menu_id(menu);
    main_category_list = get_main_category()
    sub_category_list = get_sub_category()
    for main_category in main_category_list:
        print(main_category['id'], cur_main_category.id)
        if main_category['id'] == cur_main_category.id:
            
            main_category['checked'] = True
        else:
            main_category['checked'] = False
    
    for sub_category in sub_category_list:
        if sub_category['id'] == cur_sub_category.id:
            sub_category['checked'] = True
        else:
            sub_category['checked'] = False
    
    
    menu_data = {
        'id' : menu.id,
        'name' : menu.name,
        'price': menu.price,
        'imgList' : [],
        'description': menu.main_description,
        'options' : option_data,
        'category': {
            'main' : main_category_list,
            'sub' : sub_category_list,
        },
    }
    return menu_data



@store_bp.route('/set_menu', methods=['GET', 'POST', 'PATCH'])
def set_menu():
    if request.method == 'GET':
        return render_template('set_menu_product.html')

    # 새 메뉴 추가
    if request.method == 'POST':
        return True
    
    # 기존 메뉴 수정
    if request.method == 'PATCH':
        return True
    
    
# POS관리 -> 상품 정보 등록 페이지
# '추가' 버튼 클릭 시 메뉴 id 생성
@store_bp.route('/create_menu', methods=['POST'])
def api_create_menu():
    if request.method == 'POST':
        # TODO : store_id 세션에서 받아오기, 현재 임시로 값 넣음
        #store_id = 16
        store_data = request.get_json()
        store_id = store_data['store_id']

        menu_category_id = select_main_and_sub_category_by_store_id(store_id)

        menu = create_menu(store_id, menu_category_id)
        print('DB 저장 후 컨트롤러까지 잘 왔음!!! :D')
        print(menu)
        return menu