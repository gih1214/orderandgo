from flask import render_template, request, jsonify
from app.routes import order_bp

from app.models.order import make_order

# 주문하기 클릭
@order_bp.route('/', methods=['POST'])
def menu_order():

    order_data = request.get_json()
    table_id = order_data['table_id']
    order_list = order_data['order_list']

    try:
        make_order(table_id, order_list)
    except:
        return jsonify("failed"), 400
    
    return jsonify("Success"), 200


# 결제
@order_bp.route('/payment/<table_id>', methods=['GET'])
def table_payment(table_id):
    return "temp"