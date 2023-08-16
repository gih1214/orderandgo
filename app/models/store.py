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
def update_store(user_id, store_id, name, address, tel, manager_name, manager_tel, 
                 logo_img, store_image, main_description, sub_description):
    store_item = Store.query.filter(Store.id == store_id).first()

    if not store_item:
        return '잘못된 store_item'
    
    store_item.name = name
    store_item.address = address
    store_item.tel = tel
    store_item.manager_name = manager_name
    store_item.manager_tel = manager_tel
    store_item.logo_img = logo_img
    store_item.store_image = store_image
    store_item.main_description = main_description
    store_item.sub_description = sub_description
    
    #setattr(store_item, column, value)

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
def delete_store(store_id):
    item = Store.query.filter(Store.id == store_id).first()
    if not item:
        return '스토어 정보가 없습니다.'
    db.session.delete(item)
    db.session.commit()
    return True