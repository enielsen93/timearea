import mikegraph
from io import StringIO
import pandas as pd
import numpy as np
import ColebrookWhite
import networkx as nx

class TimeArea:
    def __init__(self, rain_filepath):
        with open(rain_filepath, 'r') as f:
            txt = f.read()

        delimiter = r"  " if "  " in txt else r"\t"
        if "," in txt:
            txt = txt.replace(r",", r".")
            rain_filepath = StringIO(unicode(txt))

        series = pd.read_csv(rain_filepath, delimiter=delimiter, skiprows=3, names=["Intensity"], engine = 'python')
        series.index = pd.to_datetime(series.index)
        series = series.resample("60S").ffill()

        self.rain_event = np.concatenate((series.values[:, 0], np.zeros(60)))


    def rationelCurve(self, target, graph):
        sources = graph.find_upstream_nodes(target)[0]

        total_runoff = np.zeros(len(self.rain_event))
        for source in sources:
            for catchment in graph.find_connected_catchments(source):
                total_runoff += self.rain_event/1e6*catchment.reduced_area*1e3
        return total_runoff

    def timeareaCurve(self, target, graph):
        sources = graph.find_upstream_nodes(target)[0]

        total_runoff = np.zeros(len(self.rain_event))
        for source in sources:
            travel_time = graph.travel_time(source, target)

            for catchment in graph.find_connected_catchments(source):
                runoff = np.zeros(len(self.rain_event))
                for time_i, rain_intensity in enumerate(self.rain_event):
                    time_i_adjusted = time_i - travel_time/60
                    rain = self.rain_event[
                           max(int(time_i_adjusted - catchment.concentration_time), 0):max(0, int(time_i_adjusted))]
                    runoff[time_i] = np.sum(rain) / catchment.concentration_time if rain.any() else 0

                total_runoff += runoff/1e6*catchment.reduced_area*1e3

        return total_runoff


if __name__ == "__main__":
    graph = mikegraph.Graph(r"C:\Offline\MOL_055R_opdim_Langebro.mdb")
    graph.map_network()

    rainseries = TimeArea(r"C:\Offline\MOL_CDS5Aar.txt")

    discharge_ta = rainseries.timeareaCurve(u'Node_93', graph)
    discharge_rat = rainseries.rationelCurve(u'Node_93', graph)

    import matplotlib.pyplot as plt

    plt.step(range(len(discharge_rat)), discharge_rat*1.51)
    plt.step(range(len(discharge_ta)), discharge_ta*1.51)
    plt.show()
    print("PAUSE")
# [u'O23119R', u'O23117R-1', u'O23116R', u'O23117R', u'O23114R', u'O23134R', u'O23118R', u'O23115R']