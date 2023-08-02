from flask import session, jsonify
# TableCategory 수정한 것
# from app.models import db, Table, TableCategory, TableCategoryPage, Order, TableOrderList, Menu, OrderHasOption, MenuOption
from app.models import db, Table, TableCategory, Order, TableOrderList, Menu, OrderHasOption, MenuOption


# 주문하기 클릭 시
def make_order(table_id, order_list):
    table_order_list_item = db.session.query(TableOrderList)\
                                    .filter(TableOrderList.table_id == table_id)\
                                    .filter(TableOrderList.checkingout_at.is_(None))\
                                    .first()
    
    # table_order_list_item이 None이면 첫 주문
    if table_order_list_item is None:
        table_order_list_item = TableOrderList(table_id=table_id)
        db.session.add(table_order_list_item)
        db.session.commit()

    for o in order_list:
        # order_status_id는 임의로 1로 함. temp
        order_item = Order(order_status_id=1, menu_id=o['menu_id'], table_id=table_id, order_list_id=table_order_list_item.id)
        db.session.add(order_item)
        db.session.commit()

        # 옵션이 있으면 옵션 추가
        if len(o['option_list']) > 0:
            for oo in o['option_list']:
                option_order_item = OrderHasOption(order_id=order_item.id, menu_option_id=oo)
                db.session.add(option_order_item)
                db.session.commit()

    return True
    

# 주문만 출력
def find_order_list(table_id):
    items = db.session.query(Menu.id, Menu.name, Menu.price, Order.id.label('order_id'))\
                    .join(Order, Order.menu_id == Menu.id)\
                    .join(TableOrderList, TableOrderList.id == Order.order_list_id)\
                    .join(Table, Table.id == TableOrderList.table_id)\
                    .filter(TableOrderList.checkingout_at.is_(None), Table.id == table_id)\
                    .all()
    if items is None:
        return "잘못됨"
    return items


# 주문 옵션 출력
def find_order_option_list(order_id):
    items = db.session.query(MenuOption)\
                    .join(OrderHasOption, OrderHasOption.menu_option_id == MenuOption.id)\
                    .join(Order, Order.id == OrderHasOption.order_id)\
                    .filter(Order.id == order_id)\
                    .all()
    if items is None:
        return "잘못됨"
    return items    