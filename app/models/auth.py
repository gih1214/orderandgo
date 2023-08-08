from flask import session, jsonify
from app.models import db, Store

def update_store_session(store_id):
    store_item = db.query(Store).filter(Store.id == store_id).first()
    if store_item is None:
        return jsonify({'message': '스토어 세션 등록 실패'}), 400

    session['store_item'] = store_item

    return jsonify({'message': '스토어 세션 등록 성공'}), 200