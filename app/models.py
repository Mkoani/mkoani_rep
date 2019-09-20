from datetime import datetime
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from app import db
from app import app
from app import photos


def show_buses(routes, grade, date):
    '''this function returns a list of schedules of buses of a particular grade
    belonging to a list of routes for a given date or none if they do not exist
    '''
    return [schedule for schedule in Association.query.filter_by(departing_date=date).all()
            if schedule.route in routes and schedule.bus.grade == grade]


def add_seats(total_seats=0, bus_id=None):
    '''inserts multiple seats for a bus into database
    the seat id is a composite of the bus_id and some integers
    '''
    for number in range(total_seats):
        seat = Seat(id=bus_id + '/' + str(number), bus_id=bus_id, status='available', holding='no')
        db.session.add(seat)
        db.session.commit()


class Association(db.Model):
    __tablename__ = 'schedules'
    Bus_id = db.Column(db.String, db.ForeignKey('buses.id'), primary_key=True)
    Routes_id = db.Column(db.String, db.ForeignKey('routes.id'), primary_key=True)
    departing_date = db.Column(db.Date)
    arrival_date = db.Column(db.Date)
    departing_time = db.Column(db.Time)
    arriving_time = db.Column(db.Time)
    company = db.Column(db.String)

    def __repr__(self):
        return '{0} {1}'.format(self.Bus_id, self.Routes_id)

    @property
    def show_price(self):
        '''This function returns price for a bus of a certain grade travelling
        through a particular route
        '''
        return Price.query.filter(Price.bus_type == self.bus.grade, Price.route_id == self.Routes_id).first().amount


class Route(db.Model):
    __tablename__ = 'routes'
    from_destination = db.Column(db.String)
    to_destination = db.Column(db.String)
    bus_company = db.Column(db.String)
    id = db.Column(db.String, primary_key=True)
    # get a list of all schedules for particular route
    rschedules = db.relationship(
        'Association', backref='route', lazy='dynamic'
    )

    def __repr__(self):
        return '<Route {}>'.format(self.id)


class Bus(db.Model):
    __tablename__ = 'buses'
    id = db.Column(db.String, primary_key=True)
    ownerName = db.Column(db.String, db.ForeignKey('owners.id'))
    busName = db.Column(db.String)
    grade = db.Column(db.String)
    max_no_seats = db.Column(db.Integer)
    bschedules = db.relationship('Association', backref='bus', lazy='dynamic')
    seats = db.relationship('Seat', backref='bus', lazy='dynamic')  # setting one to many relationship

    def __repr__(self):
        return '<Bus {}>'.format(self.busName)

    #
    # show number of available seats for a bus
    def available_seats(self, grade=None):
        seat = self.seats.filter(Seat.status == 'available').count()
        max_no_seats = self.max_no_seats
        number_seats = int((seat / max_no_seats) * 100)
        return number_seats

    # get paid seats
    def paid_seats(self):
        return self.seats.filter(Seat.status == 'taken').all()

    # get available seats with no hold
    def get_available_seats(self):
        return self.seats.filter(Seat.status == 'available', Seat.holding == 'no').all()

    # get available seats with hold
    def get_available_seats_with_hold(self):
        return self.seats.filter(Seat.status == 'available', Seat.holding == 'yes').all()


class Owner(db.Model, UserMixin):
    __tablename__ = 'owners'
    id = db.Column(db.String, primary_key=True)
    password_hash = db.Column(db.String)
    image_location = db.Column(db.String)
    phone_number = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, default='optional')
    # get buses for particular owner
    buses = db.relationship('Bus', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<Owner {}>'.format(self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update_imagelocation(self, filename):
        self.image_location = filename
        db.session.commit()

    def display_image(self):
        '''the method returns an image url from a given filename
            in the database
        '''
        name = self.image_location
        image_url = photos.url(name)
        if not image_url:
            raise ValueError('can not have empty filename')
        return image_url


# @login.user_loader
# def load_user(user_id):
#   owner=Owner.query.get(user_id)
#  return owner

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.String, primary_key=True, )
    phoneNo = db.Column(db.String)
    email = db.Column(db.String)
    name = db.Column(db.String)
    # get seats booked by the customer
    seats = db.relationship('Seat', backref='customer', lazy='dynamic')

    def __repr__(self):
        return '<Customer {}>'.format(self.name)


class Seat(db.Model):
    __tablename__ = 'seats'
    id = db.Column(db.String, primary_key=True)
    status = db.Column(db.String)
    bus_id = db.Column(db.String, db.ForeignKey('buses.id'))
    time_booked = db.Column(db.DateTime)
    holding = db.Column(db.String)
    customer_id = db.Column(db.String, db.ForeignKey('customers.id'))

    def __repr__(self):
        return '<Seat {}>'.format(self.id)

    # assign seat to customer
    def assign_seats_customer(self, id):
        # obtain customer_id
        customer = Customer.query.get(id)
        self.customer_id = customer.id

    # update status and time booked and hold
    def update_status(self, status):
        self.status = status
        db.session.commit()

    def update_time(self):
        self.time_booked = datetime.now()
        db.session.commit()

    def update_hold(self, hold):
        self.holding = hold
        db.session.commit()


"""holding attribute helps to know users who have selected seat(s) and yet
to complete transaction. it will help avoid another user selecting the same seat
or in other words displaying that a given seat is available while its already
selected by another. however if a user doesnt make payment hold becomes no or if user just leaves website hold is
no after timer """


class Price(db.Model):
    __tablename__ = 'price'
    id = db.Column(db.Integer, primary_key=True)
    bus_type = db.Column(db.String)
    route_id = db.Column(db.String)
    amount = db.Column(db.Float)
    company = db.Column(db.String)

    def __repr__(self):
        return '<Price {}>'.format(self.id)
