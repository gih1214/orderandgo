from flask import session, jsonify
from flask_login import current_user
from app.models import db, User, Store, Payment, Payment_method, Payment_status, TablePaymentList, TableOrderList, Table, Order
import bcrypt
from sqlalchemy import func

from datetime import datetime
from flask_login import login_user, logout_user

from app.models.menu_category import create_main_category, create_sub_category
from app.models.table import create_table_category


# TablePaymentList 생성
def create_table_payment_list(store_id, table_id, first_order_time, order_details, discount, extra_charge, payment_time):
    table_payment_list_item = TablePaymentList(store_id=store_id, table_id=table_id, first_order_time=first_order_time, order_details=order_details, discount=discount, extra_charge=extra_charge, payment_time=payment_time)
    db.session.add(table_payment_list_item)
    db.session.commit()

    return table_payment_list_item


# Payment 생성
def create_payment(table_payment_list_id, payment_method_id, payment_status, payment_amount, payment_time):
    payment_item = Payment(table_payment_list_id=table_payment_list_id, payment_method_id=payment_method_id, payment_status=payment_status, payment_amount=payment_amount, payment_datetime=payment_time)
    db.session.add(payment_item)
    db.session.commit()

    return payment_item


# Table과 관련된 Order, TableOrderList 삭제하기
def delete_order_tableorderlist(store_id, table_id):
    table_order_list_item = db.session.query(TableOrderList)\
                                    .filter(TableOrderList.store_id == store_id)\
                                    .filter(TableOrderList.table_id == table_id)\
                                    .first()
    table_order_list_id = table_order_list_item.id

    # Order 지우기
    order_items = db.session.query(Order)\
                        .filter(Order.order_list_id == table_order_list_id)\
                        .all()
    for o in order_items:
        db.session.delete(o)

    # TableOrderList 지우기
    db.session.delete(table_order_list_item)

    db.session.commit()


# 결제정보 저장
def create_payment_database(data):    
    # store_id = current_user.id
    store_id = 16   # temp
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
        payment_time = datetime.now()
        p = data['payment']

        first_ordered_time = db.session.query(func.min(Order.ordered_at))\
                                    .filter(Order.table_id == table_id)\
                                    .scalar()
        
        if data['total_price'] == p['price']+p['extra_charge']-p['discount']:     # 1. 일반결제
            print("@@@@111")
            # TablePaymentList, Payment 생성하기
            table_payment_list_item = create_table_payment_list(store_id, table_id, first_ordered_time, str(data['order_list']), p['discount'], p['extra_charge'], payment_time)
            create_payment(table_payment_list_item.id, p['method'], 1, p['price'], payment_time)

            # Table과 관련된 Order, TableOrderList 삭제하기
            delete_order_tableorderlist(store_id, table_id)

        else:                                   # 2. 분할 결제
            check_table_payment_list = db.session.query(TablePaymentList)\
                                            .filter(TablePaymentList.store_id == store_id)\
                                            .filter(TablePaymentList.table_id == table_id)\
                                            .filter(TablePaymentList.first_order_time == data['first_order_time'])\
                                            .first()
            if check_table_payment_list is None:        # 2-1. 첫번째 분할결제
                print("@@@@222-1")
                # TablePaymentList, Payment 생성하기
                table_payment_list_item = create_table_payment_list(store_id, table_id, first_ordered_time, str(data['order_list']), p['discount'], p['extra_charge'], payment_time)
                create_payment(table_payment_list_item.id, p['method'], 1, p['price'], payment_time)
            else:
                sum_payment = db.session.query(func.sum(Payment.payment_amount))\
                                    .filter(Payment.table_payment_list_id == check_table_payment_list.id)\
                                    .filter(Payment.payment_status == 1)\
                                    .scalar()
                if sum_payment+p['price']+p['extra_charge']-p['discount'] != data['total_price']:  # 2-2. 분할결제중
                    print("@@@@222-2")
                    create_payment(check_table_payment_list.id, p['method'], 1, p['price'], payment_time)
                else:                                   # 2-3. 마지막 분할결제
                    print("@@@@222-3")
                    create_payment(check_table_payment_list.id, p['method'], 1, p['price'], payment_time)
                    
                    # Table과 관련된 Order, TableOrderList 삭제하기
                    delete_order_tableorderlist(store_id, table_id)
        return jsonify({'status':'success'}), 200
    except:
        db.session.rollback()
        return jsonify({'status':'fail'}), 500



'''
order, tableorderlist에 table_id를 nullable = true로 하고 굳이 삭제 안하고 -> 철회!!!
결제할 떄 미리 프론트에 tableorderlist.id를 보낸 다음
결제시 이 정보를 같이 넘겨받아 tablepaymentlist에 3개합쳐진 유니크키로써 확인한다(<->first_order_time) -> 철회!!

디비마이그레이션하기!!! -> 했음

해야할 것)
결제도중 전깋ㅎ... 나갔을 때 보낼 데이터 만들기
결제취소 api 만들기 -> 안해도된댕!!!!!ㅎㅎㅎㅎㅎ
잘 만들었는데 discount랑 extra_charge가 고려가 안되어있는 것 같음... -> 흠 이제 된 것 같음!


메뉴/메뉴옵션 생성할 때 page, position 맨 뒤에로 설정해서 넣기!(아바밧츄)
메뉴 순서변경 api 고민하기(궁지)
'''