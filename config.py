import os

basedir = os.path.abspath(os.path.dirname(__file__))
# this bit of code sets the path for flask

#SECRET KEY
class Config:

    """
        Sets configuration variables for our Flask app here.
        Eventually will use hidden variable items - but for now,
        we'll leave them exposed in config
    """
    SECRET_KEY = "You might guess..."
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
