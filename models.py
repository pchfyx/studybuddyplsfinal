from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# Association table for many-to-many relationship between users and groups
user_groups = db.Table('user_groups',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('study_group.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_groups = db.relationship('StudyGroup', backref='creator', lazy=True)
    joined_groups = db.relationship('StudyGroup', secondary=user_groups, backref=db.backref('members', lazy=True))
    
    def __repr__(self):
        return f'<User {self.username}>'

class StudyGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    subject = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    materials = db.relationship('StudyMaterial', backref='group', lazy=True)
    posts = db.relationship('GroupPost', backref='group', lazy=True)
    
    def __repr__(self):
        return f'<StudyGroup {self.name}>'

class StudyMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    filepath = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    group_id = db.Column(db.Integer, db.ForeignKey('study_group.id'), nullable=False)
    uploader_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    uploader = db.relationship('User', backref='uploaded_materials')
    
    def __repr__(self):
        return f'<StudyMaterial {self.filename}>'

class GroupPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    group_id = db.Column(db.Integer, db.ForeignKey('study_group.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', backref='posts')
    
    def __repr__(self):
        return f'<GroupPost {self.id}>'