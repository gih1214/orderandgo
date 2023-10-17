from flask import session
from flask_login import current_user
from app.models import db, User, Store, Payment, Payment_method, Payment_status, TablePaymentList, TableOrderList, Table, Order
import bcrypt
from sqlalchemy import func

from datetime import datetime
from flask_login import login_user, logout_user

from app.models.menu_category import create_main_category, create_sub_category
from app.models.table import create_table_category


# TablePaymentList 생성
def create_table_payment_list(store_id, table_id, order_details, discount, first_order_time, payment_time):
    table_payment_list_item = TablePaymentList(store_id=store_id, table_id=table_id, order_details=order_details, discount=discount, first_order_time=first_order_time, payment_time=payment_time)
    session.add(table_payment_list_item)
    session.commit()

    return table_payment_list_item


# Payment 생성
def create_payment(table_payment_list_id, payment_method_id, payment_status, payment_amount, payment_time):
    payment_item = Payment(table_payment_list_id=table_payment_list_id, payment_method_id=payment_method_id, payment_status=payment_status, payment_amount=payment_amount, payment_datetime=payment_time)
    session.add(payment_item)
    session.commit()

    return payment_item


# Table과 관련된 Order, TableOrderList 삭제하기
def delete_order_tableorderlist(store_id, table_id):
    table_order_list_item = session.query(TableOrderList)\
                                    .filter(TableOrderList.store_id == store_id)\
                                    .filter(TableOrderList.table_id == table_id)\
                                    .first()
    table_order_list_id = table_order_list_item.id

    table_order_list_item.delete()

    order_items = session.query(Order)\
                        .filter(Order.order_list_id == table_order_list_id)\
                        .all()
    for o in order_items:
        o.delete()

    session.commit()


# 결제정보 저장
def create_payment(data):    
    store_id = current_user.id
    print("@#$@#$#@$", store_id)

    '''
    1. 일반결제
    2. 분할결제 - 판단 근거 : TablePaymentList의 유무 / Payment의 총 합계
        2-1. 첫번째 분할결제 - TablePaymentList을 만든다. + Payment를 추가한다.
        2-2. 분할결제중     -  Payment를 추가한다.
        2-3. 마지막 분할결제 - table에 관련된 order db를 삭제시킨다. + Payment를 추가한다.
    '''
    try:
        table_id = data['table_id']
        payment_time = datetime.now
        p = data['payment']

        if data['total_price'] == p['price']:     # 1. 일반결제
            first_ordered_time = session.query(func.min(Order.ordered_at))\
                                        .filter(Order.table_id == table_id)\
                                        .scalar()

            # TablePaymentList, Payment 생성하기
            table_payment_list_item = create_table_payment_list(store_id, table_id, data['order_list'], p['discount'], first_ordered_time, payment_time)
            create_payment(table_payment_list_item.id, p['method'], 1, p['price'], payment_time)

            '''
            # Table과 관련된 Order, TableOrderList 삭제하기
            delete_order_tableorderlist(store_id, table_id)
            '''

        else:                                   # 2. 분할 결제
            check_table_payment_list = session.query(TablePaymentList)\
                                            .filter(TablePaymentList.store_id == store_id)\
                                            .filter(TablePaymentList.table_id == table_id)\
                                            .filter(TablePaymentList.table_order_list_id == data['table_order_list_id'])\
                                            .first()
            if check_table_payment_list is None:        # 2-1. 첫번째 분할결제
                # TablePaymentList, Payment 생성하기
                table_payment_list_item = create_table_payment_list(store_id, table_id, data['order_list'], p['discount'], first_ordered_time, payment_time)
                create_payment(table_payment_list_item.id, p['method'], 1, p['price'], payment_time)
            else:
                sum_payment = session.query(func.sum(Payment.payment_amount))\
                                    .filter(Payment.table_payment_list_id == check_table_payment_list.id)\
                                    .scalar()
                if sum_payment != data['total_price']:  # 2-2. 분할결제중
                    create_payment(table_payment_list_item.id, p['method'], 1, p['price'], payment_time)
                else:                                   # 2-3. 마지막 분할결제
                    create_payment(table_payment_list_item.id, p['method'], 1, p['price'], payment_time)
                    '''
                    # Table과 관련된 Order, TableOrderList 삭제하기
                    delete_order_tableorderlist(store_id, table_id)
                    '''

    except:
        session.rollback()



'''
order, tableorderlist에 table_id를 nullable = true로 하고 굳이 삭제 안하고
결제할 떄 미리 프론트에 tableorderlist.id를 보낸 다음
결제시 이 정보를 같이 넘겨받아 tablepaymentlist에 3개합쳐진 유니크키로써 확인한다(<->first_order_time)

디비마이그레이션하기!!!
'''