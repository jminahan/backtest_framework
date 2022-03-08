class ArgNotFoundException(Exception):
    def __init__(self, arg, message="Argument not found : " ):
        self.message = message + arg
        super().__init__(self.message)