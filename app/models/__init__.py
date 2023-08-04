import json
from app import db
from datetime import datetime

'''
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(512), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'



class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text)
    test = db.Column(db.Text)

    def __repr__(self):
        return f'<Post {self.title}>'
    
class Test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text)
    test2 = db.Column(db.Text)

    def __repr__(self):
        return f'<Post {self.title}>'
'''

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(50), unique=True)
    birthday = db.Column(db.Date, nullable=False)
    tel = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True)
    address = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    last_logged_at = db.Column(db.DateTime, nullable=True)

    #def __repr__(self):
    #    return f'<User {self.title}>'


class Store(db.Model):
    __tablename__ = 'store'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(50), unique=True)
    address = db.Column(db.String(150), nullable=False)
    tel = db.Column(db.String(50), nullable=False)
    manager_name = db.Column(db.String(50), nullable=False)
    manager_tel = db.Column(db.String(50), nullable=False)
    logo_img = db.Column(db.String(150), nullable=False)
    store_image = db.Column(db.String(150), nullable=False)
    main_description = db.Column(db.Text, nullable=False)
    sub_description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    last_logged_at = db.Column(db.DateTime, nullable=True)

    #def __repr__(self):
    #    return f'<Store {self.title}>'


class TableCategory(db.Model):
    __tablename__ = 'table_category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    category_name = db.Column(db.String(50), nullable=True)

    #def __repr__(self):
    #    return f'<TableCategory {self.title}>'


# class TableCategoryPage(db.Model):
#     __tablename__ ='table_category_page'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     table_category_id = db.Column(db.Integer, db.ForeignKey('table_category.id'))
#     page = db.Column(db.Integer, nullable=False)


class Table(db.Model):
    __tablename__ = 'table'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=True)
    seat_count = db.Column(db.Integer, nullable=True)
    
    # number = db.Column(db.Integer, nullable=True)
    # order = db.Column(db.Integer, nullable=True)
    
    is_group = db.Column(db.Integer, nullable=True)
    group_color = db.Column(db.String(50), nullable=True)
    table_category_id = db.Column(db.Integer, db.ForeignKey('table_category.id'))
    page = db.Column(db.Integer, nullable=True)
    position = db.Column(db.Integer, nullable=True)
    # category_page_id = db.Column(db.Integer, db.ForeignKey('table_category_page.id'))

    #def __repr__(self):
    #    return f'<Table {self.title}>'


class MainCategory(db.Model):
    __tablename__ = 'main_category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    name = db.Column(db.String(150), nullable=False)

    #def __repr__(self):
    #    return f'<MainCategory {self.title}>'


class SubCategory(db.Model):
    __tablename__ = 'sub_category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    main_category_id = db.Column(db.Integer, db.ForeignKey('main_category.id'))
    name = db.Column(db.String(150), nullable=False)

    #def __repr__(self):
    #    return f'<SubCategory {self.title}>'


class MenuOption(db.Model):
    __tablename__ = 'menu_option'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    page = db.Column(db.Integer, nullable=True)
    position = db.Column(db.Integer, nullable=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'))

    #def __repr__(self):
    #    return f'<MenuOption {self.title}>'


class Menu(db.Model):
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(150), nullable=True)
    main_description = db.Column(db.Text, nullable=True)
    sub_description = db.Column(db.Text, nullable=True)
    is_soldout = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    page = db.Column(db.Integer, nullable=True)
    position = db.Column(db.Integer, nullable=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    menu_category_id = db.Column(db.Integer, db.ForeignKey('sub_category.id'))
    #def __repr__(self):
    #    return f'<Menu {self.title}>'


# class MenuHasOption(db.Model):
#     __tablename__ = 'menu_has_option'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
#     option_id = db.Column(db.Integer, db.ForeignKey('menu_option.id'))


class OrderStatus(db.Model):
    __tablename__ = 'order_status'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.String(150), nullable=False)

    #def __repr__(self):
    #    return f'<OrderStatus {self.title}>'


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ordered_at = db.Column(db.DateTime, default=datetime.now)
    order_status_id = db.Column(db.Integer, db.ForeignKey('order_status.id'))
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    order_list_id = db.Column(db.Integer, db.ForeignKey('table_order_list.id'))
    menu_options = db.Column(db.Text)
    
    def set_menu_options(self, options_dict):
          # Python Dictionary를 JSON 형식으로 변환하여 저장
        self.menu_options = json.dumps(options_dict)

    def get_menu_options(self):
        # JSON 형식의 데이터를 Python Dictionary로 변환하여 반환
        return json.loads(self.menu_options) if self.menu_options else {}

    #def __repr__(self):
    #    return f'<Order {self.title}>'


# class OrderHasOption(db.Model):
#     __tablename__ = 'order_has_option'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
#     menu_option_id = db.Column(db.Integer, db.ForeignKey('menu_option.id'))


class TableOrderList(db.Model):
    __tablename__ = 'table_order_list'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    checkingin_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    checkingout_at = db.Column(db.DateTime, index=True, nullable=True)

    #def __repr__(self):
    #    return f'<TableOrderList {self.title}>'


class Payment_method(db.Model):
    __tablename__ = 'payment_method'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    method = db.Column(db.String(50), nullable=False)

    #def __repr__(self):
    #    return f'<Payment_method {self.title}>'


class Payment(db.Model):
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    payment_amount = db.Column(db.Integer, nullable=False)
    payment_datetime = db.Column(db.DateTime, default=datetime.now)
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))
    payment_method_id = db.Column(db.Integer, db.ForeignKey('payment_method.id'))
    table_order_list_id = db.Column(db.Integer, db.ForeignKey('table_order_list.id'))

    #def __repr__(self):
    #    return f'<Payment {self.title}>'
