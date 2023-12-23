from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from src.auth.forms import SignInForm, SignUpForm
from src.models import User
from src import db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None or not user.validate_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.signin'))
        
        login_user(user)
        
        return redirect(url_for('main.index'))
    
    return render_template('auth/signin.html', form=form)


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for(routes.main_index))
    
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('auth.signin'))
    
    return render_template('auth/signup.html', form=form)


@bp.route('/signout', methods=['GET'])
def signout():
    logout_user()

    return redirect(url_for('main.index'))