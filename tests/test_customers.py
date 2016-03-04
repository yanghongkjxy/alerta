import json
import unittest

from alerta.app import app, db


class AuthTestCase(unittest.TestCase):

    def setUp(self):

        self.ADMIN_USER = 'admin@alerta.io'

        app.config['TESTING'] = True
        app.config['AUTH_REQUIRED'] = True
        app.config['CUSTOMER_VIEWS'] = True
        app.config['ADMIN_USERS'] = [self.ADMIN_USER]
        self.app = app.test_client()

        self.api_key = db.create_key(user=self.ADMIN_USER, type='read-write', text='admin API key')

        self.headers = {
            'Authorization': 'Key %s' % self.api_key,
            'Content-type': 'application/json'
        }

        self.major_alert = {
            'event': 'node_marginal',
            'resource': self.resource,
            'environment': 'Production',
            'service': ['Network'],
            'severity': 'major',
            'correlate': ['node_down', 'node_marginal', 'node_up']
        }

    def tearDown(self):

        pass

    def test_customer(self):

        payload = {
            'name': 'Admin User',
            'login': self.ADMIN_USER,
            'password': '8lert8',
            'provider': 'basic',
            'text': 'admin user'
        }

        # create admin
        response = self.app.post('/user', data=json.dumps(payload), headers=self.headers)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIsNotNone(data['user'], 'Failed to create user')

        # create user for customer Foo
        payload = {
            'name': 'Foo customer',
            'login': 'user@foo.com',
            'provider': 'basic',
            'text': 'foo customer'
        }

        response = self.app.post('/user', data=json.dumps(payload), headers=self.headers)
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIsNotNone(data['user'], 'Failed to create user')

        # assign customer Foo
        payload = {
            'customer': 'Foo Corp.',
            'match': 'foo.com'
        }
        response = self.app.post('/customer', data=json.dumps(payload), headers=self.headers)
        self.assertEqual(response.status_code, 201)

        # login to get a bearer token

        # use bearer token to create an API key

        # create alert
        response = self.app.post('/alert', data=json.dumps(self.major_alert), headers=self.headers)
        self.assertEqual(response.status_code, 201)

        # query for alert, check customer

        # create user for customer Bar

        # assign customer Bar

        # create alert

        # query for alert, check customer


    # def test_401_error(self):
    #
    #     response = self.app.get('/alerts')
    #     self.assertEqual(response.status_code, 401)
    #
    # def test_readwrite_key(self):
    #
    #     payload = {
    #         'user': 'rw-demo-key',
    #         'type': 'read-write'
    #     }
    #
    #     response = self.app.post('/key', data=json.dumps(payload), headers=self.headers)
    #     self.assertEqual(response.status_code, 201)
    #     data = json.loads(response.data.decode('utf-8'))
    #     self.assertIsNotNone(data['key'], 'Failed to create read-write key')
    #
    #     rw_api_key = data['key']
    #
    #     response = self.app.post('/alert', data=json.dumps(self.alert), headers={'Authorization': 'Key ' + rw_api_key})
    #     self.assertEqual(response.status_code, 201)
    #
    #     response = self.app.get('/alerts', headers={'Authorization': 'Key ' + rw_api_key})
    #     self.assertEqual(response.status_code, 200)
    #     data = json.loads(response.data.decode('utf-8'))
    #     self.assertIn('total', data)
    #
    #     response = self.app.delete('/key/' + rw_api_key, headers=self.headers)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_readonly_key(self):
    #
    #     payload = {
    #         'user': 'ro-demo-key',
    #         'type': 'read-only'
    #     }
    #
    #     response = self.app.post('/key', data=json.dumps(payload), headers=self.headers)
    #     self.assertEqual(response.status_code, 201)
    #     data = json.loads(response.data.decode('utf-8'))
    #     self.assertIsNotNone(data['key'], 'Failed to create read-only key')
    #
    #     ro_api_key = data['key']
    #
    #     response = self.app.post('/alert', data=json.dumps(self.alert), headers={'Authorization': 'Key ' + ro_api_key})
    #     self.assertEqual(response.status_code, 403)
    #
    #     response = self.app.get('/alerts', headers={'Authorization': 'Key ' + ro_api_key})
    #     self.assertEqual(response.status_code, 200)
    #     data = json.loads(response.data.decode('utf-8'))
    #     self.assertIn('total', data)
    #
    #     response = self.app.delete('/key/' + ro_api_key, headers=self.headers)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_users(self):
    #
    #     payload = {
    #         'name': 'Napoleon Bonaparte',
    #         'login': 'napoleon@bonaparte.fr',
    #         'provider': 'google',
    #         'text': 'added to circle of trust'
    #     }
    #
    #     # create user
    #     response = self.app.post('/user', data=json.dumps(payload), headers=self.headers)
    #     self.assertEqual(response.status_code, 201)
    #     data = json.loads(response.data.decode('utf-8'))
    #     self.assertIsNotNone(data['user'], 'Failed to create user')
    #
    #     user_id = data['user']
    #
    #     # get user
    #     response = self.app.get('/users', headers=self.headers)
    #     self.assertEqual(response.status_code, 200)
    #     data = json.loads(response.data.decode('utf-8'))
    #     self.assertIn(user_id, [u['id'] for u in data['users']])
    #
    #     # create duplicate user
    #     response = self.app.post('/user', data=json.dumps(payload), headers=self.headers)
    #     self.assertEqual(response.status_code, 409)
    #
    #     # delete user
    #     response = self.app.delete('/user/' + user_id, headers=self.headers)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_login(self):
    #
    #     name = 'Josephine de Beauharnais'
    #
    #     payload = {
    #         'name': name,
    #         'email': 'josephine@debeauharnais.fr',
    #         'password': 'blackforest',
    #         'provider': 'basic',
    #         'text': 'Test login'
    #     }
    #
    #     # sign-up user with no customer mapping
    #     response = self.app.post('/auth/signup', data=json.dumps(payload), headers={'Content-type': 'application/json'})
    #     self.assertEqual(response.status_code, 403)
    #
    #     # add customer mapping
    #     payload = {
    #         'customer': 'Bonaparte Industries',
    #         'match': 'debeauharnais.fr'
    #     }
    #     response = self.app.post('/customer', data=json.dumps(payload), headers=self.headers)
    #     self.assertEqual(response.status_code, 201)
    #
    #     payload = {
    #         'email': 'josephine@debeauharnais.fr',
    #         'password': 'blackforest'
    #     }
    #
    #     # login now that customer mapping exists
    #     response = self.app.post('/auth/login', data=json.dumps(payload), headers={'Content-type': 'application/json'})
    #     self.assertEqual(response.status_code, 200)
    #     data = json.loads(response.data.decode('utf-8'))
    #     self.assertIn('token', data)
    #
    #     token = data['token']
    #
    #     headers = {
    #         'Authorization': 'Bearer ' + token,
    #         'Content-type': 'application/json'
    #     }
    #
    #     # create a customer demo key
    #     payload = {
    #         'user': 'customer-demo-key',
    #         'type': 'read-only'
    #     }
    #
    #     response = self.app.post('/key', data=json.dumps(payload), headers=headers)
    #     self.assertEqual(response.status_code, 201)
    #     data = json.loads(response.data.decode('utf-8'))
    #     self.assertIsNotNone(data['key'], 'Failed to create read-only key')
    #
    #     customer_api_key = data['key']
    #
    #     response = self.app.get('/alerts', headers={'Authorization': 'Key ' + customer_api_key})
    #     self.assertEqual(response.status_code, 200)
    #     data = json.loads(response.data.decode('utf-8'))
    #     self.assertIn('total', data)
    #
    #     response = self.app.delete('/key/' + customer_api_key, headers={'Authorization': 'Key ' + customer_api_key})
    #     self.assertEqual(response.status_code, 403)
    #
    #     response = self.app.delete('/key/' + customer_api_key, headers=self.headers)
    #     self.assertEqual(response.status_code, 200)
    #
    #     # get user
    #     response = self.app.get('/users', headers=self.headers)
    #     self.assertEqual(response.status_code, 200)
    #     data = json.loads(response.data.decode('utf-8'))
    #     self.assertIn(name, [u['name'] for u in data['users']])
    #
    #     user_id = [u['id'] for u in data['users'] if u['name'] == name][0]
    #
    #     # delete user
    #     response = self.app.delete('/user/' + user_id, headers=self.headers)
    #     self.assertEqual(response.status_code, 200)
    #
    #     # delete customer mapping
    #     response = self.app.delete('/customer/' + 'Bonaparte Industries', headers=self.headers)
    #     self.assertEqual(response.status_code, 200)
