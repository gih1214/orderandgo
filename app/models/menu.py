import json
from flask import session
from app.models import db, Menu, MenuOption
import pandas as pd

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

# 메뉴 조회 (SELECT ALL)
def select_menu(store_id):
    item = Menu.query.filter(Menu.store_id == store_id).all()
    if not item:
        return '없는 메뉴입니다.'
    return item

# 메뉴 수정
def update_menu(menu_id, name, price, image, main_description, sub_description, is_soldout):
    item = Menu.query.filter(Menu.id == menu_id).first()
    if not item:
        return '없는 메뉴입니다.'
    
    item.name = name
    item.price = price
    item.image = image
    item.main_description = main_description
    item.sub_description = sub_description
    item.is_soldout = is_soldout

    db.session.commit()
    return True

# 메뉴 삭제
def delete_menu(menu_id):
    item = Menu.query.filter(Menu.id == menu_id).first()
    if not item:
        return '없는 메뉴입니다.'
    
    db.session.delete(item)
    db.session.commit()
    return True