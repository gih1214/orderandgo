import json
from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from app.models.menu_category import get_main_and_sub_category_by_menu_id, select_main_and_sub_category_by_store_id
from app.models.table import select_table, select_table_category
from app.routes import store_bp


from app.models.store import create_store, update_store
from app.models.menu import create_menu, create_menu_option, select_main_category, select_menu, select_menu_all, select_sub_category, select_menu_option_all, find_all_menu, update_menu, update_menu_option
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
    # store_id = 1
    store_id = current_user.id
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
        # store_id = 1
        store_id = current_user.id
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

    
    return sub_category_list


# POS -> 매장관리 -> 상품 정보 수정 -> 전체 메뉴 조회 기능
@store_bp.route('/all_menu_list', methods=['GET'])
def all_menu_list():
    # TODO : store_id 세션에서 받아오기, 현재 임시로 값 넣음
    store_id = 16
    #store_id = current_user.id

    all_menu_list = []
    main_categories = select_main_category(store_id) # 메인 카테고리 조회

    for t in main_categories:
        main_category_id = t.id # 메인 카테고리 ID
        main_category_name = t.name # 메인 카테고리명
        sub_categories = select_sub_category(main_category_id) # 서브 카테고리 조회

        for s in sub_categories:
            sub_category_id = s.id # 메인 카테고리 ID
            sub_category_name = s.name # 메인 카테고리명
            menus = select_menu_all(sub_category_id) # 메뉴 조회
            #sorted_menus = sorted(menus, key=lambda menu: (menu.page, menu.position))

            for m in menus:
                option_list = []
                all_option_list = select_menu_option_all(m.id)
                for o in all_option_list:
                    option_list.append({
                        'option_id': o.id,
                        'option_name': o.name,
                        'option_price': o.price
                    })

                all_menu_list.append({
                    'id': m.id,
                    'name': m.name,
                    'price': m.price,
                    #'image': m.image,
                    'main_description': m.main_description,
                    'sub_description': m.sub_description,
                    #'is_soldout': m.is_soldout,
                    'main_category_id': main_category_id,
                    'main_category_name': main_category_name,
                    'sub_category_id': sub_category_id,
                    'sub_category_name': sub_category_name,
                    'option': option_list
                })
    '''
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
    '''
    return jsonify(all_menu_list)


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


# POS -> 매장관리 -> 상품 정보 수정 -> 생성, 수정
@store_bp.route('/set_menu', methods=['GET', 'POST', 'PATCH'])
def set_menu():
    if request.method == 'GET':
        return render_template('set_menu_product.html')

    # 새 메뉴 추가
    if request.method == 'POST':
        # TODO : page, position 데이터 받기, 현재 null 처리
        store_id = current_user.id
        json_data = json.loads(request.form.get('json_data'))
        images_file_path = 'app/static/images/menu/' # 파일 경로 설정

        # 이미지 저장
        for name in json_data['image']:
            #print(request.files.get(name))
            file = request.files.get(name)
            file.save(images_file_path + name) # 텍스트로 저장된다..

        name = json_data['name']
        price = json_data['price']
        image_list = json_data['image']
        main_description = json_data['main_description']
        #sub_description = json_data['sub_description']
        is_soldout = False # null 허용X -> false 기본값으로 넣고 있음
        print(type(json_data['main_category']))
        menu_category_id = json_data['main_category']
        #page = menu_data['page']
        #position = menu_data['position']
        image = json.dumps(image_list) # 리스트를 json 문자열로 변환

        # 메뉴 create
        menu = create_menu(name, price, image, main_description, is_soldout, store_id, menu_category_id)

        # 메뉴 옵션 create
        create_menu_option(json_data['options'], menu.id)

        return jsonify({'message': '메뉴가 성공적으로 생성되었습니다.'}), 201
    
    # 기존 메뉴 수정
    if request.method == 'PATCH':
        # TODO : store_id 세션에서 받아오기, 현재 임시로 값 넣음
        # TODO : image, page, position 데이터 받기, 현재 null 처리
        #store_id = 16
        menu_data = request.get_json()

        menu_id = menu_data['id']
        name = menu_data['name']
        price = menu_data['price']
        #image = menu_data['image']
        main_description = menu_data['main_description']
        sub_description = menu_data['sub_description']
        #is_soldout = menu_data['is_soldout'] # 수정란에 없음
        store_id = menu_data['store_id']
        menu_category_id = menu_data['menu_category_id']
        #page = menu_data['page']
        #position = menu_data['position']

        # 메뉴 update
        menu = update_menu(menu_id, name, price, main_description, sub_description, store_id, menu_category_id)
        
        if not menu_data['option']:
            return jsonify({'message': '메뉴가 성공적으로 업데이트되었습니다.'}), 200
        # 메뉴 옵션 update

        menu_option = create_menu_option(menu_data['option'], menu.id)
        
        print("메뉴수정 성공", menu)

        return jsonify({'message': '메뉴가 성공적으로 업데이트되었습니다.'}), 200
    
    
# POS관리 -> 상품 정보 등록 페이지
# '추가' 버튼 클릭 시 메뉴 id 생성
'''
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
'''

# POS -> 매장관리 -> 상품 정보 수정 -> 생성(완료), 수정(진행중)
@store_bp.route('/set_table', methods=['GET', 'POST', 'PATCH'])
def set_table():
    if request.method == 'GET':
        return render_template('set_table_product.html')
    
@store_bp.route('/get_table', methods=['GET'])
def get_table():
    store_id = current_user.id
    table_categorys = select_table_category(store_id)
    data=[]
    for table_category in table_categorys:
        tables = select_table(table_category.id)
        table_list = [];
        for table in tables:
            table_list.append({
                'id' : table.id,
                'name' : table.name,
                'page' : table.page,
                'position' : table.position
            })
        # page 그룹화, position 정렬
        grouped_data = {}
        for item in table_list:
            page = item['page']
            if page not in grouped_data:
                grouped_data[page] = []
            grouped_data[page].append(item)
        for page, tables in grouped_data.items():
            grouped_data[page] = sorted(tables, key=lambda x: x['position'])
        page_list = [{'page': page, 'tables': tables} for page, tables in grouped_data.items()]
          
        data.append({
            'id' : table_category.id,
            'name': table_category.category_name,
            'position': table_category.position,
            'pages': page_list
        })
    return data;
    