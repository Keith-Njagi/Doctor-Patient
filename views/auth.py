import socket
from datetime import datetime, timedelta

from is_safe_url import is_safe_url
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, abort, render_template, redirect, url_for, flash
from flask_login import UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Message


from . import login_manager
from main import app

from models.user import UserModel
from models.role import RoleModel
from models.user_role import UserRoleModel

from forms.auth import RegisterForm, LogInForm, ForgotPasswordForm, PasswordResetForm

from utilities.user_role_manager import UserPrivilege

@login_manager.user_loader
def load_user(user_id:int):
    return UserModel.get(int(user_id)) # Fetch the user from the database


"""
Routes for user authentication: login, register, logout
"""
@app.route('/user/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        user = UserModel.fetch_by_email(email=form.email.data)
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash('You are now logged in.', 'success')
                user_id = user.id
                
                next = request.args.get('next')

                # is_safe_url should check if the url is safe for redirects.
                # See http://flask.pocoo.org/snippets/62/ for an example.                
                if next != None: 
                    if not is_safe_url(next, host_ip):
                        return abort(400)

                return redirect(next or url_for('index'))

        flash('Invalid email or password. Please check your credentials and ensure you are a registered user.', 'danger')
        return render_template('user/login.html', form=form)
    return render_template('user/login.html', form=form)

@app.route('/user/logout')
@login_required
def logout():
    logout_user()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))

@app.route('/user/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        #Check whether a user with the same Email or Phone exists
        full_name = form.full_name.data
        email = form.email.data
        phone = form.phone.data

        user_by_email = UserModel.fetch_by_email(email=email)
        if user_by_email:
            flash('A user with this email already exists.', 'danger')
            return redirect(url_for('signup'))
        
        user_by_phone = UserModel.fetch_by_phone(phone=phone)
        if user_by_phone:
            flash('A user with this phone already exists.', 'danger')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = UserModel(full_name=full_name, email=email, phone=phone, password=hashed_password)
        new_user.insert_record()
        
        # Add user roles to registered user
        this_user = UserModel.fetch_by_email(email)

        UserPrivilege.generate_user_role(user_id = this_user.id)
        user_id = UserPrivilege.user_id
        role = UserPrivilege.role
        # Ensure all roles are saved to the db before registering the role to user
        db_roles = UserRoleModel.fetch_all()
        all_privileges = UserPrivilege.all_privileges
        if len(db_roles) == 0:
            for key, value in all_privileges.items():
                new_role = RoleModel(role=value)
                new_role.insert_record()
        # Link role to user
        new_user_role = UserRoleModel(user_id=user_id, role_id=role)
        new_user_role.insert_record()
        # Create access token  
        # privileges = UserPrivilege.privileges

        #log in user
        login_user(this_user) #, remember=form.remember.data)
        flash('You are now logged in.', 'success')

    return render_template('user/register.html', form=form)
