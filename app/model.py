class AudioLibrary:
    """Class to manage audio files with unique IDs."""

    def __init__(self) -> None:
        self.data = {}
        self.__id_counter = self.__count_from_one()

    def add(self, content: str, owner: str, filename: str) -> int:
        """Add a new audio file and return its unique ID."""
        if not all([content, owner, filename]):
            raise ValueError("Content, owner, and filename must be provided.")

        id = next(self.__id_counter)
        self.data[id] = {
            'content': content,
            'owner': owner,
            'filename': filename
        }
        return id
    
    def __count_from_one(self) -> int:
        """Private generator method to create unique IDs starting from 1."""
        n = 1
        while True:
            yield n
            n += 1
