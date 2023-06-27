from flask import session
from app.models import db, Menu, MenuOption

# 메뉴 생성
def create_menu(name, price, image, main_description, sub_description,
                is_soldout, store_id, menu_category_id):
    menu = Menu(name=name, price=price, image=image, main_description=main_description, sub_description=sub_description,
                 is_soldout=is_soldout, store_id=store_id, menu_category_id=menu_category_id)
    db.session.add(menu)
    db.session.commit()
    return True

# 메뉴 옵션 생성
def create_menu_option(name, price, description, store_id):
    menu_option = MenuOption(name=name, price=price, description=description, store_id=store_id)
    db.session.add(menu_option)
    db.session.commit()
    return True

# 메뉴 조회


# 메뉴 수정


# 메뉴 삭제