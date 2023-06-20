from flask import render_template
from app.routes import pos_bp

@pos_bp.route('/tableList')
def index():
    return render_template('pos/table_list.html')

@pos_bp.route('/order/<table_id>', methods=['GET'])
def order(table_id):
    return render_template('/pos/order.html')