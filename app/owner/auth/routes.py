from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user
from flask_mail import Message
from werkzeug.security import generate_password_hash

from app import app, login_manager, db, models, mail
from app.models import Owner
from app.owner.auth.forms import *


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        # obtain a user
        owner = Owner.query.get(form.username.data)
        # verify password
        if owner.verify_password(form.password.data):
            # log in the user
            login_user(owner, remember=form.remember_me.data)
            flash('login success!')
            # send email
            return redirect(url_for('owner'))
        else:
            flash('incorrect password')
            return redirect(url_for('login'))

    return render_template('login.html', form=form, title='login')


@login_manager.user_loader
def load_user(user_id):
    owner = Owner.query.get(user_id)
    return owner


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('owner'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Registration()
    if form.validate_on_submit():
        owner = models.Owner(id=form.user.data,
                             password_hash=generate_password_hash(form.password.data),
                             image_location=form.image.data,
                             phone_number=form.contact.data,
                             email=form.email.data,
                             )
        db.session.add(owner)
        db.session.commit()

        # Send an email to the new Owner
        msg = Message(
            subject='Welcome To Mkoani App.',
            recipients=[
                owner.email
            ],
            body='Welcome to your Mkoani account. To login please visit <LOGIN_URL> to activate your account.'
                 'Your password is ' + form.password.data + ' '
        )
        # send email
        mail.send(msg)
        return redirect(url_for('owner'))

    return render_template('owner_registration.html', form=form, title='login')
