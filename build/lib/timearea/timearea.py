import mikegraph
from io import StringIO
import pandas as pd
import numpy as np
import ColebrookWhite
import networkx as nx
import os

class TimeArea:
    def __init__(self, rain_filepath):
        if os.path.splitext(rain_filepath)[1].lower() == ".dfs0":
            import mikeio
            dfs0 = mikeio.open(rain_filepath)
            self.series = dfs0.to_pandas()
            self.series = self.series.resample("60s").bfill()
            self.rain_event = np.concatenate((self.series.values[:], np.zeros(60)))

        else:
            with open(rain_filepath, 'r') as f:
                txt = f.read()

            delimiter = r"  " if "  " in txt else r"\t"
            if "," in txt:
                txt = txt.replace(r",", r".")
                rain_filepath = StringIO(unicode(txt))

            self.series = pd.read_csv(rain_filepath, delimiter=delimiter, skiprows=3, names=["Intensity"], engine='python')
            self.series.index = pd.to_datetime(self.series.index)
            self.series = self.series.resample("60s").bfill()
            self.rain_event = np.concatenate((self.series.values[:, 0], np.zeros(60)))

        self.additional_discharge = {}
        self.scaling_factor = 1

    def rationelCurve(self, target, graph):
        sources = graph.find_upstream_nodes(target)[0]

        total_runoff = np.zeros(len(self.rain_event))
        for source in sources:
            if source in self.additional_discharge:
                total_runoff += self.additional_discharge[source]*1e3

            for catchment in graph.find_connected_catchments(source):
                total_runoff += self.rain_event/1e6*catchment.reduced_area*1e3*self.scaling_factor
        return total_runoff

    def timeareaCurve(self, target, graph):
        sources = graph.find_upstream_nodes(target)[0]

        total_runoff = np.zeros(len(self.rain_event))
        for source in sources:
            if source in self.additional_discharge:
                total_runoff += self.additional_discharge[source]*1e3

            travel_time = graph.travel_time(source, target)

            for catchment in graph.find_connected_catchments(source):
                runoff = np.zeros(len(self.rain_event))
                for time_i, rain_intensity in enumerate(self.rain_event):
                    time_i_adjusted = time_i - travel_time/60
                    rain = self.rain_event[
                           max(int(time_i_adjusted - catchment.concentration_time), 0):max(0, int(time_i_adjusted))]
                    runoff[time_i] = np.sum(rain) / catchment.concentration_time if rain.any() else 0
                total_runoff += runoff/1e6*catchment.reduced_area*1e3*self.scaling_factor

        return total_runoff


if __name__ == "__main__":
    graph = mikegraph.Graph(r"C:\Users\elnn\OneDrive - Ramboll\Documents\Aarhus Vand\Soenderhoej\MIKE\MIKE_URBAN\_ORIGINAL\Viby_detailed_200101_40\Viby_detailed_200101_40.sqlite")
    graph.map_network()

    rainseries = TimeArea(r"C:\Users\elnn\OneDrive - Ramboll\Documents\Aarhus Vand\Jens Juuls Vej\MIKE_URBAN\02_RAIN\CDS_T5_5 min.DFS0")
    # rainseries.additional_discharge = {"SEMI25":0.25}

    discharge_ta = rainseries.timeareaCurve(u'D43440R', graph)
    # import timeit
    # timeit.timeit(lambda: rainseries.timeareaCurve(u'Haslevangsvej_R719', graph), number = 5)
    discharge_rat = rainseries.rationelCurve(u'D43440R', graph)
    #
    import matplotlib.pyplot as plt
    #
    plt.step(range(len(discharge_rat)), discharge_rat)
    plt.step(range(len(discharge_ta)), discharge_ta)
    plt.show()
    print("PAUSE")
# [u'O23119R', u'O23117R-1', u'O23116R', u'O23117R', u'O23114R', u'O23134R', u'O23118R', u'O23115R']