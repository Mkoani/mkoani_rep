from flask import render_template, request, redirect, flash, url_for
from flask_login import current_user, login_required

from app import app
from app import db
from app import models
from app import photos
from app.owner.main import forms


@app.route('/owner')
@login_required
def owner():
    # get all buses for a given owner that are travelling
    # in other words get bus schedules
    schedules = models.Association.query.filter_by(company=current_user.id).all()
    return render_template('owner.html', schedules=schedules)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        photo_name = photos.save(request.files.get('photo'))
        # update filename
        current_user.update_imagelocation(photo_name)
        flash('upload is a success')
        url = photos.url(photo_name)
        return render_template('owner_profile.html')

    return render_template('owner_profile.html')


@app.route('/owner/prices', methods=["GET", "POST"])
@login_required
def set_prices():
    '''this view functions renders a form
    for the user to insert prices and inserts
    the price record into the database
    '''
    form = forms.PriceForm()
    if form.validate_on_submit():
        price = models.Price(bus_type=form.bus_grade.data, route_id=form.route_id.data,
                             amount=form.amount.data, company=current_user.id)
        db.session.add(price)
        db.session.commit()
        flash('success')
        return redirect(url_for('owner'))
    return render_template('set_prices.html', form=form)


@app.route('/owner/addBuses', methods=('GET', 'POST'))
@login_required
def add_buses():
    '''the function renders a form for the user
    to enter some details of the bus and
    then insert the bus details into database
    and also inserts seats for that bus'''
    form = forms.BusForm()
    if form.validate_on_submit():
        # insert bus record into databse
        bus = models.Bus(id=form.bus_id.data, busName=form.bus_name.data,
                         grade=form.grade.data, max_no_seats=form.number_of_seats.data, ownerName=current_user.id)
        db.session.add(bus)
        db.session.commit()
        # insert seats for the bus
        models.add_seats(form.number_of_seats.data, form.bus_id.data)
        flash('success')
        return redirect(url_for('owner'))

    return render_template('add_buses.html', form=form)


@app.route('/owner/addroutes', methods=['GET', 'POST'])
@login_required
def add_routes():
    '''this function adds a route for a company
    '''
    form = forms.RouteForm()
    if form.validate_on_submit():
        route = models.Route(id=form.route_id.data, from_destination=form.from_destination.data,
                             to_destination=form.to_destination.data, bus_company=current_user.id)
        db.session.add(route)
        db.session.commit()
        flash('successful')
        return redirect(url_for('owner'))
    return render_template('routes.html', form=form)


@app.route('/owner/schedules')
@login_required
def show_schedules():
    '''this function pulls all schedules
    from the database for a given bus company
    and displays them
    '''
    schedules = models.Association.query.filter_by(company=current_user.id).all()
    if schedules:
        return render_template('schedules.html', schedules=schedules)
    flash('sorry no available schedules')
    return render_template('schedules.html')


@app.route('/owner/addschedules', methods=('GET', 'POST'))
@login_required
def add_schedules():
    '''this functions inserts new schedules
        into database
    '''
    form = forms.SchedulesForm()
    if form.validate_on_submit():
        schedule = models.Association(Bus_id=form.bus_id.data, Routes_id=form.route_id.data,
                                      departing_date=form.departing_date.data,
                                      arrival_date=form.arrival_date.data,
                                      departing_time=form.departing_time.data,
                                      arriving_time=form.arrival_time.data,
                                      company=current_user.id)
        db.session.add(schedule)
        db.session.commit()
        flash('success')
        return redirect(url_for('show_schedules'))
    return render_template('add_schedules.html', form=form)


@app.route('/owner/customers', methods=['POST', 'GET'])
@login_required
def customers():
    if request.method == 'POST':
        search = request.form.get('search')
        result = models.Customer.query.filter_by(name=search).all()
        if result:
            return render_template('customers.html', result=result)
        flash('sorry no results')
        return redirect(url_for('customers'))
    return render_template('customers.html')
