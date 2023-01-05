from __future__ import absolute_import, print_function

__all__ = ["IPythonNotebookBokehMultiprocessPlotObserver"]

import pandas as pd
import multiprocessing
from pandas import DataFrame

from cameobrs import config
from cameobrs.strain_design.heuristic.evolutionary.multiprocess.observers import (
    AbstractParallelObserver,
    AbstractParallelObserverClient,
)

if config.use_bokeh:
    from bokeh.io import push_notebook
    from bokeh.models import ColumnDataSource
    from bokeh.plotting import figure, show


class IPythonNotebookBokehMultiprocessPlotObserver(AbstractParallelObserver):
    __name__ = "IPython Notebook Bokeh Multiprocess Plot Observer"

    def __init__(self, color_map={}, *args, **kwargs):
        super(IPythonNotebookBokehMultiprocessPlotObserver, self).__init__(
            *args, **kwargs
        )
        self.connections = {}
        self.color_map = color_map
        self.data_frame = DataFrame(columns=["iteration", "island", "color", "fitness"])
        self.plotted = False
        self.handle = None

    def _create_client(self, i):
        self.clients[i] = IPythonNotebookBokehMultiprocessPlotObserverClient(
            queue=self.queue, index=i
        )

    def start(self):
        self._plot()
        AbstractParallelObserver.start(self)

    def _plot(self):
        self.plot = figure(
            title="Fitness plot", tools="", plot_height=400, plot_width=650
        )
        self.plot.xaxis.axis_label = "Iteration"
        self.plot.yaxis.axis_label = "Fitness"
        self.ds = ColumnDataSource(data=dict(x=[], y=[], island=[]))
        self.plot.circle("x", "y", source=self.ds)

        self.handle = show(self.plot, notebook_handle=True)
        self.plotted = True

    def _process_message(self, message):
        if not self.plotted:
            self._plot()

        index = message["index"]
        df = DataFrame(
            {
                "iteration": [message["iteration"]],
                "fitness": [message["fitness"]],
                "color": [self.color_map[index]],
                "island": [index],
            }
        )
        self.data_frame = pd.concat([self.data_frame, df])
        if message["iteration"] % message["n"] == 0:
            self._update_plot()

    def _update_plot(self):
        self.ds.data["x"] = self.data_frame["iteration"]
        self.ds.data["y"] = self.data_frame["fitness"]
        self.ds.data["fill_color"] = self.data_frame["color"]
        self.ds.data["line_color"] = self.data_frame["color"]
        self.ds._dirty = True
        push_notebook(handle=self.handle)

    def stop(self):
        self.data_frame = DataFrame(columns=["iteration", "island", "color", "fitness"])
        self.plotted = False


class IPythonNotebookBokehMultiprocessPlotObserverClient(
    AbstractParallelObserverClient
):
    __name__ = "IPython Notebook Bokeh Multiprocess Plot Observer"

    def __init__(self, *args, **kwargs):
        super(IPythonNotebookBokehMultiprocessPlotObserverClient, self).__init__(
            *args, **kwargs
        )
        self.iteration = 0

    def __call__(self, population, num_generations, num_evaluations, args):
        self.iteration += 1
        best = max(population)
        try:
            self._queue.put_nowait(
                {
                    "fitness": best.fitness,
                    "iteration": self.iteration,
                    "index": self.index,
                    "n": args.get("n", 1),
                }
            )
        except multiprocessing.queues.Full:
            pass

    def reset(self):
        self.iteration = 0

    def close(self):
        raise NotImplementedError
