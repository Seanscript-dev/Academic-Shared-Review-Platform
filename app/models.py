from . import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='student')
    profile_picture = db.Column(db.String(300), default='icon9.png')

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    filename = db.Column(db.String(300))
    description = db.Column(db.Text)
    uploaded_by = db.Column(db.Integer)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_global = db.Column(db.Boolean, default=False)

class FlashcardSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    owner_id = db.Column(db.Integer)
    is_global = db.Column(db.Boolean, default=False)
    cards = db.relationship('Flashcard', backref='set', cascade='all, delete-orphan')

class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    set_id = db.Column(db.Integer, db.ForeignKey('flashcard_set.id'))
    question = db.Column(db.Text)
    answer = db.Column(db.Text)
