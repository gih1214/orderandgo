from flask import session
from app.models import db, MainCategory, SubCategory

# 메인카테고리 생성
def create_main_category(store_id, name):
    main_category = MainCategory(store_id=store_id, name=name)
    db.session.add(main_category)
    db.session.commit()
    return True