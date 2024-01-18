from flask import session, jsonify
from app.models import Order, TableOrderList, db, Table, TableCategory

#################
# 테이블 카테고리
#################

# 테이블 카테고리 생성/수정
def create_table_category(table_category_list, store_id):
    for t in table_category_list:
        
        if not t['id']: # id 없으면 신규 생성
            
            table_category = TableCategory(store_id=store_id, category_name=t['category_name'], position=t['position'])
            db.session.add(table_category)
            db.session.commit()
            for i in range(20):
                data = {
                    'name': t['category_name'] + str(i+1),
                    'seat_count' : None, 
                    'is_group' : None,
                    'table_category_id' : table_category.id,
                    'page': 1,
                    'position' : i+1
                }
                item = Table(name=data['name'], seat_count=data['seat_count'], is_group=data['is_group'], table_category_id=data['table_category_id'], page=data['page'], position=data['position'])
                db.session.add(item) 
            db.session.commit()
        else: # id 있으면 수정
            table_category = TableCategory.query.filter(TableCategory.id == t['id']).first()
            table_category.category_name = t['category_name']
            table_category.position = t['position']
            db.session.commit()
    return True


# # 테이블 카테고리 생성
'''#     db.session.add(item)

            #     db.session.commit()
            #     db.session.refresh(item)
def create_table_category(store_id, category_name, position=None):
    table_category = TableCategory(store_id=store_id, category_name=category_name, position=position)
    db.session.add(table_category)
    db.session.commit()
    return table_category
'''

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


# 테이블 이름 수정
def update_table_name(table_id, name):
    table_item = db.session.query(Table)\
                        .filter(Table.id == table_id)\
                        .first()
    if not table_item:
        return jsonify({'message': 'Not found table id'}), 400
    table_item.name = name
    db.session.commit()
    return jsonify({'message': 'Table name updated successfully'}), 200  


# 테이블 위치 수정
def update_table_position(table_id_fir, table_id_sec):
    fir_table_item = db.session.query(Table)\
                        .filter(Table.id == table_id_fir)\
                        .first()
    
    sec_table_item = db.session.query(Table)\
                        .filter(Table.id == table_id_sec)\
                        .first()
    if fir_table_item is None or sec_table_item is None:
        return jsonify({'message': 'Not found table id'}), 400
    
    fir_table_item.position = sec_table_item.position
    sec_table_item.position = fir_table_item.position
    db.session.commit()
    return jsonify({'message': 'Table position updated successfully'}), 200  


# 테이블 생성
def create_table(data):
    item = Table(name=data['name'], seat_count=data['seat_count'], is_group=0, table_category_id=data['table_category'], page=data['page'], position=data['position'])
    db.session.add(item)
    db.session.commit()
    db.session.refresh(item)
    return jsonify({'table_id': item.id, 'table_name': item.name}), 200

# 테이블 조회 - 테이블에 해당 테이블 카테고리가 있는지 조회
# 테이블 카테고리 삭제 시 테이블 이용 유무 확인하기 위함
def select_table_id(id):
    table_list = Table.query.filter(Table.table_category_id == id).all()
    cnt = 0
    for t in table_list:
        item = db.session.query(TableOrderList).filter(TableOrderList.table_id == t.id).first()
        if not item:
            continue
        else:
            cnt += 1
        if cnt > 0: # 이용 중인 테이블이 하나라도 있으면 False
            return False
    return True