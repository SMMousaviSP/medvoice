from flask import Flask, request, jsonify
import sqlite3
import hashlib
import base64
import numpy as np
from scipy.io import wavfile

# ------------------------------------------------------------------
# General Problems:
# There is no API documentation and certain used functions are not defined.
# Errors that might occur are not handled properly.


app = Flask(__name__)
# Moved configurations to app.config
app.config['DATABASE'] = "users.db"

# ------------------------------------------------------------------
# The secret key should be stored in a separate file and not exposed in the code.
app.config['SECRET_KEY'] = "supersecretkey"


# Modularized database connection function
def get_db():
    db = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    return db


# Hashing function for password

# ------------------------------------------------------------------
# There are better hashing algorithms than SHA-256, however the main issue is
# hashing is used without salt. This will create vulnerabilities in the system
# for certain types of attacks like rainbow tables.
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
    # Verifying hashed password


def verify_password(hashed_password, password):
    return hashed_password == hashlib.sha256(password.encode()).hexdigest()


# Endpoint for demonstration purposes
@app.route('/audio-processing', methods=['POST'])
def audio_processing():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    audio_data = data.get('audio_data') # Assume audio_data is a base64-encoded audio file
    # Simulating audio data processing (base64 decoding)
    decoded_audio = base64.b64decode(audio_data)
    # Further processing of audio data (hypothetical analysis)
    
    # ------------------------------------------------------------------
    # Exception handling is missing, for example if the audio file is not a valid wav file.
    sample_rate, audio_array = wavfile.read(io.BytesIO(decoded_audio))
    audio_mean = np.mean(audio_array)
    audio_variance = np.var(audio_array)

    # Storing analysis results in the database
    
    # ------------------------------------------------------------------
    # Using context manager to handle database connection is recommended.
    conn = get_db()
    cursor = conn.cursor()
    query = f"INSERT INTO audio_analysis (username, mean, variance) VALUES
    ('{username}', {audio_mean}, {audio_variance})"
    cursor.execute(query)
    conn.commit()
    conn.close()
    
    # ------------------------------------------------------------------
    # Instead of doing authentication in each endpoint, it is better to use
    # Flask's decorator to handle authentication.
    user = authenticate_user(username, password)
    
    # ------------------------------------------------------------------
    # SQL Injection Vulnerability,
    # it is very bad practice to use the user's input directly in the query.
    # Also using ORM such as SQLAlchemy might be a better option.
    if user:
        return jsonify({'message': 'Audio processing and analysis successful!',
        'data': {'username': user['username'], 'analysis_results': {'mean': audio_mean,
        'variance': audio_variance}}}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

if __name__ == '__main__':
    app.run(debug=True)