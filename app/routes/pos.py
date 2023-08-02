from flask import render_template, jsonify, request
from app.models.menu import select_main_category, select_menu
from app.models.order import find_order_list, find_order_option_list
from app.routes import pos_bp
import json

from app.routes import pos_bp
from app.models.table import create_table_catgory, move_table, select_table_category, update_table_category, delete_table_category, select_table, select_table_category_page, set_table_group
from app.models import db


@pos_bp.route('/tableList')
def tableList():    
    return render_template('pos/table_list.html')


@pos_bp.route('/set_group', methods=['GET', 'POST'])
def set_group():
    sample_data = [
        {
            'table_id':1,
            'group_id':None,
            'group_color':None
        },
        {
            'table_id':2,
            'group_id':1,
            'group_color':'fff'
        },
    ]
    # group_data = request.get_json()
    
    return set_table_group(sample_data)


@pos_bp.route('/get_table_page', methods=['GET'])
def get_table_page():

    # # JSON 파일 경로 설정
    # json_file_path = 'app/static/json/tableList.json'

    # # JSON 파일 로드
    # with open(json_file_path, 'r', encoding='UTF-8') as file:
    #     json_data = json.load(file)

    # # JSON 데이터를 프론트에 반환
    # return jsonify(json_data)


    store_id = 1    # temp
    all_table_list = []
    table_categories = select_table_category(store_id)
    
    for t in table_categories:
        category_name = t.category_name
        category_id = t.id
        tables = select_table(category_id)
        sorted_tables = sorted(tables, key=lambda table: (table.page, table.position))
        
        def sort_table(table):
            return {
                "tableId": table.id, 
                "table": table.name,
                "statusId": 0,
                "status": "",
                "orderList" : [],
            }

        print(sorted_tables)
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

        print(page_list)
            
        all_table_list.append({
            "categoryId" : category_id,
            "category" : category_name,
            "pageList" : page_list
        })
        
        
    print(all_table_list)
        

    return jsonify(all_table_list)

    # # 테이블 카테고리
    # for t in table_categories:
    #     page_list = []
    #     table_category_pages = select_table_category_page(t.id)
        
    #     for p in table_category_pages:
    #         table_list = []
    #         tables = select_table(p.id)

    #         for table in tables:
    #             # 주문 리스트 출력
    #             order_list_items = find_order_list(table.id)
    #             print("@#$@#$@#$#@$",find_order_list)
                
    #             order_list = []
    #             for o in order_list_items:
                    
    #                 # 주문 옵션 리스트 출력
    #                 order_option_items = find_order_option_list(o.order_id)

    #                 option_list = []
    #                 for oo in order_option_items:
    #                     option_list.append({
    #                         'optionId':oo.id,
    #                         'option':oo.name,
    #                         'price':oo.price,
    #                         'count':1
    #                     })


    #                 order_list.append({
    #                     "menuId" : o.id,
    #                     "menu" : o.name,
    #                     "price" : o.price,
    #                     "count" : 1,
    #                     "optionList" : option_list             
    #                 })

    #             table_list.append({
    #                 'tableId' : table.id,
    #                 'table' : table.name,
    #                 'statusId' : 0,
    #                 'status' : '???',
    #                 'orderList' :  order_list,
    #                 'isGroup' : table.is_group if table.is_group is not None else None,
    #                 'groupId' : table.is_group if table.is_group is not None else None,
    #                 'groupNum' : table.is_group if table.is_group is not None else None,
    #                 'groupColor' : table.group_color if table.is_group is not None else None
    #             })

    #         page_list.append({
    #             'page' : p.page,
    #             'tableList' : table_list
    #         })

    #     all_table_list.append({
    #         'categoryId' : t.id,
    #         'category' : t.category_name,
    #         'pageList' : page_list
    #     })


    # print("@#$", all_table_list)

    # # JSON 데이터를 프론트에 반환
    # return jsonify(all_table_list)


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
    print('menu_categories,',menu_categories)
    # 메인 카테고리별 메뉴 조회
    for m in menu_categories:
        # page_list = []
        # menu_category_pages = select_menu_category_page(m.id)
        
        print(m.name)
        
        menu_list = []
        menus = select_menu(m.id) # 카테고리별 메뉴 조회
        print(menus)
        if menus == '없는 메뉴입니다.': # 카테고리 안에 메뉴가 없을 때
            all_menu_list.append({
                'categoryId' : m.id,
                'category' : m.name,
                'menuList' : []
            })
        else:
            for menu in menus: # 메뉴 있을 때
                menu_list.append({
                    'menuId' : menu.id,
                    'menu' : menu.name,
                    'price' : menu.price,
                    'optionList' :  []
                })

                '''
                page_list.append({
                    'page' : p.page,
                    'tableList' : menu_list
                })
                '''

            all_menu_list.append({
                'categoryId' : m.id,
                'category' : m.name,
                'menuList' : menu_list
            })
            print(all_menu_list)

    # # JSON 파일 경로 설정
    # json_file_path = 'app/static/json/menuList.json'
        
    # # JSON 파일 로드
    # with open(json_file_path, 'r', encoding='UTF-8') as file:
    #     json_data = json.load(file)
    # print(json_data)
    # return jsonify(json_data)

    # JSON 데이터를 프론트에 반환
    return jsonify(all_menu_list)

# 테이블 이동/합석
@pos_bp.route('/set_table/<store_id>', methods=['PUT'])
def set_table_list(store_id):
    table_data = request.get_json()
    end_id = table_data['end_id']
    start_id = table_data['start_id'] # end_id로 이동할 테이블
    set_table = move_table(end_id, start_id)
    response = jsonify({'message': 'Success'})
    response.status_code = 200
    print('Received JSON data:', set_table)
    return response