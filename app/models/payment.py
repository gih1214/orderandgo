from flask import session
from flask_login import current_user
from app.models import db, User, Store, Payment, Payment_method, Payment_status, TablePaymentList, TableOrderList, Table, Order
import bcrypt

from datetime import datetime
from flask_login import login_user, logout_user

from app.models.menu_category import create_main_category, create_sub_category
from app.models.table import create_table_category


# 결제정보 저장
def create_payment(data):    
    store_id = current_user.id
    print("@#$@#$#@$", store_id)

    try:
        # TablePaymentList, Payment 생성하기
        table_payment_list_item = TablePaymentList(store_id, data['order_list'], datetime.now)
        session.add(table_payment_list_item)
        session.commit()

        for p in data['payment_list']:
            payment_item = Payment(p['price'], p['method'], 1, datetime.now, table_payment_list_item.id)
            session.add(payment_item)
        session.commit()

        # Table과 관련된 Order, TableOrderList 삭제하기
        table_order_list_item = session.query(TableOrderList)\
                                        .filter(TableOrderList.store_id == store_id)\
                                        .filter(TableOrderList.table_id == data['table_id'])\
                                        .first()
        table_order_list_id = table_order_list_item.id

        table_order_list_item.delete()

        order_items = session.query(Order)\
                            .filter(Order.order_list_id == table_order_list_id)\
                            .all()
        for o in order_items:
            o.delete()

    except:
        session.rollback()