from project import db


class User(db.Model):
    """ User Model with all data about a specific user. """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    name = db.Column(db.String)
    street_address = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip_code = db.Column(db.Integer)
    country = db.Column(db.String)
    phone_number = db.Column(db.Integer)
    latitude = db.Column(db.String)
    longitude = db.Column(db.String)

    def __init__(self, username, password, name, street_address, city, state, zip_code, country, phone_number,
                 latitude, longitude):
        self.username = username
        self.password = password
        self.name = name
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country = country
        self.phone_number = phone_number
        self.latitude = latitude
        self.longitude = longitude

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return "<User(username='%s', name='%s', street_address='%s', phone_number='%i')>" \
               % (self.username, self.name, self.street_address, self.phone_number)


class Routes(db.Model):
    """ Routes model to be used for tracking user route data. """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    start_longitude = db.Column(db.Float)
    start_latitude = db.Column(db.Float)
    end_longitude = db.Column(db.Float)
    end_latitude = db.Column(db.Float)
    lowest_price = db.Column(db.Float)
    highest_price = db.Column(db.Float)
    num_deliveries = db.Column(db.Integer)

    def __init__(self, user_id, start_longitude, start_latitude, end_longitude, end_latitude, lowest_price,
                 highest_price):
        self.user_id = user_id
        self.start_longitude = start_longitude
        self.start_latitude = start_latitude
        self.end_longitude = end_longitude
        self.end_latitude = end_latitude
        self.lowest_price = lowest_price
        self.highest_price = highest_price
        self.num_deliveries = 1

    def __repr__(self):
        return "<Routes(user_id='%i', start_longitude='%f', start_latitude='%f', " \
               "end_longitude='%f', end_latitude='%f'>" \
                % (self.user_id, self.start_longitude, self.start_latitude, self.end_longitude, self.end_latitude)
