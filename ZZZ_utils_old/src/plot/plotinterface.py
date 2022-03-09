import logging
import matplotlib
import pandas
from utils.src.plot.PresetGraphs.DefaultGraph import 

class PlotInterface():
    def __init__(self):
        logging.debug("In Plot Interface")

    def initGraph(self, graph : DefaultGraph):
        plt.figure()
