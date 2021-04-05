import unittest
import json
import main

class FlaskTest(unittest.TestCase):
    def setUp(self):
        main.app.testing = True
        self.client = main.app.test_client()
    
    def test_index(self):
        response = self.client.get('/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('text/html', response.content_type)
        self.assertEqual(response.charset, 'utf-8')

        content = response.data

        self.assertEqual(content.decode('utf-8'), 'Hello, World!')
    
    def test_users_add(self):
        response = self.client.post(
            '/users',
            data=json.dumps(dict(name='Dowon Lee')),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('application/json', response.content_type)

        result = json.loads(response.data)

        self.assertNotEqual(result.get('user_id'), None)
        self.assertEqual(result.get('name'), 'Dowon Lee')
    
    # def test_tell_something_fails(self):
    #     response = self.client.post(
    #         '/tell/something',
    #         data=json.dumps(dict(gossip='definitely not a message')),
    #         content_type='application/json'
    #     )
        
    #     self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()