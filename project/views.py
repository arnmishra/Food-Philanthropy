from geopy.geocoders import Nominatim
from parse import *
import datetime
import googlemaps
from flask import render_template, request, jsonify, redirect
from flask.ext.login import login_user, logout_user, login_required, current_user
from flask_googlemaps import Map
from project import app, db, GOOGLEMAPS_KEY
from project.scripts.get_quotes import get_quotes
from models import User, Routes
from flask.ext.login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
marker_addresses = {}
app.secret_key = 'secret'


@login_manager.user_loader
def load_user(id):
    """ Login Page

    :param id: of user
    :return: User being queried for
    """
    return User.query.get(int(id))


@app.route("/")
def index():
    """ Renders Home page

    :return: index.html
    """
    all_users = User.query.all()
    num_users = len(all_users)
    num_destinations = 0
    num_deliveries = 0
    states = []
    for user in all_users:
        states.append(user.state)
        all_destinations = Routes.query.filter_by(user_id=user.id).all()
        num_destinations += len(all_destinations)
        for destination in all_destinations:
            num_deliveries += destination.num_deliveries
    num_states = len(set(states))
    return render_template("index.html", num_users=num_users, num_destinations=num_destinations,
                           num_deliveries=num_deliveries, num_states=num_states)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """ Login Page for account. Checks Username/Password Combo

    :return: to order page after authentication
    """
    if request.method == "GET":
        return render_template("login.html")
    username = request.form["username"]
    password = request.form["password"]
    user = User.query.filter_by(username=username, password=password).first()
    if not user:
        return render_template("login.html", error="Incorrect Username/Password")
    login_user(user)
    return redirect("/order")


@app.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    """ Sign Up for an account

    :return: to order page after authentication
    """
    if request.method == "GET":
        return render_template("sign_up.html")
    username = request.form["username"]
    password = request.form["password"]
    name = request.form["name"]
    street_address = request.form["street_address"]
    city = request.form["city"]
    state = request.form["state"]
    country = request.form["country"]
    try:
        zip_code = int(request.form["zip_code"])
    except:
        return render_template("sign_up.html", error="Zip Code must be Integer")
    try:
        phone_number = int(request.form["number"])
    except:
        return render_template("sign_up.html", error="Phone Number must be Integer")
    if len(str(phone_number)) != 10:
        return render_template("sign_up.html", error="Phone Number must be 10 Digits (include area code)")
    latitude, longitude = get_coordinates_from_address(street_address, city, state, country)
    new_user = User(username, password, name, street_address, city, state, zip_code, country, phone_number,
                    latitude, longitude)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    return redirect("/order")


@app.route('/logout')
def logout():
    """ Log out of system
    https://blog.openshift.com/use-flask-login-to-add-user-authentication-to-your-python-application/

    :return: return to home page
    """
    logout_user()
    return redirect("/")


@app.route("/order")
@login_required
def order():
    """ Home page with Google Maps. Use Google Maps Places API to find nearby Food Pantries
    and Google Maps Flask API to render the map with proper red markers for pantries and
    blue marker for current location.

    :return: order.html
    """
    locations = get_nearby_pantries()
    markers = get_markers(locations)
    main_map = set_main_map(markers)
    return render_template('order.html', map=main_map)


def set_main_map(markers):
    """ Set up the primary Google Map on the home page with donation options

    :param markers: the food pantries to donate too
    :return: map object
    """
    main_map = Map(
        style=(
            "height:70%;"
            "width:70%;"
        ),
        identifier="current_map",
        lat=current_user.latitude,
        lng=current_user.longitude,
        markers=markers
    )
    return main_map


