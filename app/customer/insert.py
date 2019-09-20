from app.models import *
from app import db
from datetime import date
from datetime import time


def insert(rows, col):
    d = {}
    tables = {'route': ['fdest', 'tdest', 'cmpny', 'route_id'], 'owner': ['owname'],
              'bus': ['bus_id', 'grade', 'busName', 'max_seats'],
              'schedule': ['bus_id', 'route_id', 'departing_date', 'arrival_date', 'departing_time', 'arrival_time'],
              'seat': ['seat_no', 'status', 'holding'], 'price': ['route_id', 'grade', 'amount', 'cmpny']}
    for row in range(rows):
        for co in tables[col]:
            d[co] = input('enter' + co + ':')
        if col == 'route':
            route = Route(from_destination=d['fdest'], to_destination=d['tdest'],
                          id=d['route_id'], bus_company=d['cmpny'])
            db.session.add(route)
            db.session.commit()
        if col == 'owner':
            owner = Owner(name=d['owname'])
            db.session.add(owner)
            db.session.commit()
        if col == 'bus':
            bus = Bus(id=d['bus_id'], busName=d['busName'], ownerName=d['owname'], grade=d['grade'],
                      max_no_seats=int(d['max_seats']))
            db.session.add(bus)
            db.session.commit()
        if col == 'schedule':
            schedule = Association(Bus_id=d['bus_id'], Routes_id=d['route_id'],
                                   departing_date=date.fromisoformat(d['departing_date']),
                                   arrival_date=date.fromisoformat(d['arrival_date']),
                                   departing_time=time.fromisoformat(d['departing_time']),
                                   arriving_time=time.fromisoformat(d['arriving_time']))
            db.session.add(schedule)
            db.session.commit()
        if col == 'seat':
            seat = Seat(id=d['seat_no'], status=d['status'], bus_id=d['bus_id'], holding=d['holding'])
            db.session.add(seat)
            db.session.commit()
        if col == 'price':
            price = Price(bus_type=d['grade'], route_id=d['route_id'], amount=int(d['amount']), company=d['cmpny'])
            db.session.add(price)
            db.session.commit()
