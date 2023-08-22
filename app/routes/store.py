import json
from flask import render_template, jsonify, request, session


from app.routes import store_bp

@store_bp.route('/login')
def login():
    return render_template('store_login.html');

# @store_bp.route('/')
# def index():
#     return render_template('adm.html');

@store_bp.route('/')
def index():
    return render_template('store.html');
  
@store_bp.route('/product')
def product():
    return render_template('store_product.html');

@store_bp.route('/set_menu')
def set_menu():
    return render_template('set_menu_product.html');

@store_bp.route('/get_main_category', methods=['GET'])
def get_main_category():
    # JSON 파일 경로 설정
    json_file_path = 'app/static/json/setMenuProductMainCategory.json'
    # JSON 파일 로드
    with open(json_file_path, 'r', encoding='UTF-8') as file:
        json_data = json.load(file)
    # JSON 데이터를 프론트에 반환
    return jsonify(json_data)

@store_bp.route('/get_sub_category', methods=['GET'])
def get_sub_category():
    # JSON 파일 경로 설정
    json_file_path = 'app/static/json/setMenuProductSubCategory.json'
    # JSON 파일 로드
    with open(json_file_path, 'r', encoding='UTF-8') as file:
        json_data = json.load(file)
    # JSON 데이터를 프론트에 반환
    return jsonify(json_data)

@store_bp.route('/get_menu_list', methods=['GET'])
def get_menu_list():
    # JSON 파일 경로 설정
    json_file_path = 'app/static/json/setMenuProductMenu.json'
    # JSON 파일 로드
    with open(json_file_path, 'r', encoding='UTF-8') as file:
        json_data = json.load(file)
    # JSON 데이터를 프론트에 반환
    return jsonify(json_data)

@store_bp.route('/all_menu_list', methods=['GET'])
def all_menu_list():
    # JSON 파일 경로 설정
    json_file_path = 'app/static/json/setMenuProductAllMenu.json'
    # JSON 파일 로드
    with open(json_file_path, 'r', encoding='UTF-8') as file:
        json_data = json.load(file)
    # JSON 데이터를 프론트에 반환
    return jsonify(json_data)

