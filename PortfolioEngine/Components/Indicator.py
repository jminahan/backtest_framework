from optparse import Values

from sqlalchemy import true


class Indicator():
    indicators : dict = {}

    def __init__(self):
        pass

    def validateIndicator(self) -> bool:
        sum = 0
        for key, value in self.indicators:
            sum += value

        if sum == 100:
            return true

        raise Exception("Indicator resulted in less than 100 distribution pts")