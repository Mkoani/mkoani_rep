from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, IntegerField, SubmitField, SelectMultipleField, DateTimeField
from wtforms_components import TimeField
from wtforms.validators import DataRequired, ValidationError, Email
from app.customer.regions import region


class RouteForm(FlaskForm):
    from_destination = SelectField('From', validators=[DataRequired()], choices=region())
    to_destination = SelectField('To', validators=[DataRequired()], choices=region())
    date_departure = DateField('Date')
    grade = SelectField('Grade', validators=[DataRequired()],
                        choices=[('luxury', 'luxury'), ('semi luxury', 'semi luxury'), ('economy', 'economy')])
    submit = SubmitField('Choose route')

    def validate_from_destination(self, from_destination):
        if from_destination.data == self.to_destination.data:
            raise ValidationError('you should choose a different location')


class SeatsForm(FlaskForm):
    seat = SelectMultipleField('Seat number', validators=[DataRequired()])
    choose_seat = SubmitField('Choose seat')


class CustomerForm(FlaskForm):
    name = StringField('Name of passenger', validators=[DataRequired()])
    from_destination = StringField('From', validators=[DataRequired()])
    to_destination = StringField('To', validators=[DataRequired()])
    leaving_date = DateField('departure date', validators=[DataRequired()])
    arrival_date = DateField('arrival date', validators=[DataRequired()])
    leaving_time = TimeField('leaving time', validators=[DataRequired()])
    arriving_time = TimeField('arriving time')
    phoneno = StringField('Phone number', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    pay = SubmitField('pay')


class Cancel(FlaskForm):
    cancel = SubmitField('cancel')