def get_markers(locations):
    """ Get the food pantry options in proper format

    :param locations: information about the food pantries
    :return: formatted marker locations
    """
    markers = []
    for result in locations["results"]:
        latitude = result["geometry"]["location"]["lat"]
        longitude = result["geometry"]["location"]["lng"]
        address = result["formatted_address"]
        address_data = {}
        address_data["street"], address_data["city"], address_data["state"], address_data["zip_code"], \
        address_data["country"] = parse("{}, {}, {} {}, {}", address)
        marker_addresses[result["name"]] = address_data
        markers.append(
            {'lat': latitude,
             'lng': longitude,
             'infobox': "<h2>" + result["name"] + "</h2><p>" + address + "</p>"}
        )
    markers.append(
        {'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
         'lat': current_user.latitude,
         'lng': current_user.longitude,
         'infobox': "Current Location"}
    )
    return markers


def get_nearby_pantries():
    """ Calls Google Maps Places API to get current locations of nearby pantries.

    :return: Locations of the food pantries
    """
    maps_client = googlemaps.Client(GOOGLEMAPS_KEY)
    locations = maps_client.places("food pantry", location=[current_user.latitude, current_user.longitude])
    return locations


@app.route("/past_orders", methods=['GET'])
@login_required
def show_orders():
    """ Redirect to show all past orders made by a user and their metadata

    :return: past_orders.html
    """
    all_routes = Routes.query.filter_by(user_id=current_user.id).all()
    name = current_user.name
    start_address = get_address_from_coordinates(current_user.latitude, current_user.longitude)
    all_markers = []
    all_paths = []
    for route in all_routes:
        end_address = get_address_from_coordinates(route.end_latitude, route.end_longitude)
        destination_data = "<h2>Route Used " + str(route.num_deliveries) + " Time(s)</h2><p>Pricing Ranges From $" + \
                           str(route.lowest_price) + " - $" + str(route.highest_price) + "</p>"
        markers, path = set_route_map(start_address, name, end_address, destination_data)
        all_markers.append(markers[1])
        all_paths.append(path)
    all_markers.append(
        {'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
         'lat': current_user.latitude,
         'lng': current_user.longitude,
         'infobox': "Start Location"}
    )
    map = Map(
        style=(
            "height:70%;"
            "width:70%;"
        ),
        identifier="plinemap",
        varname="plinemap",
        lat=current_user.latitude,
        lng=current_user.longitude,
        polylines=all_paths,
        markers=all_markers
    )
    return render_template('past_orders.html', map=map)


@app.route("/show_quotes", methods=['POST'])
@login_required
def show_quotes():
    """ Renders the page with quotes and a map of the route for a given donation.

    :return: quotes.html
    """
    customer_data, delivery_data = get_delivery_route_data(request)
    postmates_quote, uber_quote = get_quotes(customer_data, delivery_data)
    uber_quote["estimated_at"] = str(datetime.datetime.utcfromtimestamp(uber_quote["estimated_at"]))
    uber_quote["expires_at"] = str(datetime.datetime.utcfromtimestamp(uber_quote["expires_at"]))
    start_address = "%s, %s, %s" % (customer_data["address"], customer_data["city"], customer_data["state"])
    end_address = "%s, %s, %s" % (delivery_data["address"], delivery_data["city"], delivery_data["state"])
    markers, path = set_route_map(start_address, customer_data["name"], end_address, delivery_data["name"])
    map = Map(
        style=(
            "height:70%;"
            "width:70%;"
        ),
        identifier="plinemap",
        varname="plinemap",
        lat=current_user.latitude,
        lng=current_user.longitude,
        polylines=[path],
        markers=markers
    )
    add_route_to_database(customer_data, delivery_data, postmates_quote.fee/100.0, uber_quote["fee"])
    return render_template('quotes.html', postmates_quote=postmates_quote, uber_quote=uber_quote, map=map)


