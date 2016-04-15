from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests


Base = declarative_base()

association_table = Table('association', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('geo_location_id', Integer, ForeignKey('geo_location.id'))
)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)
    city = Column(String)
    location = relationship("Geo_location", secondary=association_table)

    def __init__(self, name, fullname, password, city):
        self.name = name
        self.fullname = fullname
        self.password = password
        self.city = city

    def __iter__(self):
        for key in self.some_sequence:
            yield (key, 'Value for {}'.format(key))


class Geo_location(Base):
    __tablename__ = 'geo_location'
    id = Column(Integer, primary_key=True)
    lat = Column(String)
    lng = Column(String)

    def __init__(self, lat, lng):
        self.lat = lat

        self.lng = lng


engine = create_engine('sqlite:///user.db')

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
Session.configure(bind=engine)

session = Session()

userName = input("What's your name? ")
userFullName = input("What's your Full name? ")
userPassword = input("Enter you password ")

addNewUser = User(userName, userFullName, userPassword, 'none')


userAddress = input("Hello, " + userName + "! " + " Enter your address ")
url = 'https://maps.googleapis.com/maps/api/geocode/json'
params = {'sensor': 'false', 'address': str(userAddress)}
r = requests.get(url, params=params)
results = r.json()['results']
location = results[0]['geometry']['location']

geol = Geo_location(location['lat'], location['lng'])
addNewUser.city = userAddress
addNewUser.location.append(geol)

session.add(addNewUser)
session.commit()
session.close()

