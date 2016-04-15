from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests
import random
from SQL import User, Geo_location
from sqlalchemy.ext.declarative import declarative_base
from SQL import association_table
from json import dumps
from sqlalchemy.orm import class_mapper
from sqlalchemy.ext.serializer import loads, dumps
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import func
from flask import render_template,redirect
from flask import jsonify
import json

arrayWithIdUser = []
dictUser = []


def rewrite(user, city, session):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {'sensor': 'false', 'address': str(city)}
    r = requests.get(url, params=params)
    results = r.json()['results']
    location = results[0]['geometry']['location']

    session.query(User).filter(User.id == user.id).\
        update({User.city: city}, synchronize_session=False)
    my_geoloc = session.query(Geo_location).filter(Geo_location.lat == location['lat'],
                                                   Geo_location.lng == location['lng']).first()
    global arrayWithIdUser
    arrayWithIdUser.append(user.id)
    stmt = association_table.update().where(association_table.c.user_id == user.id).values(geo_location_id=my_geoloc.id)
    session.execute(stmt)
    session.commit()


def asdict(obj):
    return dict((col.name, getattr(obj, col.name))
                for col in class_mapper(obj.__class__).mapped_table.c)

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/get_users_location')
def get_users_location():

    global arrayWithIdUser
    global dictUser

    arrayWithIdUser.clear()
    dictUser.clear()

    Base = declarative_base()

    engine = create_engine('sqlite:///user.db')

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)

    session = Session()
    citys = ['London', 'Moscow', 'Barysaw', 'Slutsk', 'Zaslawye', 'Zhodzina', 'Stowbtsy', 'Salihorsk', 'Byerazino']

    recount = 5
    temp = ""
    while recount > 0:
        randUser = random.randrange(0, session.query(User).count())
        randCity = random.randrange(0,len(citys) - 1)
        temp = temp + " " + str(randUser) + "| " + citys[randCity]
        rewrite(session.query(User)[randUser - 1], citys[randCity], session)
        recount -= 1
    session.close()
    return redirect("http://127.0.0.1:5000/results/", code="302")


@app.route('/results/')
def results():
    Base = declarative_base()

    engine = create_engine('sqlite:///user.db')

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)

    session = Session()

    global arrayWithIdUser
    global dictUser

    for item in arrayWithIdUser:
        for u in session.query(User).filter(User.id == item):
            dictUser.append(asdict(u))
    session.close()

    return json.dumps(dictUser)

if __name__ == '__main__':
    app.run()
