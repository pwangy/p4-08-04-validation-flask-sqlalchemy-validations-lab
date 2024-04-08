from multiprocessing import Value
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, _, name):
        if not name:
            raise ValueError('Name is required')
        author = db.session.query(Author.id).filter_by(name = name).first()
        if author is not None:
            raise ValueError('Name must be unique')
        return name

    @validates('phone_number')
    def validate_phone(self, _, phone_number):
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError('Phone number must be 10 digits')
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'


class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validate_title(self, _, title):
        if not title:
            raise ValueError('Title is required')
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(substring in title for substring in clickbait):
            raise ValueError('Tite must include clickbait')
        return title

    @validates('content', 'summary')
    def validate_length(self, _, string):
        if(_ == 'content'):
            if len(string) < 250:
                raise ValueError('Post must be 250 or more characters long')
        if (_ == 'summary'):
            if len(string) > 250:
                raise ValueError('Post summary must be 240 or more characters long')
        return string

    @validates('cateogry')
    def validate_cateogry(self, _, category):
        if category != 'Fiction' and category != 'Non-Fiction':
            raise ValueError('Category must be either Fiction or Non-Fiction')
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
