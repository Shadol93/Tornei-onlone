from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    games = db.relationship('Game', secondary='user_game', backref='players', lazy='dynamic')
    newsletters = db.relationship('Newsletter', secondary='user_newsletter', backref='subscribers', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))  # FPS, MOBA, RPG, etc.
    min_players = db.Column(db.Integer, default=1)
    max_players = db.Column(db.Integer, default=10)

class Newsletter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text)
    frequency = db.Column(db.String(20))  # daily, weekly, monthly

user_game = db.Table('user_game',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('game_id', db.Integer, db.ForeignKey('game.id'), primary_key=True)
)

user_newsletter = db.Table('user_newsletter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('newsletter_id', db.Integer, db.ForeignKey('newsletter.id'), primary_key=True)
)
