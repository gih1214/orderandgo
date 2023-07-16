from flask import session
from app.models import db, Table, TableCategory, TableCategoryPage


# 테이블 카테고리 페이지 생성
def create_table_catgory_page(table_category_id, page):
    table_category_page_item = TableCategoryPage(table_category_id, page)
    db.session.add(table_category_page_item)
    db.session.commit()
    db.session.refresh(table_category_page_item)


# 테이블 카테고리 페이지 조회
def select_table_category_page(table_category_id):
    item = TableCategoryPage.query.filter(TableCategoryPage.table_category_id == table_category_id).all()
    if not item:
        return '잘못됨'
    return item


# 테이블 카테고리 생성
def create_table_catgory(data):
    table_category_item = TableCategory(data['store_id'], data['category_name'])
    db.session.add(table_category_item)
    db.session.commit()
    db.session.refresh(table_category_item)

    # 테이블 카테고리 만들 때 자동으로 테이블 카테고리 페이지(1페이지로) 생성
    create_table_catgory_page(table_category_item.id, 1)

    return table_category_item


# 테이블 카테고리 조회
def select_table_category(store_id):
    item = TableCategory.query.filter(TableCategory.store_id == store_id).all()
    if not item:
        return '잘못됨'
    return item

# 테이블 카테고리 수정
def update_table_category(table_category_id, value):
    item = TableCategory.query.filter(TableCategory.id == table_category_id).first()
    if not item:
        return '잘못됨'
    
    item['category_name'] = value
    session.commit()
    return True


# 테이블 카테고리 삭제
def delete_table_category(table_category_id):
    item = TableCategory.query.filter(TableCategory.id == table_category_id).first()
    if not item:
        return '잘못됨'
    
    session.delete(item)
    session.commit()
    return True


# 테이블 생성
def create_table(data):
    item = Table(data['name'], data['number'], data['seat_count'], data['table_category'], data['x_axis'], data['y_axis'], data['page'], data['is_group'])
    db.session.add(item)
    db.session.commit()
    db.session.refresh(item)
    return item

# 테이블 조회
def select_table(category_page_id):
    print("@#$",category_page_id)
    item = Table.query.filter(Table.category_page_id == category_page_id).all()
    if not item:
        return '잘못됨'
    return item

# 테이블 수정
def update_table(table_id, change_dict):
    item = Table.query.filter(Table.id == table_id).first()
    if not item:
        return '잘못됨'
    
    change_list = ['seat_count', 'table_category', 'x_axis', 'y_axis', 'page', 'is_group']
    for c in change_dict.keys():
        if c in change_list:
            item[c] = change_dict[c]
            session.commit()
    return True


# 테이블 삭제
def delete_table(table_id):
    item = Table.query.filter(Table.id == table_id).first()
    if not item:
        return '잘못됨'
    
    session.delete(item)
    session.commit()
    return True
