import base64
import io
import unittest

from main import app

# Default credentials for testing
username_password = b'test:test'

class FlaskApiTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def get_basic_auth_headers(self):
        credentials = base64.b64encode(username_password).decode('utf-8')
        return {
            'Authorization': f'Basic {credentials}'
        }

    def test_valid_authentication(self):
        response = self.app.get('/audio', headers=self.get_basic_auth_headers())
        self.assertEqual(response.status_code, 200)

    def test_invalid_authentication(self):
        credentials = base64.b64encode(b'wrong:wrong').decode('utf-8')
        response = self.app.get('/audio', headers={'Authorization': f'Basic {credentials}'})
        self.assertEqual(response.status_code, 401)

    # def test_post_audio_valid(self):
    #     data = {
    #         'file': (io.BytesIO(b'test wav data'), 'test.wav')
    #     }
    #     response = self.app.post('/audio', data=data, headers=self.get_basic_auth_headers(), content_type='multipart/form-data')
    #     self.assertEqual(response.status_code, 201)

    def test_post_audio_no_file(self):
        response = self.app.post('/audio', headers=self.get_basic_auth_headers())
        self.assertEqual(response.status_code, 400)

    def test_get_audios(self):
        response = self.app.get('/audio', headers=self.get_basic_auth_headers())
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
