from flask_mail import Message

from app import app, mail
from app import db
from flask import render_template, redirect, url_for, session, flash
from app.customer.forms import *
from app.models import Route, Price, Bus, Seat, Customer, Association, show_buses
from datetime import datetime
from app.customer.generate_uuid import generate_uuid


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = RouteForm()
    # proceed when the validators on form dont raise error
    if form.validate_on_submit():

        # get choosen routes from user
        routes = Route.query.filter(Route.from_destination == form.from_destination.data,
                                    Route.to_destination == form.to_destination.data).all()
        if not routes:
            flash('sorry we do not have such route at the moment')
            return redirect(url_for('index'))

        # get buses for given routes
        buses = show_buses(routes, form.grade.data, form.date_departure.data)

        # if no buses for available route
        if not buses:
            flash('sorry there are no buses travelling this route on this date at the moment')
            return redirect(url_for('index'))

        # if buses are available for that route
        return render_template('index.html', form=form, buses=buses, title='Our Buses')
    return render_template('index.html', form=form, title='Home')


#
# display seats for a given bus
#
@app.route('/bus/<schedule>', methods=['GET', 'POST'])
def bus(schedule):
    schedule = schedule.split()  # schedule here is a list of two items the bus id
    # and route id respectively

    # store the schedule in the session
    session['schedule'] = schedule
    # obtain the bus
    bus = Bus.query.get(schedule[0])
    # obtain paid seats for the bus
    paid_seats = bus.paid_seats()
    # obtain available seats but which are hold
    available_seats_with_hold = bus.get_available_seats_with_hold()

    form = SeatsForm()
    # obtain available seats and
    # assign seats to choices for seat_id in form
    seats = [(seat.id, seat.id) for seat in bus.get_available_seats()]
    form.seat.choices = seats

    if form.validate_on_submit():
        # get chosen seat(s) from user
        chosen_seat = form.seat.data
        # store seats for user
        session['seats'] = chosen_seat
        # then update hold column for every seat
        for seats in chosen_seat:
            seat = Seat.query.get(seats)
            seat.update_hold('yes')
        # end of update#
        return redirect(url_for('pay'))

    return render_template('bus.html', form=form, seats=paid_seats, title='Bus seats', held=available_seats_with_hold)


#
# show the ticket details user has chosen
# ask user to pay
# ask for user details
#
@app.route('/payment', methods=['GET', 'POST'])
def pay():
    form = CustomerForm()
    cancel = Cancel()
    # get seat(s) chosen by customer
    seat_no = session['seats']
    print(seat_no)
    # get chosen route from session
    #
    route_id = session['schedule'][1]
    route = Route.query.get(route_id)

    # obtain schedule for that route and bus
    schedule = Association.query.filter_by(Bus_id=session['schedule'][0], Routes_id=session['schedule'][1]).first()
    print(schedule)

    # show ticket details to user
    form.from_destination.data = route.from_destination
    form.to_destination.data = route.to_destination
    form.leaving_date.data = schedule.departing_date
    form.arrival_date.data = schedule.arrival_date
    form.leaving_time.data = schedule.departing_time
    form.arriving_time.data = schedule.arriving_time
    # show total amount
    # all seat belong to same bus
    # get bus name
    bus_name = schedule.bus.busName
    # get price
    price = schedule.show_price
    # calculate total amount
    amount = price * len(seat_no)

    #
    # user wants to pay
    # integration with tigo secure implemented here
    # for now just store customer details
    # update seat hold and timebooked and status
    # email and text customer ticket details
    if form.validate_on_submit():
        # store customer details
        # generate uniqueid for customer
        id = generate_uuid()
        customer = Customer(id=id, name=form.name.data, phoneNo=form.phoneno.data, email=form.email.data)
        db.session.add(customer)
        db.session.commit()
        # assign seats to this customer
        # perform seat update
        for seats in seat_no:
            seat = Seat.query.get(seats)
            seat.update_status('taken')
            seat.update_hold('yes')
            seat.update_time()
            seat.assign_seats_customer(id)
            db.session.commit()
        # end update

        # send email to customer
        if form.email.data is not None:
            msg = Message(subject='Mkoani App Booking Successful',
                          sender='booking@mkoani.com',
                          recipients=[form.email.data],
                          body='Congratulations. You have successfully booked your trip from %s to %s.' % (
                              form.from_destination.data, form.to_destination.data)
                          )
            mail.send(msg)
        return redirect(url_for('index'))
    return render_template('pay.html', form=form, seat=seat_no, title='Payment', amount=amount, cancel=cancel,
                           name=bus_name)


#
# update seats when the user cancels payment
@app.route('/payment/cancel', methods=['POST'])
def cancel():
    # get seats
    # use session
    seats = session['seats']
    # update seats to show holding is no
    for seats in seats:
        seat = Seat.query.get(seats)
        seat.update_hold('no')
    # end of updates
    # delete session for user
    session.pop('schedule', None)
    session.pop('seats', None)
    print(session)
    # end
    return redirect(url_for('index'))


@app.route('/base')
def base():
    return render_template('base.html')
