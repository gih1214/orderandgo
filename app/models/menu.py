from flask import session
from app.models import db, Menu

# 메뉴 생성
def create_menu(name, price, image, main_description, sub_description,
                is_soldout, store_id, menu_category_id):
    menu = Menu(name=name, price=price, image=image, main_description=main_description, sub_description=sub_description,
                 is_soldout=is_soldout, store_id=store_id, menu_category_id=menu_category_id)
    db.session.add(menu)
    db.session.commit()
    return True

# 조회


# 수정


# 삭제