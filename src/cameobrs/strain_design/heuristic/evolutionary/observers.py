from __future__ import absolute_import, print_function

from IProgress.progressbar import ProgressBar
from IProgress.widgets import Bar, Percentage


class ProgressObserver(object):
    """
    Progress bar to in command line. It keeps track of the progress during heuristic optimization.
    """

    __name__ = "Progress Observer"

    def __init__(self):
        self.progress = None

    def __call__(self, population, num_generations, num_evaluations, args):
        if self.progress is None:
            self.max_evaluations = args.get("max_evaluations", 50000)
            self.progress = ProgressBar(
                maxval=self.max_evaluations,
                widgets=["Running Optimization", Bar(), Percentage()],
            )
            self.progress.start()

        if num_evaluations % args.get("n", 1) == 0:
            if num_evaluations > self.max_evaluations:
                self.progress.update(self.max_evaluations)
            else:
                self.progress.update(num_evaluations)

    def reset(self):
        self.progress = None

    def end(self):
        self.progress.finish()
        self.progress = None
