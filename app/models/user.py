from flask import session
from app.models import db, User
import bcrypt

# 회원가입
def create_user(username, email, password):
    user = User(username=username, email=email, password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))
    db.session.add(user)
    db.session.commit()
    return user

# 아이디(PK)로 유저 조회
def get_user_by_id(id):
    return User.query.filter_by(id=id).first()

# 유저네임으로 유저 조회
def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

# 아이디(PK)로 유저 삭제
def delete_user_by_id(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False

# 로그인
def get_user_login(username, password):
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return user
    return False

# 로그아웃
def logout():
    session.clear()