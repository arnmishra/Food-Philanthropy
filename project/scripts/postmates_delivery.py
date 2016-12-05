from py_postmates import postmates as pm

POSTMATES_CUSTOMER_KEY = "cus_L0meVbIU6KYRIk"
POSTMATES_DEVELOPER_KEY = "ba2f6d3e-149f-41d3-b3c5-b305bd501250"


def main():
    postmates = pm.PostmatesAPI(POSTMATES_DEVELOPER_KEY, POSTMATES_CUSTOMER_KEY)

    delivery = order(postmates)

    interact = True

    while interact:

        command = raw_input("Status, Cancel, Done: ")

        if command == "Status": # Check what button the user presses.
            print get_status(delivery)

        elif command == "Cancel":
            if delivery.status != "pending":
                delivery.cancel()
            else:
                print "Can only cancel deliveries not yet picked up."
                print "The current status is: " + get_status(delivery)
            interact = False

        elif command == "Done":
            interact = False

        else:
            print "Please enter a valid option."


def get_status(delivery):
    if delivery.status == "pending":
        return "Processing the request."
    elif delivery.status == "pickup":
        return "Picked up the food."
    elif delivery.status == "dropoff":
        return "Dropped off the food."
    elif delivery.status == "delivered":
        return "Delivery is complete."


def order(postmates):
    # TODO: Take all this info from Google Maps API
    customer_name = raw_input("Please enter your company's name: ")
    customer_address = raw_input("Please enter the address to pick-up from: ")
    customer_number = raw_input("Please enter your Phone number (i.e. 123-456-7890): ")
    manifest = raw_input("Please enter what you will be delivering (i.e. 50 bagels): ")

    delivery_name = raw_input("Please enter the name of the place to deliver to: ")
    delivery_address = raw_input("Please enter the address to deliver to: ")
    delivery_number = raw_input("Please enter the Phone number where we should deliver: ")

    pickup = pm.Location(customer_name, customer_address, customer_number)
    dropoff = pm.Location(delivery_name, delivery_address, delivery_number)
    delivery = pm.Delivery(postmates, manifest, pickup, dropoff)

    delivery.create()

    return delivery

if __name__ == '__main__':
    main()
