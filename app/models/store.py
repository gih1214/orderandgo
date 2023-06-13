from flask import session
from app.models import db, Store

# 매장 생성
def insert_store(user_id, store_name, store_type, store_address, store_phone, store_manage_name, store_manage_number,
                 service_ids, store_logo_image, store_image, store_main_description, store_sub_description, store_table):
    store = Store(user_id=user_id, store_name=store_name, store_type=store_type, store_address=store_address, store_phone=store_phone, 
                  store_manage_name=store_manage_name, store_manage_number=store_manage_number,
                 service_ids=service_ids, store_logo_image=store_logo_image, store_image=store_image, 
                 store_main_description=store_main_description, store_sub_description=store_sub_description, store_table=store_table)
    db.session.add(store)
    db.session.commit()
    return True

# 조회


# 수정


# 삭제
