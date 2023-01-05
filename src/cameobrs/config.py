from __future__ import absolute_import, print_function

from .parallel import SequentialView
from .util import in_ipnb

non_zero_flux_threshold = 1e-6
ndecimals = 6

# Determine available solver interfaces
solvers = {}

try:
    from optlang import glpk_interface

    solvers["glpk"] = glpk_interface
except ImportError:
    pass
try:
    from optlang import cplex_interface

    solvers["cplex"] = cplex_interface
except ImportError:
    pass

# Determine if bokeh is available
try:
    import bokeh
except ImportError:
    use_bokeh = False
else:
    if in_ipnb():
        from bokeh.plotting import output_notebook

        output_notebook(hide_banner=True)
    use_bokeh = True
    bokeh_url = "default"

# Set default parallelization view
default_view = SequentialView()
