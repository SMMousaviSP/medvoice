import wave


def allowed_file(filename):
    """Check if the filename has a valid extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'wav'

def is_valid_wav(file_stream):
    """Check if the file is a valid WAV file."""
    try:
        with wave.open(file_stream) as audio:
            return True
    except wave.Error:
        return False