from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import Owner


class Login(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember me')
    submit = SubmitField('Login')

    # verify username
    def validate_username(self, username):
        owner = Owner.query.get(username.data)
        # check if owner do not exist
        if owner is None:
            raise ValidationError('username already exists')


class Registration(FlaskForm):
    user = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    # validate_password = StringField('repeat password', validators=[DataRequired(), EqualTo(password)])
    contact = StringField('phone number', validators=[DataRequired()])
    email = StringField('email', validators=[Email()])
    submit = SubmitField('sign up')
    image = StringField('image', validators=[DataRequired()])

    # verify username
    def validate_username(self, username):
        owner = Owner.query.get(username.data)
        # check if owner do exist
        if owner is not None:
            raise ValidationError('username already taken')

    def validate_email(self, email):
        owner = Owner.query.get(email.data)
        if owner is not None:
            raise ValidationError('User wit the email already exists')
