from app.models import db, User

def create_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user

def get_user_by_id(id):
    return User.query.filter_by(id=id).first()

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()