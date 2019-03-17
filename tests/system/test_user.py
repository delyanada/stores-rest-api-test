from tests.base_test import BaseTest
from models.user import UserModel
import json


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                response=client.post('/register', data={'username': 'test', 'password': '1234'})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual({'message': 'User created successfully.'},
                                     json.loads(response.data))

    def test_register_and_login(self):     #success
        with self.app() as client:
            with self.app_context():
                # Create a new user
                client.post("/register", data={'username': 'test', 'password': '1234'})

                # Login the new user
                auth_response=client.post('/auth',
                                          data=json.dumps({'username': 'test', 'password': '1234'}),
                                          headers={'Content-Type': 'application/json'})

                self.assertIn('access_token', json.loads(auth_response.data).keys())     #['access_token']it wil be return

    def test_fail_register_and_login(self):   # not success
        with self.app() as client:
            with self.app_context():
                # Login none existing
                auth_response=client.post('/auth',
                                          data=json.dumps({'username': 'test', 'password': 'fake pass'}),
                                          headers={'Content-Type': 'application/json'})

                self.assertEqual(auth_response.status_code, 401)

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post("/register", data={'username': 'test', 'password': '1234'})
                response=client.post("/register", data={'username': 'test', 'password': '1234'})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'A user with that username already exists'},
                                     json.loads(response.data))
