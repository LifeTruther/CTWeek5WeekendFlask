from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import uuid

# Adding Flask security for passwords
from werkzeug.security import generate_password_hash, check_password_hash

# creates hex tokens for our API access
import secrets

# imports login manager from flask_login package
from flask_login import LoginManager, UserMixin

#Marshmallow marshaller
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id) 

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    email = db.Column(db.String(150), nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)
    token = db.Column(db.String, unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, password, token = '', id = ''):
        self.id = self.set_id()
        self.email = email
        self.password = self.set_password(password)
        self.token = self.set_token(24)
    
    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self, length):
        return secrets.token_hex(length)

class Stories(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    summary = db.Column(db.String(200), nullable = False)
    category = db.Column(db.String(150), nullable = True)
    relevantdx = db.Column(db.String(200), nullable = True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)


    def __init__(self, name, summary, category, relevantdx, user_token, id=''):
        self.id = self.set_id()
        self.name = name
        self.summary = summary
        self.category = category
        self.relevantdx = relevantdx
        self.user_token = user_token
    
    def set_id(self):
        return(secrets.token_urlsafe())

# Creating our Marshaller to pull k,v pairs out of Story instance attributes
class StorySchema(ma.Schema):
    class Meta:
        # detailing which fields to pull out of our story and send to API call & vice versa
        fields = ['id', 'name', 'summary', 'category', 'relevantdx','user_token']

#take a python class object, iterate through our field, and add to dictionary
story_schema = StorySchema()
stories_schema = StorySchema(many = True)