from flask import session
from app.models import db, Store

# 매장 생성
def create_store(user_id, name, address, tel, manager_name, manager_tel,
                logo_img, store_image, main_description, sub_description):
    store = Store(user_id=user_id, name=name, address=address, tel=tel, manager_name=manager_name, manager_tel=manager_tel,
                 logo_img=logo_img, store_image=store_image, main_description=main_description, sub_description=sub_description)
    db.session.add(store)
    db.session.commit()
    return store

# 조회


# 수정
def update_store(store_id, column, value):
    store_item = Store.query.filter_by(id=store_id).first()
    if not store_item:
        return '잘못된 store_item'
    
    setattr(store_item, column, value)
    db.session.commit()
    return True
# def update_store(store_id, column, value):
#     store_item = session.query(Store).filter(Store.id == store_id).first()
#     if not store_item:
#         return '잘못된 store_item'
    
#     store_item[column] = value
#     session.commit()
#     return True


# 삭제
