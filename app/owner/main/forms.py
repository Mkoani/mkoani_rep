from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField,DateField
from wtforms.validators import DataRequired,ValidationError
from wtforms_components import TimeField
from app.customer import forms
from app import db, models


class PriceForm(FlaskForm):
	bus_grade=StringField('bus grade',validators=[DataRequired()])
	route_id=StringField('route ID',validators=[DataRequired()])
	amount=IntegerField('amount',validators=[DataRequired()])
	set_price=SubmitField('set price')



class BusForm(FlaskForm):
	bus_id=StringField('bus id',validators=[DataRequired()])
	bus_name=StringField('bus name',validators=[DataRequired()])
	grade=StringField('grade',validators=[DataRequired()])
	number_of_seats=IntegerField('maximum seats',validators=[DataRequired()])
	submit=SubmitField('submit')


class RouteForm(forms.RouteForm):
	route_id=StringField('route id',validators=[DataRequired()])
	grade=None
	date_departure=None
	add=SubmitField('add')

class SchedulesForm(FlaskForm):
	route_id=StringField('route id',validators=[DataRequired()])
	bus_id=StringField('bus id',validators=[DataRequired()])
	departing_date=DateField('departing date',validators=[DataRequired()])
	arrival_date=DateField('arrival date',validators=[DataRequired()])
	departing_time=TimeField('departing time',validators=[DataRequired()])
	arrival_time=TimeField('arrival time',validators=[DataRequired()])
	submit=SubmitField('submit')

	#the follwing methods check whether
	#the bus id and route id exist
	#in the database and if not ask user
	#to try again

	def validate_route_id(self,route_id):
		route=models.Route.query.filter_by(id=route_id.data)
		if not db.session.query(route.exists()).scalar():
			raise ValidationError('route does not exist')

	def validate_bus_id(self,bus_id):
		bus=models.Bus.query.filter_by(id=bus_id.data)
		if not db.session.query(bus.exists()).scalar():
			raise ValidationError('bus does not exist')
