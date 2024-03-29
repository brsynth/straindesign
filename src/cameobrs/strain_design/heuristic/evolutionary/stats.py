from __future__ import absolute_import, print_function

import numpy as np
from inspyred.ec.emo import Pareto

from cameobrs import config

if config.use_bokeh:
    from bokeh.models import Range1d
    from bokeh.plotting import figure, output_notebook, show


class GenericStatsData(object):
    def __init__(self, solution, *args, **kwargs):
        super(GenericStatsData, self).__init__(*args, **kwargs)
        self.solution = solution
        self.knockouts_hist, self.knockouts_edges = np.histogram(
            solution.solutions["Size"]
        )

    def display(self):
        raise NotImplementedError


try:
    from bashplotlib.histogram import plot_hist
    from bashplotlib.scatterplot import plot_scatter
except ImportError:
    pass
else:

    class CLIStatsData(GenericStatsData):
        def __init__(self, *args, **kwargs):
            super(CLIStatsData, self).__init__(*args, **kwargs)

        def display(self):
            plot_hist(
                list(self.knockouts_hist),
                title="Knockout size distribution",
                colour="blue",
            )
            lines = [
                "%s, %s" % (x, y)
                for x, y in zip(
                    self.solution.solutions["Size"], self.solution.solutions["Fitness"]
                )
            ]
            plot_scatter(
                lines,
                None,
                None,
                20,
                "*",
                "blue",
                "Correlation between number of knockouts and fitness",
            )


class BokehStatsData(GenericStatsData):
    def __init__(self, *args, **kwargs):
        super(BokehStatsData, self).__init__(*args, **kwargs)
        self.xdr = Range1d(start=-0.5, end=20.5)
        self.ydr = Range1d(start=-0.5, end=20.5)

    def display(self):
        output_notebook(hide_banner=True)
        plot = figure(title="Knockout size distribution")
        plot.quad(
            top=self.knockouts_hist,
            bottom=np.zeros(len(self.knockouts_hist)),
            left=self.knockouts_edges[:-1],
            right=self.knockouts_edges[1:],
            title="Knockout size distribution",
        )
        plot.xaxis.axis_label = "Number of knockouts"
        plot.yaxis.axis_label = "Number of solutions"
        show(plot)

        plot = figure(title="Correlation between number of knockouts and fitness")
        fitness = self.solution.solutions["Fitness"]
        if isinstance(fitness[0], Pareto):
            pass
        else:
            plot.scatter(
                self.solution.solutions["Size"], self.solution.solutions["Fitness"]
            )
            plot.xaxis.axis_label = "Number of knockouts"
            plot.yaxis.axis_label = "Fitness"
        show(plot)
