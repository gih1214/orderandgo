from flask import render_template
from app.routes import main_bp

@main_bp.route('/')
def index():
    from app.models.user import create_user, get_user_by_id
    # create_user('test', 'asd123', '이름', '2000-01-01', '010-0000-0000', 'test@test.co.kr', '부산 어딘가')
    print('실행됨')
    return render_template('index.html')
