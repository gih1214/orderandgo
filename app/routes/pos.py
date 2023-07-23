from flask import render_template, jsonify, request
from app.models.menu import select_main_category, select_menu
from app.routes import pos_bp
import json

from app.routes import pos_bp
from app.models.table import create_table_catgory, select_table_category, update_table_category, delete_table_category, select_table, select_table_category_page, set_table_group
from app.models import db


@pos_bp.route('/tableList')
def tableList():    
    return render_template('pos/table_list.html')


@pos_bp.route('/set_group', methods=['GET', 'POST'])
def set_group():
    group_data = request.get_json()
    
    set_or_del = group_data['set_or_del']
    group_id_list = group_data['group_id_list']
    group_id = group_data['group_id']
    group_color = group_data['group_color']

    return set_table_group(set_or_del, group_id_list, group_id, group_color)


@pos_bp.route('/get_table_page', methods=['GET'])
def get_table_page():
    print('##########호출됨')

    # JSON 파일 경로 설정
    json_file_path = 'app/static/json/tableList.json'

    # JSON 파일 로드
    with open(json_file_path, 'r', encoding='UTF-8') as file:
        json_data = json.load(file)

    # JSON 데이터를 프론트에 반환
    return jsonify(json_data)
    '''
    store_id = 1    # temp
    all_table_list = []
    table_categories = select_table_category(store_id)

    # 테이블 카테고리
    for t in table_categories:
        page_list = []
        table_category_pages = select_table_category_page(t.id)
        
        for p in table_category_pages:
            table_list = []
            tables = select_table(p.id)

            for table in tables:
                table_list.append({
                    'tableId' : table.id,
                    'table' : table.name,
                    'statusId' : 0,
                    'status' : '???',
                    'orderList' :  [],
                    'isGroup' : table.is_group if table.is_group is not None else None,
                    'groupId' : table.is_group if table.is_group is not None else None,
                    'groupNum' : table.is_group if table.is_group is not None else None,
                    'groupColor' : table.group_color if table.is_group is not None else None
                })

            page_list.append({
                'page' : p.page,
                'tableList' : table_list
            })

        all_table_list.append({
            'categoryId' : t.id,
            'category' : t.category_name,
            'pageList' : page_list
        })


        

    # JSON 데이터를 프론트에 반환
    return jsonify(all_table_list)
    '''
# 테이블 -> 메뉴리스트 페이지
@pos_bp.route('/menuList/<table_id>', methods=['GET'])
def menuList(table_id): 
    # JSON 데이터를 프론트에 반환
    return render_template('/pos/menu_list.html')

# 테이블 -> 메뉴리스트에 필요한 메뉴 데이터 (json)
@pos_bp.route('/get_menu_list/<table_id>', methods=['GET'])
def get_menu_list(table_id):
    
    # store_id = 1    # temp
    # all_menu_list = []
    # menu_categories = select_main_category(store_id) # 메인 카테고리 조회

    # # 메인 카테고리별 메뉴 조회
    # for m in menu_categories:
    #     #page_list = []
    #     #menu_category_pages = select_menu_category_page(m.id)
        
    #     menu_list = []
    #     menus = select_menu(m.id) # 카테고리별 메뉴 조회

    #     if menus == '없는 메뉴입니다.': # 카테고리 안에 메뉴가 없을 때
    #         all_menu_list.append({
    #             'categoryId' : m.id,
    #             'category' : m.name,
    #             'menuList' : []
    #         })
    #     else:
    #         for menu in menus: # 메뉴 있을 때
    #             menu_list.append({
    #                 'menuId' : menu.id,
    #                 'menu' : menu.name,
    #                 'price' : menu.price,
    #                 'optionList' :  []
    #             })

    #             '''
    #             page_list.append({
    #                 'page' : p.page,
    #                 'tableList' : menu_list
    #             })
    #             '''

    #         all_menu_list.append({
    #             'categoryId' : m.id,
    #             'category' : m.name,
    #             'menuList' : menu_list
    #         })
    #         print(all_menu_list)

    # JSON 파일 경로 설정
    json_file_path = 'app/static/json/menuList.json'
        
    # JSON 파일 로드
    with open(json_file_path, 'r', encoding='UTF-8') as file:
        json_data = json.load(file)
    print(json_data)
    return jsonify(json_data)

    # JSON 데이터를 프론트에 반환
    # return jsonify(all_menu_list)