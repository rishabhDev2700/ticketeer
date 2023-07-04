from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

tickets_tags = db.Table('tickets_tags',
    db.Column('ticket_id', db.Integer, db.ForeignKey('ticket.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
    )


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    email = db.Column(db.String(40),unique=True,nullable=False)
    first = db.Column(db.String(30),nullable=False)
    last = db.Column(db.String(40),nullable=False)
    password = db.Column(db.String(128),nullable=False)
    tickets = db.relationship('Ticket',backref='user',lazy=True)
    
    def __repr__(self):
        return '<User %r>' % self.email



class Staff(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    email = db.Column(db.String(40),unique=True,nullable=False)
    first = db.Column(db.String(30),nullable=False)
    last = db.Column(db.String(40),nullable=False)
    password = db.Column(db.String(64),nullable=False)

    def __repr__(self):
        return '<Staff %r>' % self.email



class Ticket(db.Model):
    id= db.Column(db.Integer,primary_key=True, autoincrement=True)
    title = db.Column(db.String(50),nullable=False)
    description = db.Column(db.Text,nullable=True)
    created_on = db.Column(db.DateTime,default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    assigned_to = db.Column(db.Integer,db.ForeignKey('staff.id'))
    is_resolved = db.Column(db.Boolean, default=False)
    tags = db.relationship('Tag',secondary=tickets_tags,backref=db.backref('tickets',lazy='dynamic'))

    def __repr__(self):
        return '<Ticket %r>' % self.title



class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20),unique=True)

    def __repr__(self):
        return '<Tag %r>' % self.name


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50),unique=True)
    description = db.Column(db.Text)
    field = db.Column(db.String(30))

    def __repr__(self):
        return '<Company %r>' % self.name


class Category(db.Model):
    id = db.Column(db.Integer,primary_key=True,)
    name = db.Column(db.String(50),unique=True)
    description = db.Column(db.Text)

    def __repr__(self):
        return '<Category %r>' % self.name
