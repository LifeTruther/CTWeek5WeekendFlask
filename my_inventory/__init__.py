from flask import Flask
from config import Config
from .site.routes import site
from .authentication.routes import auth
from flask_migrate import Migrate
from .models import db, login_manager
from .api.routes import api

app=Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(site)
app.register_blueprint(auth)
app.register_blueprint(api)

db.init_app(app)

login_manager.init_app(app)
login_manager.login_view = 'auth.signin' #Specify what page to load for nonauth users if try to visit protected route

migrate = Migrate(app, db)







from .models import User