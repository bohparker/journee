from sqlalchemy import select
from flask import render_template, url_for, request, flash, redirect, g, abort
from flask_login import current_user, login_user, logout_user, login_required

from ..app import db, login_manager
from ..models import User
from . import bp_auth as bp
from .forms import LoginForm, RegistrationForm



@login_manager.unauthorized_handler
def redirect_to_login():
    flash('You must be logged in to view this page.', 'info')
    return redirect(url_for('bp_auth.login'))


@bp.before_request
def get_current_user():
    g.user = current_user


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('bp_views.index'))
    
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        q = select(User).where(User.username == username)
        existing_username = db.session.scalars(q).one_or_none()

        if existing_username:
            flash('Sorry, that username already exists.', 'warning')
            return render_template('register.html', form=form)
        
        new_user = User(username, password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash('You have been registered!', 'success')
        return redirect(url_for('bp_views.index'))
    
    if form.errors:
        for error, message in form.errors.items():
            flash(message[0], 'danger')
            return render_template('register.html', form=form)
        
    return render_template('register.html', form=form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('bp_views.index'))
    
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        q = select(User).where(User.username == username)
        existing_user = db.session.scalars(q).one_or_none()

        if existing_user and existing_user.check_password(password):
            login_user(existing_user)
            flash(f'Welcome, {existing_user.username}.', 'success')
            return redirect(url_for('bp_views.index'))
        
        else:
            flash('Invalid username or password', 'warning')
            return render_template('login.html', form=form)
        
    if form.errors:
        for error, message in form.errors.items():
            flash(message[0], 'danger')
            return render_template('login.html', form=form)
        
    return render_template('login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('bp_views.index'))