def add_route_to_database(customer_data, delivery_data, postmates_price, uber_price):
    """ Add a new route to the database or update an existing route in the database

    :param customer_data: Data about the origin
    :param delivery_data: Data about the delivery destination
    :param postmates_price: Price Quote from Postmates
    :param uber_price: Price Quote from Uber
    """
    start_latitude, start_longitude = get_coordinates_from_address(customer_data["address"], customer_data["city"],
                                                                   customer_data["state"], customer_data["zip_code"])
    end_latitude, end_longitude = get_coordinates_from_address(delivery_data["address"], delivery_data["city"],
                                                               delivery_data["state"], delivery_data["zip_code"])
    route = Routes.query.filter_by(start_longitude=start_longitude, start_latitude=start_latitude,
                                   end_longitude=end_longitude, end_latitude=end_latitude).first()
    if postmates_price <= uber_price:
        lowest_price = postmates_price
        highest_price = uber_price
    else:
        lowest_price = uber_price
        highest_price = postmates_price
    if route:
        route.num_deliveries += 1
        if route.highest_price < highest_price:
            route.highest_price = highest_price
        if route.lowest_price > lowest_price:
            route.lowest_price = lowest_price
        db.session.commit()
    else:
        new_route = Routes(current_user.id, start_longitude, start_latitude, end_longitude, end_latitude, lowest_price,
                           highest_price)
        db.session.add(new_route)
        db.session.commit()


def set_route_map(start_address, start_label, end_address, end_label):
    """ Get all the details for a route between two coordinates

    :param start_address: Address of start of route
    :param start_label: Name of start of route
    :param end_address: Address of end of route
    :param end_label: Name of end of route
    :return: Markers (the latitudes/longitudes of the trip) and Path (the pieces of the path)
    """
    maps_client = googlemaps.Client(GOOGLEMAPS_KEY)
    directions_result = maps_client.directions(start_address, end_address)
    path = []
    steps = directions_result[0]["legs"][0]["steps"]
    for i in range(len(steps)):
        path.append((steps[i]["start_location"]["lat"], steps[i]["start_location"]["lng"]))
    path.append((steps[i]["end_location"]["lat"], steps[i]["end_location"]["lng"]))
    markers = []
    markers.append(
        {'lat': current_user.latitude,
         'lng': current_user.longitude,
         'infobox': start_label}
    )
    markers.append(
        {'lat': steps[i]["end_location"]["lat"],
         'lng': steps[i]["end_location"]["lng"],
         'infobox': end_label}
    )
    return markers, path


def get_delivery_route_data(request):
    """ Get data about the delivery route from the form.

    :param request: The form submission.
    :return: data about the customer and delivery location
    """
    customer_data = {}
    customer_data["name"] = request.form["start"]
    customer_data["address"] = request.form["start_street"]
    customer_data["city"] = request.form["start_city"]
    customer_data["zip_code"] = request.form["start_zip_code"]
    customer_data["state"] = request.form["start_state"]
    customer_data["country"] = request.form["start_country"]
    customer_data["number"] = request.form["start_number"]
    delivery_data = {}
    delivery_data["name"] = request.form["destination"]
    delivery_data["address"] = request.form["destination_street"]
    delivery_data["city"] = request.form["destination_city"]
    delivery_data["zip_code"] = request.form["destination_zip_code"]
    delivery_data["state"] = request.form["destination_state"]
    delivery_data["country"] = request.form["destination_country"]
    delivery_data["number"] = request.form["destination_number"]
    return customer_data, delivery_data


def get_coordinates_from_address(street_address, city, state, country):
    """ Get the coordinates of a given address

    :param street_address: Street address
    :param city: City of address
    :param state: State of address
    :param country: Country of address
    :return: Latitude and Longitude
    """
    geolocator = Nominatim()
    location = geolocator.geocode("%s %s %s %s" % (street_address, city, state, country))
    return location.latitude, location.longitude


def get_address_from_coordinates(latitude, longitude):
    """ Get a street address from coordinates

    :param latitude: Starting latitude
    :param longitude: Starting longitude
    :return:
    """
    geolocator = Nominatim()
    location = geolocator.reverse("%.2f, %.2f" % (float(latitude), float(longitude)))
    return location.address


@app.route("/get_data", methods=['POST'])
@login_required
def get_data():
    """ Handles asynchronous request to get information about a food pantry on the front-end form

    :return: Data about the food pantry
    """
    destination = request.form['destination']
    return jsonify(marker_addresses[destination])

if __name__ == "__main__":
    app.run(debug=True)
