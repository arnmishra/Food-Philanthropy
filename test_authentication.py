"""
Used to help write tests: https://pythonhosted.org/Flask-Testing/ and http://damyanon.net/flask-series-testing/
"""

from project import app, db
from project.models import User
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

    def test_home_status_code(self):
        """ Test of home page rendering """
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_empty_db(self):
        """ Test that empty database has no content """
        all_comments = User.query.all()
        self.assertTrue(len(all_comments) == 0)

    def test_creating_user(self):
        """ Test that user are added correctly """
        new_user = User("username", "password", "name", "street_address", "city", "state", "12345",
                        "country", 123)
        db.session.add(new_user)
        db.session.commit()
        self.assertTrue(new_user in db.session)
        all_users = User.query.all()
        self.assertEqual(len(all_users), 1)
        self.assertEqual(all_users[0].username, "username")
        self.assertEqual(all_users[0].password, "password")
        self.assertEqual(all_users[0].name, "name")
        self.assertEqual(all_users[0].street_address, "street_address")
        self.assertEqual(all_users[0].city, "city")
        self.assertEqual(all_users[0].state, "state")
        self.assertEqual(all_users[0].zip_code, 12345)
        self.assertEqual(all_users[0].country, "country")
        self.assertEqual(all_users[0].phone_number, 123)

    def test_sql_injection(self):
        """ Test that SQL style comments don't affect the database """
        new_user = User("username", "Drop DATABASE User", "name", "street_address", "city", "state", "12345",
                        "country", 123)
        db.session.add(new_user)
        db.session.commit()
        self.assertTrue(new_user in db.session)
        all_users = User.query.all()
        self.assertEqual(len(all_users), 1)
        self.assertEqual(all_users[0].username, "username")
        self.assertEqual(all_users[0].password, "Drop DATABASE User")
        self.assertEqual(all_users[0].name, "name")
        self.assertEqual(all_users[0].street_address, "street_address")
        self.assertEqual(all_users[0].city, "city")
        self.assertEqual(all_users[0].state, "state")
        self.assertEqual(all_users[0].zip_code, 12345)
        self.assertEqual(all_users[0].country, "country")
        self.assertEqual(all_users[0].phone_number, 123)

    def test_unauthorized(self):
        """ Test that you can't access a page that requires authentication. """
        result = self.app.get('/show_quotes')
        self.assertEqual(result.status_code, 405)


if __name__ == '__main__':
    unittest.main()
