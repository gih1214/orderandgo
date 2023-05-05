from app.models import db, Post

def create_post(title, body):
    post = Post(title=title, body=body)
    db.session.add(post)
    db.session.commit()
    return post

def get_post_by_id(id):
    return Post.query.filter_by(id=id).first()

def get_all_posts():
    return Post.query.all()