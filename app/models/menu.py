import json
from flask import jsonify, session
from sqlalchemy import desc
from app.models import MainCategory, Order, SubCategory, db, Menu, MenuOption

# 메뉴 id 생성
'''
def create_menu(store_id, menu_category_id):
    menu = Menu(store_id=store_id, menu_category_id=menu_category_id)
    db.session.add(menu)
    db.session.commit()
    print('DB에 메뉴 생성 완료')
    print(menu)
    return menu
'''

# 메뉴 생성
def create_menu(name, price, image, main_description, is_soldout, store_id, menu_category_id, page, position):
    menu = Menu(name=name, price=price, image=image, main_description=main_description,
                is_soldout=is_soldout, store_id=store_id, menu_category_id=menu_category_id, page=page, position=position)
    db.session.add(menu)
    db.session.commit()
    return menu # 커밋된 메뉴 리턴

# 메뉴 옵션 생성
def create_menu_option(option_list, menu_id):
    page = 1
    position = 1
    for o in option_list:
        menu_option = MenuOption(name=o['name'], price=o['price'], page=page, position=position, menu_id=menu_id)
        db.session.add(menu_option)
        if position == 8:
            page += 1
            position = 1
        else:
            position += 1
    db.session.commit()
    return True

# 메뉴 마지막 행의 id 값 조회 (스토어별)
def select_pre_menu_id(store_id):
    menu = Menu.query.filter(Menu.store_id == store_id).order_by(desc(Menu.id)).first()
    if not menu:
        return 0
    return menu.id

# 이미지 조회
def check_image_exsit(menu_id):
    item = Menu.query.filter(Menu.id == menu_id).first()
    if not item.image:
        return '해당 메뉴에 이미지가 없습니다.'
    return item.image

# 메뉴 수정
def update_menu(menu_id, name, price, images, main_description, is_soldout, store_id, menu_category_id):
    item = Menu.query.filter(Menu.id == menu_id).first()
    if not item:
        return '해당 메뉴가 없습니다.'
    item.name = name
    item.price = price
    item.image = images
    item.main_description = main_description
    item.is_soldout = is_soldout
    item.menu_category_id = menu_category_id
    db.session.commit()
    return item

# 메뉴 옵션 삭제 (개별)
def delete_menu_option(option_id):
    item = MenuOption.query.filter(MenuOption.id == option_id).all()
    if not item:
        return '메뉴 옵션이 없습니다.'
    db.session.delete(item)
    db.session.commit()
    return True

# 메뉴 옵션 조회 (SELECT ID)
def select_menu_option(option_id):
    item = MenuOption.query.filter(MenuOption.id == option_id).all()
    if not item:
        return False
    return item

# 메뉴 옵션 조회
def select_menu_option_all(menu_id):
    item = MenuOption.query.filter(MenuOption.menu_id == menu_id).all()
    if not item:
        return False
    return item

# 메뉴 옵션 존재여부 조회
def check_options_exist(menu_id):
    check_option = MenuOption.query.filter(MenuOption.menu_id == menu_id).all()
    if not check_option:
        return '등록된 옵션이 없습니다.'
    else:
        delete_options = delete_all_menu_option(menu_id)
        return delete_options

# 메뉴 옵션 삭제 (한 개의 메뉴에 등록된 모든 옵션)
def delete_all_menu_option(menu_id):
    options = MenuOption.query.filter(MenuOption.menu_id == menu_id).all()
    if not options:
        return '메뉴 옵션이 없습니다.'
    for o in options:
        db.session.delete(o)
    db.session.commit()
    return True

# 메뉴 카테고리 조회 (SELECT ALL)
def select_main_category(store_id):
    item = MainCategory.query.filter(MainCategory.store_id == store_id).all()
    return item

# 메뉴 서브 카테고리 조회 (SELECT ALL)
def select_sub_category(main_category_id):
    item = db.session.query(SubCategory)\
                    .filter(SubCategory.main_category_id == main_category_id)\
                    .all()
    return item

# 메뉴 조회 (SELECT ID)
def select_menu(menu_id):
    item = Menu.query\
        .filter(Menu.id == menu_id).all()
    if not item:
        return '없는 메뉴입니다.'
    return item


# 메뉴 조회 (SELECT ALL)
def select_menu_all(menu_category_id):
    item = Menu.query\
        .filter(Menu.menu_category_id == menu_category_id).all()
    if not item:
        return [] # 카테고리에 메뉴가 하나도 없음, 오류 발생
    return item

# 메뉴 조회 (메인 카테고리 아이디)
def select_menu_all_to_main_category(main_category_id):
    sub_categories = SubCategory.query\
        .filter_by(main_category_id=main_category_id).all()
    item = Menu.query\
        .filter(Menu.menu_category_id.in_([sub_category.id for sub_category in sub_categories])).all()
    if not item:
        return [] # 카테고리에 메뉴가 하나도 없음, 오류 발생
    return item

# 메뉴 삭제
def delete_menu(menu_id):
    item = Menu.query.filter(Menu.id == menu_id).first()
    if not item:
        return False
    
    # 메뉴 옵션 삭제
    delete_options = delete_all_menu_option(menu_id)

    # 메뉴 삭제
    db.session.delete(item)
    db.session.commit()
    return True

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

# 메뉴 페이지, 포지션 마지막 값 가져오기
def find_last_menu_page(store_id):
    menu = Menu.query.filter(Menu.store_id == store_id).order_by(desc(Menu.page), desc(Menu.position)).first()
    if not menu:
        return 0
    return menu

# 메뉴 조회 - 메뉴가 이용 중인 테이블에 있는지 조회
def select_menu_yn(id):
    menu = Menu.query.filter(Menu.id == id).first()
    if menu:
        item = Order.query.filter(Order.menu_id == menu.id).first()
        if item: # order 테이블에 해당 menu_id가 있으면 삭제 불가능 -> False
            return False
        else: # order 테이블에 없으면 삭제 가능 -> True
            return True
    else: # meun 테이블에 데이터가 없으므로 잘못된 접근:삭제 불가능 -> False
        return False

# 메뉴 위치 변경
def move_menu(json_data):
    print('json_data,',json_data)
    for m in json_data:
        menu = Menu.query.filter(Menu.id == m['menu_id']).first()
        if not menu: # 잘못된 접근 - 메뉴 id 없음
            return False
        menu.menu_category_id = m['sub_category_id']
        menu.page = m['page']
        menu.position = m['position']
        db.session.commit()
    return True