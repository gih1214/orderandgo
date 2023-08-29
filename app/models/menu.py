import json
from flask import session
from app.models import MainCategory, SubCategory, db, Menu, MenuOption

# 메뉴 생성
def create_menu(name, price, image, main_description, sub_description,
                is_soldout, store_id, menu_category_id):
    menu = Menu(name=name, price=price, image=image, main_description=main_description, sub_description=sub_description,
                 is_soldout=is_soldout, store_id=store_id, menu_category_id=menu_category_id)
    db.session.add(menu)
    db.session.commit()
    return True

# 메뉴 옵션 생성
def create_menu_option(name, price, description, store_id, menu_id):
    menu_option = MenuOption(
        name=name, 
        price=price, 
        description=description, 
        store_id=store_id, 
        menu_id=menu_id
    )
    db.session.add(menu_option)
    db.session.commit()
    return True

# 메뉴 옵션 조회 (SELECT ID)
def select_menu_option(option_id):
    item = MenuOption.query.filter(MenuOption.id == option_id).all()
    if not item:
        return '메뉴 옵션이 없습니다.'
    return item

# 메뉴 옵션 조회
def select_menu_option_all(menu_id):
    item = MenuOption.query.filter(MenuOption.menu_id == menu_id).all()
    if not item:
        return '메뉴 옵션이 없습니다.'
    return item

# 메뉴 카테고리 조회 (SELECT ALL)
def select_main_category(store_id):
    item = MainCategory.query.filter(MainCategory.store_id == store_id).all()
    if not item:
        return '메인 메뉴 카테고리가 없습니다.'
    return item

# 메뉴 조회 (SELECT ID)
def select_menu(menu_id):
    item = Menu.query\
        .filter(Menu.id == menu_id).all()
    if not item:
        return '없는 메뉴입니다.'
    return item

# 메뉴 조회 (SELECT ALL)
def select_menu_all(main_category_id):
    item = Menu.query\
        .filter(SubCategory.id == Menu.menu_category_id)\
        .filter(SubCategory.main_category_id == main_category_id).all()
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


# 서브 카테고리 조회 (SELECT ALL)
def select_sub_category(main_category_id):
    item = SubCategory.query.filter(SubCategory.main_category_id == main_category_id).all()
    if not item:
        return '서브 메뉴 카테고리가 없습니다.'
    return item


# store id의 모든 메뉴 조회
def find_all_menu(store_id):
    items = db.session.query(Menu.id, Menu.name, Menu.price, 
                        MainCategory.name.label('main_category_name'), 
                        SubCategory.name.label('sub_category_name')
                    )\
                    .join(SubCategory, SubCategory.id == Menu.menu_category_id)\
                    .join(MainCategory, MainCategory.id == SubCategory.main_category_id)\
                    .filter(MainCategory.store_id == store_id)\
                    .all()
    return items