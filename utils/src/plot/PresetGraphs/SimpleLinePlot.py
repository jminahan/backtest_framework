import logging
from utils.src.plot.PresetGraphs.DefaultGraph import DefaultGraph
import pandas as pd
import plotly.express as px

class SimpleLinePlot(DefaultGraph):
    def __init__(self):
        logging.debug("SimplePricePlot init")

    def buildPlot(self, df : pd.DataFrame):
        '''
            Takes in a df with the following headers
            ["Date", price] or ["Date", return] for a single symbol
            
            and produces a graph
        '''
        headers = list(df.columns.values)
        self.fig = px.line(df, x = df.index, y = df.columns.values)
        self.fig.update_layout(hovermode='x unified')


    def show(self):
        self.fig.show()