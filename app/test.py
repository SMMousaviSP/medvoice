"""Test module for the Flask API."""

import base64
# import io
import unittest

from main import app

# Default credentials for testing
USERNAME_PASSWORD = b'test:test'

class FlaskApiTest(unittest.TestCase):
    """Test case for the Flask API."""
    def setUp(self):
        """Set up test variables."""
        self.app = app.test_client()
        self.app.testing = True

    def get_basic_auth_headers(self):
        """Return the headers for basic authentication."""
        credentials = base64.b64encode(USERNAME_PASSWORD).decode('utf-8')
        return {
            'Authorization': f'Basic {credentials}'
        }

    def test_valid_authentication(self):
        """Test that the authentication works with valid credentials."""
        response = self.app.get('/audio', headers=self.get_basic_auth_headers())
        self.assertEqual(response.status_code, 200)

    def test_invalid_authentication(self):
        """Test that the authentication fails with invalid credentials."""
        credentials = base64.b64encode(b'wrong:wrong').decode('utf-8')
        response = self.app.get('/audio', headers={'Authorization': f'Basic {credentials}'})
        self.assertEqual(response.status_code, 401)

    # def test_post_audio_valid(self):
    #     """Test that a valid audio file can be uploaded."""
    #     data = {
    #         'file': (io.BytesIO(b'test wav data'), 'test.wav')
    #     }
    #     response = self.app.post(
    #         '/audio',
    #         data=data,
    #         headers=self.get_basic_auth_headers(),
    #         content_type='multipart/form-data'
    #     )
    #     self.assertEqual(response.status_code, 201)

    def test_post_audio_no_file(self):
        """Test that an error is returned when no file is provided."""
        response = self.app.post('/audio', headers=self.get_basic_auth_headers())
        self.assertEqual(response.status_code, 400)

    def test_get_audios(self):
        """Test that the list of audio files can be retrieved."""
        response = self.app.get('/audio', headers=self.get_basic_auth_headers())
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
