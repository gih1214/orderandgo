from flask import render_template, request, jsonify
from flask_login import login_required
from app.routes import store_bp

from app.models import db, Store
from app.models.store import create_store, update_store
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

  
@store_bp.route('/product')
def product():
    return render_template('store_product.html')

@store_bp.route('/set_menu')
def set_menu():
    return render_template('set_menu_product.html')
