"""Model classes for the audio library."""

class AudioLibrary:
    """Class to manage audio files with unique IDs."""

    def __init__(self) -> None:
        self.data = {}
        self.__id_counter = self.__count_from_one()

    def add(self, content: str, owner: str, filename: str) -> int:
        """Add a new audio file and return its unique ID."""
        if not all([content, owner, filename]):
            raise ValueError("Content, owner, and filename must be provided.")

        audio_id = next(self.__id_counter)
        self.data[audio_id] = {
            'content': content,
            'owner': owner,
            'filename': filename
        }
        return audio_id

    def __getitem__(self, audio_id: int) -> dict:
        """Retrieve an audio file's information by its ID."""
        try:
            return self.data[audio_id]
        except KeyError as e:
            raise KeyError(f"Audio file with ID {audio_id} does not exist.") from e

    def __count_from_one(self) -> int:
        """Private generator method to create unique IDs starting from 1."""
        n = 1
        while True:
            yield n
            n += 1
