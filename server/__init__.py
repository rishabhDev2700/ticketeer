from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from server.authentication import authentication
from server.ticketing import ticketing
from server.models import db
def create_app(config=None):
    app = Flask(__name__,instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rishabhdev:secretpassword@localhost/ticketer'
    if config is None:
        app.config.from_pyfile('config.py', silent=True)
    db.init_app(app)
    migrate = Migrate(app,db)
    with app.app_context():
        from server.models import User, Ticket, Tag, Company, Category 
        db.create_all()
    
    app.register_blueprint(authentication)
    app.register_blueprint(ticketing)

    return app

