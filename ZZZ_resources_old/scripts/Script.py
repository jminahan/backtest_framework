import logging

class Script():
    def __init__(self):
        logging.debug("In Super Script class")

    @staticmethod
    def run():
        """
        Super version of run
        Should be a set of things to be run for a script a la loading nasdaq symbols
        """
        raise NotImplementedError