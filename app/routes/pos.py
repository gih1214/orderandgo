from flask import render_template, jsonify
from app.routes import pos_bp
import json

from app.routes import pos_bp
from app.models.table import create_table_catgory, select_table_category, update_table_category, delete_table_category, select_table, select_table_category_page
from app.models import db


@pos_bp.route('/tableList')
def tableList():    
    return render_template('pos/table_list.html')

@pos_bp.route('/get_table_page', methods=['GET'])
def get_table_page():
    print('##########호출됨')

    '''
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
                    'isGroup' : 0,
                    'groupId' : '',
                    'groupNum' : '',
                    'groupColor' : ''
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

# 테이블 -> 메뉴리스트 페이지
@pos_bp.route('/menuList/<table_id>', methods=['GET'])
def menuList(table_id):
    
    # JSON 데이터를 프론트에 반환
    return render_template('/pos/menu_list.html')

@pos_bp.route('/get_menu_list/<table_id>', methods=['GET'])
def get_menu_list(table_id):
    #menu_list = select_menu(1)

    # JSON 파일 경로 설정
    json_file_path = 'app/static/json/menuList.json'
        
    # JSON 파일 로드
    with open(json_file_path, 'r', encoding='UTF-8') as file:
        json_data = json.load(file)
    #print(json_data)
    # JSON 데이터를 프론트에 반환
    return jsonify(json_data)