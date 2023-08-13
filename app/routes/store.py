from flask import render_template, jsonify, request, session


from app.routes import store_bp

@store_bp.route('/')
def index():
    return render_template('adm.html')
  
@store_bp.route('/product')
def product():
    return render_template('store_product.html')

@store_bp.route('/set_menu')
def set_menu():
    return render_template('set_menu_product.html')