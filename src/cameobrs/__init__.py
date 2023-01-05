"""
CAMEO-Brs: Computer Aided Metabolic Engineering & Optimization (Hard fork from Brsynth team)

CameoBrs is a high-level python library developed to aid the in silico
strain design process in metabolic engineering projects. The library
provides a modular architecture that enables the efficient construction
of custom analysis workflows.

Example
-------

from cameobrs import load_model

# load a model from SBML format (can be found under cameo/tests/data)
model = load_model('EcoliCore.xml')

# optimize the model and print the objective value
solution = model.optimize()
print 'Objective value:', solution.objective_value

# Determine a set of gene deletions that will optimize the production
# of a desired compound
from cameobrs.strain_design.heuristic import GeneKnockoutOptimization
from cameobrs.strain_design.heuristic.objective_functions import biomass_product_coupled_yield
from cameobrs.flux_analysis.simulation import fba

objective = biomass_product_coupled_yield("Ec_biomass_iJO1366_core_53p95M",
                                          "EX_succ_lp_e_rp_", "EX_glc_lp_e_rp_")
optimization = GeneKnockoutOptimization(model=model, objective_function=of,
                              simulation_method=fba, heuristic_method=inspyred.ec.GA)
optimization.run(max_evaluations=2000, n=1,
       mutation_rate=0.3, view=cameo.parallel.SequentialView(),
       product="EX_succ_lp_e_rp_", num_elites=1)
"""

import os
import sys

from cameobrs import config
from cameobrs.util import get_system_info, in_ipnb

if sys.version_info[0] == 2:
    import imp

    def find_module(name):
        try:
            imp.find_module(name)
            return True
        except ImportError:
            return False

elif sys.version_info[0] == 3:
    if sys.version_info[1] <= 3:
        from importlib import find_loader as _find
    else:
        from importlib.util import find_spec as _find

    def find_module(name):
        return _find(name) is not None


_cameo_path = __path__[0]
_cameo_data_path = os.path.join(_cameo_path, "data")

# fix - if matplotlib is installed it is not possible to import cameo without importing matplotlib on jupyter notebook.
if find_module("matplotlib") and in_ipnb():
    from IPython import get_ipython

    ipython = get_ipython()
    ipython.magic("matplotlib inline")

system_info = get_system_info()

from cameobrs._version import __version__

from cameobrs import models
from cameobrs.io import load_model

from .flux_analysis.analysis import flux_variability_analysis, phenotypic_phase_plane
from .flux_analysis.simulation import fba, pfba

del os, sys, in_ipnb, get_system_info, find_module
