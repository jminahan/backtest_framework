from optparse import Values

import logging


class Indicator():
    indicators : dict = {}

    def __init__(self):
        pass

    def validateIndicator(self) -> bool:
        sum = 0
        for key in self.indicators:
            value = self.indicators[key]
            sum += value

        if sum == 100:
            return True

        raise Exception("Indicator resulted in less than 100 distribution pts")