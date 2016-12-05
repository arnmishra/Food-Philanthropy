""" Tests for the Graph in graph.py

PyCharm Error Code Documented: https://youtrack.jetbrains.com/issue/PY-20171
"""

import unittest

import get_quotes


class TestPostmates(unittest.TestCase):

    def test_basic_quote(self):
        """ Test getting a simple quote. """
        customer_data = {"name": "Customer", "address": "1629 Provincetown Dr. San Jose, CA 95129", "number": "408-666-0765"}
        delivery_data = {"name": "Delivery", "address": "3041 Stevens Creek Blvd, Santa Clara, CA 95050", "number": "408-255-5346"}
        quote = get_quotes.get_quotes(customer_data=customer_data, delivery_data=delivery_data)
        self.assertEqual(quote.fee, 1125)
        self.assertEqual(quote.currency, "usd")
        self.assertEqual(quote.duration, 90)

    def test_no_movement_quote(self):
        """ Test same start and end. """
        customer_data = {"name": "Customer", "address": "1629 Provincetown Dr. San Jose, CA 95129", "number": "408-666-0765"}
        delivery_data = {"name": "Delivery", "address": "1629 Provincetown Dr. San Jose, CA 95129", "number": "408-666-0765"}
        quote = get_quotes.get_quotes(customer_data=customer_data, delivery_data=delivery_data)
        self.assertEqual(quote, "Please provide different delivery and customer addresses")

    def test_invalid_movement(self):
        """ Test an invalid movement to a place that is too far. """
        customer_data = {"name": "Customer", "address": "1629 Provincetown Dr. San Jose, CA 95129", "number": "408-666-0765"}
        delivery_data = {"name": "Delivery", "address": "606 E. White St. UChampaign, IL 61820", "number": "408-666-0765"}
        try:
            get_quotes.get_quotes(customer_data=customer_data, delivery_data=delivery_data)
        except Exception,e:
            self.assertEqual(str(e), "The specified location is not in a deliverable area.")
            return
        self.assertTrue(False)

if __name__ == "__main__":
    unittest.main()
