"""
Used to help write tests: https://pythonhosted.org/Flask-Testing/ and http://damyanon.net/flask-series-testing/
"""

from project import app, db
from project.models import Routes
import unittest


class FlaskUserTests(unittest.TestCase):

    def setUp(self):
        """ Used to set up the database and app for each test """
        self.app = app.test_client()
        self.app.testing = True
        db.create_all()

    def tearDown(self):
        """ Used to remove the database for each test """
        db.session.remove()
        db.drop_all()

    def test_empty_db(self):
        """ Test that empty database has no content """
        all_comments = Routes.query.all()
        self.assertTrue(len(all_comments) == 0)

    def test_creating_route(self):
        """ Test that route are added correctly """
        new_route = Routes(1, 123, 321, 456, 654, 1.0, 2.0)
        db.session.add(new_route)
        db.session.commit()
        self.assertTrue(new_route in db.session)
        all_routes = Routes.query.all()
        self.assertEqual(len(all_routes), 1)
        self.assertEqual(all_routes[0].user_id, 1)
        self.assertEqual(all_routes[0].start_longitude, 123.0)
        self.assertEqual(all_routes[0].start_latitude, 321.0)
        self.assertEqual(all_routes[0].end_longitude, 456.0)
        self.assertEqual(all_routes[0].end_latitude, 654.0)
        self.assertEqual(all_routes[0].lowest_price, 1.0)
        self.assertEqual(all_routes[0].highest_price, 2.0)
        self.assertEqual(all_routes[0].num_deliveries, 1)

    def test_sql_injection(self):
        """ Test that SQL style comments can't be inserted because of integer/float constraints """
        try:
            Routes(1, 123, "DROP DATABASE Routes", 456, 654, 1.0, 2.0)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_incrementing_num_deliveries(self):
        """ Test that incrementing the number of deliveries is saved appropriately """
        new_route = Routes(1, 123, 321, 456, 654, 1.0, 2.0)
        db.session.add(new_route)
        db.session.commit()
        self.assertTrue(new_route in db.session)
        all_routes = Routes.query.all()
        self.assertEqual(len(all_routes), 1)
        self.assertEqual(all_routes[0].num_deliveries, 1)
        all_routes[0].num_deliveries += 1
        db.session.commit()
        all_routes = Routes.query.all()
        self.assertEqual(len(all_routes), 1)
        self.assertEqual(all_routes[0].num_deliveries, 2)


if __name__ == '__main__':
    unittest.main()
