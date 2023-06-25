from flask import render_template, jsonify
from app.routes import pos_bp
import json


@pos_bp.route('/tableList')
def tableList():    
    return render_template('pos/table_list.html')

@pos_bp.route('/get_table_page', methods=['GET'])
def get_table_page():
    print('호출됨')
    # JSON 파일 경로 설정
    json_file_path = 'app/static/json/tableList.json'

    # JSON 파일 로드
    with open(json_file_path, 'r', encoding='UTF-8') as file:
        json_data = json.load(file)
    # JSON 데이터를 프론트에 반환
    return jsonify(json_data)

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