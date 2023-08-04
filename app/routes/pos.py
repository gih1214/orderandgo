from flask import render_template, jsonify, request
from app.models.menu import select_main_category, select_menu_all, select_menu, select_menu_option, select_menu_option_all
from app.models.order import find_order_list, find_order_option_list, get_orders_by_store_id
from app.routes import pos_bp
import json

from app.routes import pos_bp
from app.models.table import \
    create_table_catgory,\
    move_table, \
    select_table_category, \
    update_table_category, \
    delete_table_category, \
    select_table, \
    set_table_group
from app.models import db


@pos_bp.route('/tableList')
def tableList():    
    return render_template('pos/table_list.html')


@pos_bp.route('/set_group', methods=['GET', 'POST'])
def set_group():
    group_data = request.get_json()
    return set_table_group(group_data)


@pos_bp.route('/get_table_page', methods=['GET'])
def get_table_page():
    store_id = 1    # temp
    
    # 실행할 코드
    orders = get_orders_by_store_id(store_id)

    # # 가져온 데이터 사용 예시
    # for order in orders:
    #     print(order.id, order.ordered_at, order.menu_id, order.table_id, order.menu_options)
    
    # table_id를 기준으로 중복 제거하여 딕셔너리로 구성
    orders_by_table = {}
    for order in orders:
        table_id = order.table_id
        if table_id not in orders_by_table:
            orders_by_table[table_id] = []
        orders_by_table[table_id].append(order)
    
    all_table_list = []
    table_categories = select_table_category(store_id)
    
    for t in table_categories:
        category_name = t.category_name
        category_id = t.id
        tables = select_table(category_id)
        sorted_tables = sorted(tables, key=lambda table: (table.page, table.position))
        
        def sort_table(table):
            print('table,',table)
            
            if table.id in dict(orders_by_table):
                # print("있음")
                orders = orders_by_table[table.id]
                statusId = 1
                orderList = []
                for order in orders:
                    
                    optionList = [];
                    options = json.loads(order.menu_options) if order.menu_options else []
                    for option_data in options:
                        option = select_menu_option(option_data['id'])[0]
                        optionList.append({
                            "optionId" : option.id,
                            "option" : option.name,
                            "price" : option.price,
                            "count" : option_data['count']
                        })
                    menu = select_menu(order.menu_id)[0]
                    orderList.append({
                        "menuId" : order.menu_id,
                        "menu" : menu.name,
                        "price" : menu.price,
                        "count" : 1,
                        "optionList" : optionList
                    })
                    if order.order_status_id == 2:
                        statusId = 2
                return {
                    "tableId": table.id, 
                    "table": table.name,
                    "statusId": statusId,
                    "status": "",
                    "orderList" : orderList,
                }
            else :
                # print("없음")
                return {
                    "tableId": table.id, 
                    "table": table.name,
                    "statusId": 0,
                    "status": "",
                    "orderList" : [],
                }

        # 페이지별로 그룹화
        page_list = [];
        current_page = None
        for table in sorted_tables:
            if table.page != current_page:
                current_page = table.page
                page_list.append({
                    "page": current_page, 
                    "tableList": [sort_table(table)]
                })
            else:
                page_list[-1]["tableList"].append(sort_table(table))

        all_table_list.append({
            "categoryId" : category_id,
            "category" : category_name,
            "pageList" : page_list
        })
        
    return jsonify(all_table_list)

    # # JSON 파일 경로 설정
    # json_file_path = 'app/static/json/tableList.json'

    # # JSON 파일 로드
    # with open(json_file_path, 'r', encoding='UTF-8') as file:
    #     json_data = json.load(file)

    # # JSON 데이터를 프론트에 반환
    # return jsonify(json_data)


# 테이블 -> 메뉴리스트 페이지
@pos_bp.route('/menuList/<table_id>', methods=['GET'])
def menuList(table_id): 
    # JSON 데이터를 프론트에 반환
    return render_template('/pos/menu_list.html')

# 테이블 -> 메뉴리스트에 필요한 메뉴 데이터 (json)
@pos_bp.route('/get_menu_list/<table_id>', methods=['GET'])
def get_menu_list(table_id):
    
    store_id = 1    # temp
    all_menu_list = []
    menu_categories = select_main_category(store_id) # 메인 카테고리 조회
    
    for t in menu_categories:
        category_name = t.name
        category_id = t.id
        menus = select_menu_all(category_id)
        sorted_menus = sorted(menus, key=lambda menu: (menu.page, menu.position))
        
        def sort_menu(menu):
            option_list = [];
            menu_options = select_menu_option(menu.id)
            
            if isinstance(menu_options, list):
                for option in menu_options:
                    option_data = {
                        "optionId" : option.id,
                        "option" : option.name,
                        "price" : option.price
                    }
                    option_list.append(option_data)
            return {
                "menuId": menu.id, 
                "menu": menu.name,
                "price": menu.price,
                "optionList" : option_list
            }

        # 페이지별로 그룹화
        page_list = [];
        current_page = None
        for menu in sorted_menus:
            if menu.page != current_page:
                current_page = menu.page
                page_list.append({
                    "page": current_page, 
                    "menuList": [sort_menu(menu)]
                })
            else:
                page_list[-1]["menuList"].append(sort_menu(menu))

        all_menu_list.append({
            "categoryId" : category_id,
            "category" : category_name,
            "pageList" : page_list
        })

    return jsonify(all_menu_list)

    # # JSON 파일 경로 설정
    # json_file_path = 'app/static/json/menuList.json'
        
    # # JSON 파일 로드
    # with open(json_file_path, 'r', encoding='UTF-8') as file:
    #     json_data = json.load(file)
    # print(json_data)
    # return jsonify(json_data)

# 테이블 이동/합석
@pos_bp.route('/set_table', methods=['PUT'])
def set_table_list():
    table_data = request.get_json()
    end_id = table_data['end_id']
    start_id = table_data['start_id'] # end_id로 이동할 테이블
    set_table = move_table(end_id, start_id)
    response = jsonify({'message': 'Success'})
    response.status_code = 200
    print('Received JSON data:', set_table)
    return response