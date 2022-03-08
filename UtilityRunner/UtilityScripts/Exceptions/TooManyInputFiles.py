class TooManyInputFiles(Exception):
    def __init__(self, message="Too many Command line arguments provided!"):
        super().__init__(self.message)