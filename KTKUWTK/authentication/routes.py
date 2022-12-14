from flask import Blueprint, render_template
from ktkuwtk.forms import UserLoginForm
from ktkuwtk.models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required 

auth = Blueprint('auth', __name__, template_folder = 'auth_templates')

@auth.route('/signup', methods = ['GET', 'POST']) 
def signup(): 
    form = UserLoginForm()
    try:
        if request.method == "POST" and form.validate_on_submit(): 
            email = form.email.data 
            first_name = form.first_name.data
            last_name = form.last_name.data
            password = form.password.data
            user = User(email, first_name, last_name, password = password)

            db.session.add(user)
            db.session.commit()

            flash(f'Koolness! An aKKount was made for {email}', 'user-created')

            return redirect(url_for("auth.signin"))
    except: 
        raise Exception('Yikes! Looks like you entered some yucky form data. :( Please check form data and try again!')
    return render_template('signup.html')

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()

    try:
        if request.method == "POST" and form.validate_on_submit():
            email = form.email.data 
            password = form.password.data
            print(email, password)

            logged_user = User.query.filter(User.email == email).first() 
            if logged_user and check_password_hash(logged_user.password, password): 
                login_user(logged_user)
                flash('Heck YAS! You totes successfully logged in via email/password', 'auth-success') 
                return redirect(url_for('site.profile')) 
            else: 
                flash('Uh oh! Looks like your email or password is invalid!', 'auth-failed')
                return redirect(url_for('auth.signin'))  
    except:
        raise Exception('Yikes! Looks like you entered some yucky form data. :( Please check form data and try again!')
    return render_template('signin.html')
    
@auth.route('/logout')
@login_required 
def logout():
    logout_user()
    return redirect(url_for('site.home'))
