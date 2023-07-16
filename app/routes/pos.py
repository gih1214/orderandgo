from flask import render_template, jsonify
import json

from app.routes import pos_bp
from app.models.table import create_table_catgory, select_table_category, update_table_category, delete_table_category, select_table
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
    table_categories = select_table_category(store_id)

    tables = select_table(store_id)

    table_list = []

    # 테이블 카테고리
    for t in table_categories:
        table_list.append({
            'categoryId' : t.id,
            'category' : t.category_name
        })
        

    # JSON 데이터를 프론트에 반환
    return jsonify(table_list)

@pos_bp.route('/menuList/<table_id>', methods=['GET'])
def menuList(table_id):
    
    # JSON 데이터를 프론트에 반환
    return render_template('/pos/menu_list.html')

@pos_bp.route('/get_menu_list/<table_id>', methods=['GET'])
def get_menu_list(table_id):
    # JSON 파일 경로 설정
    json_file_path = 'app/static/json/menuList.json'
        
    # JSON 파일 로드
    with open(json_file_path, 'r', encoding='UTF-8') as file:
        json_data = json.load(file)
    print(json_data)
    # JSON 데이터를 프론트에 반환
    return jsonify(json_data)