from flask import session, jsonify
# TableCategory 수정한 것
# from app.models import Order, TableOrderList, db, Table, TableCategory, TableCategoryPage
from app.models import Order, TableOrderList, db, Table, TableCategory

#################
# 테이블 카테고리
#################


# 테이블 카테고리 생성
def create_table_catgory(data):
    table_category_item = TableCategory(data['store_id'], data['category_name'])
    db.session.add(table_category_item)
    db.session.commit()
    db.session.refresh(table_category_item)

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


#########
# 테이블
#########

# 테이블 생성
def create_table(data):
    item = Table(data['name'], data['number'], data['seat_count'], data['table_category'], data['x_axis'], data['y_axis'], data['page'], data['is_group'])
    db.session.add(item)
    db.session.commit()
    db.session.refresh(item)
    return item

# 테이블 조회
def select_table(table_category_id):
    item = Table.query.filter(Table.table_category_id == table_category_id).all()
    if not item:
        return '잘못됨'
    return item

# 테이블 이동/합석
def move_table(end_id, start_id):
    #print('이동하고픈 테이블 : ', start_id)
    #print('가만히 있는 테이블 : ', end_id)
    for s in start_id:
        # order 테이블에 table 번호 변경
        order_table = Order.query.filter(Order.table_id == s).update({'table_id': end_id})\
        # table_order_list 테이블에 table 번호 변경
        list_table = TableOrderList.query.filter(TableOrderList.table_id == s).update({'table_id': end_id})

        if not order_table:
            return '없는 정보입니다.'
        elif not list_table:
            return '없는 정보입니다.'
        
    db.session.commit()
    print('테이블 이동/합석 완료')
    return True

# 테이블 수정
def update_table(table_id, change_dict):
    item = Table.query.filter(Table.id == table_id).first()
    if not item:
        return '잘못됨'
    
    change_list = ['seat_count', 'table_category', 'x_axis', 'y_axis', 'page', 'is_group']
    for c in change_dict.keys():
        if c in change_list:
            item[c] = change_dict[c]
            db.session.commit()
    return True


# 테이블 삭제
def delete_table(table_id):
    item = Table.query.filter(Table.id == table_id).first()
    if not item:
        return '잘못됨'
    
    db.session.delete(item)
    db.session.commit()
    return True


# 테이블 그룹 설정
def set_table_group(table_list):
    for t in table_list:
        item = db.session.query(Table).filter(Table.id == t['table_id']).first()
        if not item:
            return jsonify({'message': 'Not found table id'}), 400
        
        item.is_group = t['group_id']
        item.group_color = t['group_color']
        db.session.commit()

    return jsonify({'message': 'User updated successfully'}), 200  
