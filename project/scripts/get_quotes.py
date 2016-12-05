from py_postmates import postmates as pm
import requests
import requests.auth
import json

POSTMATES_CUSTOMER_KEY = "cus_L0meVbIU6KYRIk"
POSTMATES_DEVELOPER_KEY = "ba2f6d3e-149f-41d3-b3c5-b305bd501250"
UBER_KEY = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzY29wZXMiOlsiZGVsaXZlcnkiXSwic3ViIjoiOTkxMjQ1NTQtZjU2OC00MzNkLWI2MDQtYmNmNjIxMmRhMTA3IiwiaXNzIjoidWJlci11czEiLCJqdGkiOiI0YWM5MmJjZi1iMjkzLTQxNmMtYjE3My0yNGNhODZiNjJkOGQiLCJleHAiOjE0ODE0MDczOTIsImlhdCI6MTQ3ODgxNTM5MiwidWFjdCI6IlZ5aFdSZkpYanoxNmVpZjc1QnI0cHR0bVRORGJEZCIsIm5iZiI6MTQ3ODgxNTMwMiwiYXVkIjoidERKTWdNdDJSUnU2dUFhSC1iMTF2eWlTYWdwTEc4SzkifQ.Zsuy35oyiFkvqYZDRO5YyMvrwOTalMa7zQISEO40vMdMxQ7wmC0xhTcGriJbLFIB6Ptzxx0H89axGjR0QxdRnzAB_We2AGyu6CnqIJbo44fbv-ldsa5NShk4VVnb6lPQQKOGSQ0fBJaf6VZOjsbWvhKKHgso2yUs5bKcUw5mXhY4rCcIfPOr9pGYNox_4KG7HrT8g2v31Tc6q1QKy2rd71nwG_t0H758RFdSYEZyV_mxz1bO3dJBNgr1g3RdnW4XZR0_8gYubart3UpeIdn4BnrMQUplQJcD_8YM7FJMGhKd8Zj-VfPN7llFbqC5eQEk7PTxXsZVudHzFtoy3f3lOA"
UBER_CLIENT_ID = "tDJMgMt2RRu6uAaH-b11vyiSagpLG8K9"
UBER_SECRET_ID = "wZH7dx3Tg-H1RBZ0Y9PGh35OLhBoNE3P6_BTcDKh"


def get_quotes(customer_data = None, delivery_data = None):
    if customer_data and delivery_data and customer_data["address"] == delivery_data["address"]:
        return "Please provide different delivery and customer addresses"

    if not customer_data:
        customer_data = get_customer_data()
    if not delivery_data:
        delivery_data = get_delivery_data()

    postmates_quote = get_postmates_quote(customer_data, delivery_data)
    uber_quote = get_uber_quote(customer_data, delivery_data)

    return postmates_quote, uber_quote


def get_postmates_quote(customer_data, delivery_data):
    """ Script to get the quote for a trip from a customer to a delivery destination

    params customer_data: Data about the customer or None if not provided
    params delivery_data: Data about the delivery location or None of if not provided
    return: Quote price and metadata
    """
    pickup_address = ",".join([customer_data["address"], customer_data["city"], customer_data["state"]])
    dropoff_address = ",".join([delivery_data["address"], delivery_data["city"], delivery_data["state"]])
    pickup = pm.Location(customer_data["name"], pickup_address, customer_data["number"])
    dropoff = pm.Location(delivery_data["name"], dropoff_address, delivery_data["number"])

    postmates = pm.PostmatesAPI(POSTMATES_DEVELOPER_KEY, POSTMATES_CUSTOMER_KEY)
    quote = pm.DeliveryQuote(postmates, pickup.address, dropoff.address)
    return quote


def get_uber_quote(customer_data, delivery_data):
    """ Script to get the quote for a trip from a customer to a delivery destination

    params customer_data: Data about the customer or None if not provided
    params delivery_data: Data about the delivery location or None of if not provided
    return: Quote price and metadata
    """

    params = {
        "pickup": {
            "location": {
                "address": customer_data["address"],
                "state": customer_data["state"],
                "country": customer_data["country"],
                "postal_code": customer_data["zip_code"],
                "city": customer_data["city"]
            }
        },
        "dropoff": {
            "location": {
                "address": delivery_data["address"],
                "state": delivery_data["state"],
                "country": delivery_data["country"],
                "postal_code": delivery_data["zip_code"],
                "city": delivery_data["city"]
            }
        }
    }

    URL = "https://sandbox-api.uber.com/v1/deliveries/quote"

    header = {
        'Authorization': "Bearer " + UBER_KEY,
        'content-type': 'application/json'
    }

    r = requests.post(URL, headers=header, data=json.dumps(params))
    quote = json.loads(r.text)
    return quote["quotes"][0]


def get_customer_data():
    """ Ask user for customer data if not provided. Otherwise, create pickup object.

    params customer_data: Data about the customer or None if not provided
    return: pickup object
    """

    customer_data = {}
    customer_data["name"] = raw_input("Please enter your company's name: ")
    customer_data["address"] = raw_input("Please enter the address to pick-up from: ")
    customer_data["number"] = raw_input("Please enter your Phone number (i.e. 123-456-7890): ")
    return customer_data


def get_delivery_data():
    """ Ask user for delivery data if not provided. Otherwise, create delivery object.

    params delivery_data: Data about the delivery or None if not provided
    return: delivery object
    """
    delivery_data = {}
    delivery_data["name"] = raw_input("Please enter the name of the place to deliver to: ")
    delivery_data["address"] = raw_input("Please enter the address to deliver to: ")
    delivery_data["number"] = raw_input("Please enter the Phone number where we should deliver: ")
    return delivery_data


'''if __name__ == '__main__':
    customer_data = {"name": "Customer", "address": "1629 Provincetown Dr.", "city": "San Jose", "state": "CA",
                     "zip_code": "95129", "country": "USA", "number": "408-666-0765"}
    delivery_data = {"name": "Customer", "address": "3041 Stevens Creek Blvd", "city": "Santa Clara", "state": "CA",
                     "zip_code": "95050", "country": "USA", "number": "408-255-5346"}
    postmates_quote, uber_quote = get_quotes(customer_data=customer_data, delivery_data=delivery_data)
    print postmates_quote
    print ""
    print "Uber Delivery Quote --------"
    print "ID: " + uber_quote["quote_id"]
    print "Created At: " + str(datetime.datetime.utcfromtimestamp(uber_quote["estimated_at"]))
    print "Fee: $" + str(uber_quote["fee"]) + " " + uber_quote["currency_code"]
    print "Dropoff ETA: " + str(uber_quote["dropoff_eta"]) + " minutes"
    print "Expires: " + str(datetime.datetime.utcfromtimestamp(uber_quote["expires_at"]))
    print "Expired: False"'''

