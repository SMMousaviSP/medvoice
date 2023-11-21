"""Main module for the Audio Storage Service."""

import io
import base64

from flask import Flask, json, jsonify, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.exceptions import HTTPException
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from flasgger import Swagger, swag_from

from config_local import USERS
from model import AudioLibrary
from validation import allowed_file, is_valid_wav


app = Flask(__name__)
auth = HTTPBasicAuth()
app.config['SWAGGER'] = {
    'title': 'Audio Storage Service',
    'uiversion': 3
}
swagger = Swagger(app)

audio_library = AudioLibrary()


@auth.verify_password
def verify_password(username, password):
    """Verify the password for the username provided."""
    if username in USERS and \
            check_password_hash(USERS.get(username), password):
        return username
    return None


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "data": {},
        "errors": [e.description],
    })
    response.content_type = "application/json"
    return response


@auth.error_handler
def auth_error(status):
    """Return JSON instead of HTML for authentication errors."""
    return jsonify({
        'code': status,
        'data': {},
        'errors': ['Invalid credentials']
    }), status


@app.route('/audio', methods=['POST'])
@auth.login_required
@swag_from('specs/post_audio.yml')
def post_audio():
    """Upload a new audio file."""
    if 'file' not in request.files:
        return jsonify({
            'code': 400,
            'data': {},
            'errors': ['No file part']
        }), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({
            'code': 400,
            'data': {},
            'errors': ['No selected file']
        }), 400

    if file and allowed_file(file.filename):
        file_stream = io.BytesIO(file.read())
        if is_valid_wav(file_stream):
            file_stream.seek(0)  # Reset file pointer to the beginning
            encoded_content = base64.b64encode(file_stream.read()).decode()
            file_id = audio_library.add(
                encoded_content,
                auth.current_user(),
                secure_filename(file.filename)
            )
            return jsonify({
                'code': 201,
                'data': {
                    'id': file_id
                },
                'errors': []
            }), 201
        return jsonify({
            'code': 400,
            'data': {},
            'errors': ['Invalid WAV file']
        }), 400

    return jsonify({
        'code': 400,
        'data': {},
        'errors': ['Invalid file extension']
    }), 400


@app.route('/audio', methods=['GET'])
@auth.login_required
@swag_from('specs/get_all_audios.yml')
def get_audios():
    """Get all audio files."""
    return jsonify({
        'code': 200,
        'data': audio_library.data,
        'errors': []
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
