from flask import session
from app.models import db, User
from app.models.auth import update_user_session
import bcrypt

from datetime import datetime

# 회원가입
def create_user(user_id, password, name, birthday, tel, email, address):
    b_day  = datetime.strptime(birthday, '%Y-%m-%d').date()
    user = User(user_id=user_id, password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()),
                name=name, birthday=b_day, tel=tel, email=email, address=address)
    db.session.add(user)
    db.session.commit()
    return True

# 아이디(PK)로 유저 조회
def get_user_by_id(id):
    return User.query.filter_by(id=id).first()

# 유저아이디로 유저 조회
def get_user_by_userid(user_id):
    return User.query.filter_by(user_id=user_id).first()

# 회원정보 수정 (마이페이지)
# 비밀번호, 성명, 생년월일, 전화번호, 이메일, 주소
def update_user(id, password, name, birthday, tel, email, address):
    # id(PK)로 유저 확인
    select_user = User.query.filter_by(id=id).all()
    if len(select_user) == 0:
        return "유저 정보가 없습니다."
    else: # 유저가 맞으면 update
        user = User.query.filter_by(id=id).first()
        if password != bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            user.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        else:
            return "기존 비밀번호와 동일합니다."
        user.name = name
        user.birthday = birthday
        user.tel = tel
        user.email = email
        user.address = address

        db.session.commit()
        return user
    
# 아이디(PK)로 유저 삭제
def delete_user_by_id(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False

# 로그인
def get_user_login(user_id, password):
    user = User.query.filter_by(user_id=user_id).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        update_user_session(user)   # 세션 등록
        return user
    return False

# 로그아웃
def logout():
    session.clear()
