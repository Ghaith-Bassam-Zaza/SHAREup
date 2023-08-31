from flask import Blueprint, render_template, request, flash, redirect, session, url_for, make_response
from app.forms.users import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash,check_password_hash
from app.models import db
from app.models.users import User
from flask_login import login_user, login_required, logout_user, current_user
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies
)

auth = Blueprint('auth',__name__)


@auth.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    title ='login'
    if request.method == 'GET':
        return render_template('auth/login.html',title =title,form=form)

    # for POST requests
    email = request.form.get('email')
    passwrd =request.form.get('passwrd')

    
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()
        # if user exists and password matches
        if user and check_password_hash(user.pswrd,passwrd):
            # start login session
            login_user(user)
            session['username'] = current_user.name

            # create and return response with jwt tokens
            resp = make_response(redirect(url_for('home.home_page')))
            access_token =  create_access_token(identity=email)
            refresh_token =  create_refresh_token(identity=email)
            set_access_cookies(resp,access_token)
            set_refresh_cookies(resp,refresh_token)
            
            return resp
            
        
        # if user does not exists
        flash('username or password are incorrect!')
        return render_template("auth/login.html",title=title,form = form)
            
    
    # if not valid rerender page with errors
    return render_template("auth/login.html",title=title,form = form)


@auth.route('/register',methods=['GET','POST'])
def register():
    title = 'register'
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('auth/register.html',title='register',form = form)
    
    # for POST requests
    email = request.form.get('email')
    name = request.form.get('name')
    passwrd =request.form.get('passwrd')

    # if email already registered refresh page and flash massage
    user = User.query.filter_by(email=email).first()
    if user:
        flash('Email already registered!')
        return redirect(url_for('auth.register'))

    # else create new user with the recieved data, hash passwrd for security
    if form.validate_on_submit():
        new_user = User(email=email,name=name,pswrd=generate_password_hash(passwrd,method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        flash('registered successfully!')
        return redirect(url_for('auth.login'))
    
    # if not valid rerender page with errors
    return render_template("auth/register.html",title=title,form = form)


@auth.route('/logout')
@login_required
def logout():
    # end user session
    session.pop('username',None)
    logout_user()
    # delete jwt token
    resp = make_response(redirect(url_for('home.home_page')))
    unset_jwt_cookies(resp)
    return resp


    