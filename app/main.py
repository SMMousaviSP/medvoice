from flask import Flask, json, jsonify
from werkzeug.exceptions import HTTPException
from werkzeug.security import check_password_hash

from config_local import USERS


app = Flask(__name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    """Verify the password for the username provided."""
    if username in USERS and \
            check_password_hash(USERS.get(username), password):
        return username


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


@app.route("/", methods=["GET"])
def hello_world():
    return jsonify({"message": "Hello, World!"}), 200


if __name__ == '__main__':
    app.run(debug=True)
