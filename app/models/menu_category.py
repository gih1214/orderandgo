from flask import session
from app.models import Menu, db, MainCategory, SubCategory

# 메인카테고리 생성
def create_main_category(store_id, name):
    main_category = MainCategory(store_id=store_id, name=name)
    db.session.add(main_category)
    db.session.commit()
    return main_category

# 서브카테고리 생성
def create_sub_category(main_category_id, name):
    sub_category = SubCategory(main_category_id=main_category_id, name=name)
    db.session.add(sub_category)
    db.session.commit()
    return True

# 메뉴id 생성에 필요한 메인, 서브 카테고리 id 조회
def select_main_and_sub_category_by_store_id(store_id):
    main_category = MainCategory.query.filter(MainCategory.store_id == store_id).first()
    main_id = main_category.id
    menu_category = SubCategory.query.filter(SubCategory.main_category_id == main_category.id).first()
    menu_id = menu_category.id
    return menu_id

# 메뉴로 메인, 서브 카테고리 모두 조회
def get_main_and_sub_category_by_menu_id(menu):
    try:

        if not menu:
            return None, None  # 메뉴가 없으면 None을 반환합니다.

        # 메뉴와 연결된 서브 카테고리를 조회합니다.
        sub_category = SubCategory.query.get(menu.menu_category_id)

        if not sub_category:
            return None, None  # 서브 카테고리가 없으면 None을 반환합니다.

        # 서브 카테고리와 연결된 메인 카테고리를 조회합니다.
        main_category = MainCategory.query.get(sub_category.main_category_id)

        if not main_category:
            return None, None  # 메인 카테고리가 없으면 None을 반환합니다.

        return main_category, sub_category  # 메인 카테고리와 서브 카테고리를 반환합니다.

    except Exception as e:
        print(f"Error: {str(e)}")
        return None, None  # 오류 발생 시 None을 반환합니다.


