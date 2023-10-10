from flask import session, jsonify, request, render_template, request
from flask_login import LoginManager, UserMixin, login_required

from app.models import db, Store, User
from app.models.user import get_user_by_userid, get_store_by_storeid

from app import login_manager # Flask-login의 변수


# 사용자 로드 함수
@login_manager.user_loader
def load_user(store_id):
    print('사용자 로드 함수')
    # type 이 user, store를 구분해서 실행해야함
    current_path = request.path
    if current_path ==  '/register_store':
        return get_user_by_userid(store_id)
    else:
        return get_store_by_storeid(store_id)


# 로그인이 되어있지 않은 경우
@login_manager.unauthorized_handler
def unauthorized_callback():
    print('로그인이 되어있지 않은 경우')
    return render_template('login.html')


# # 유저 세선 등록
# def update_user_session(user_item):
#     session['user_item'] = user_item
#     return jsonify({'message': '유저 세션 등록 성공'}), 200


# 스토어 세선 등록
def update_store_session(store_id):
    store_item = db.query(Store).filter(Store.id == store_id).first()
    if store_item is None:
        return jsonify({'message': '스토어 세션 등록 실패'}), 400

    session['store_item'] = store_item

    return jsonify({'message': '스토어 세션 등록 성공'}), 200