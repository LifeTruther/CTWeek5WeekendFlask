from flask import Blueprint, render_template, request
from my_inventory.forms import UserLoginForm
from my_inventory.models import User, db


auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()
    if request.method == 'POST'and form.validate_on_submit():
        email = form.email.data
        password = form.password.data 
        print(email, password)

        user = User(email,password)

        db.session.add(user)
        db.session.commit()

    return render_template('signup.html', form = form)

@auth.route('/signin', methods = ['GET'])
def signin():
    return render_template('signin.html')