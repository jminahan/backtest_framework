import pandas as pd

class TraderStats():

    '''
    helper class used to keep track of what a trader
    does and what their values are by time slice
    '''
    def __init__(self):
        self.portfolioValueByTimeSlice = {}

    def portfolioValueByTimeSliceAsDf(self):
        return pd.DataFrame(list(zip(
            (i.currentTime for i in self.portfolioValueByTimeSlice.keys()),
            (self.portfolioValueByTimeSlice.values())
            )), columns=["Date", "Close"]).set_index("Date")