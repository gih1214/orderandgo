from flask import session
from app.models import db, Table, TableCategory


# 테이블 카테고리 생성
def create_table_catgory(data):
    item = TableCategory(data['store_id'], data['category_name'])
    db.session.add(item)
    db.session.commit()
    db.session.refresh(item)
    return item

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

# 테이블 카테고리 조회
def select_table(table_category_id):
    item = Table.query.filter(Table.table_category_id == table_category_id).all()
    if not item:
        return '잘못됨'
    return item

# 테이블 카테고리 수정
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


# 테이블 카테고리 삭제
def delete_table(table_id):
    item = Table.query.filter(Table.id == table_id).first()
    if not item:
        return '잘못됨'
    
    session.delete(item)
    session.commit()
    return True
