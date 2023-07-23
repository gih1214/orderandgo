from flask import session, jsonify
from app.models import db, Table, TableCategory, TableCategoryPage, Order, TableOrderList, Menu


# 주문하기 클릭 시
def make_order(table_id, menu_list):
    table_order_list_item = db.session.query(TableOrderList)\
                                    .filter(TableOrderList.table_id == table_id)\
                                    .filter(TableOrderList.checkingout_at.is_(None))\
                                    .first()
    
    # table_order_list_item이 None이면 첫 주문
    if table_order_list_item is None:
        table_order_list_item = TableOrderList(table_id=table_id)
        db.session.add(table_order_list_item)
        db.session.commit()

    

# 결제할 리스트 출력
def payment_list(table_id):
    item = db.session.query(Order)\
                    .join(TableOrderList, TableOrderList.id == Order.order_list_id)\
                    .join(Table, Table.id == TableOrderList.table_id)\
                    .filter(TableOrderList.checkingout_at.is_(None), Table.id == table_id)\
                    .all()
    if item is None:
        return "잘못됨"
    return item