####
#
####

##imports
import logging
import pandas
from io import StringIO

class PandasInterface():
    def __init__(self):
        logging.debug("In Pandas Interface")

    def stringcsvToDf(self,
                        stringCSV : str,
                        delim : str = ",") -> pandas.DataFrame:
        """
        takes a string and returns a dataframe from it
        """
        return pandas.read_csv(StringIO(stringCSV.decode("utf-8")), delim)

    def fileToDf(self, filePath : str) -> pandas.DataFrame:
        return pandas.read_csv(filePath)