"""
Multiprocess heuristic optimization.

Implementation of the islands model. The islands model consists of having multiple processes running in parallel where
individual process is running an isolated heuristic optimization, therefor called island.
At certain time points, individuals in an island can migrate through a Queue. That individual will arrive in a another
island and introduce variability in population of that island.

For information on how to run Gene Knockout or Reaction Knockout optimizations refer to
cameo.strain_design.heuristic.optimization

The result object is the same as in the single objective optimization. The knockouts solutions resulting from all
processes are merged.

Examples
--------
>>> from cameobrs import models
>>> from cameobrs.strain_design.heuristic.evolutionary.multiprocess import MultiprocessGeneKnockoutOptimization
>>> from cameobrs.strain_design.heuristic.evolutionary.objective_functions import biomass_product_coupled_yield
>>> import inspyred
>>>
>>> model = models.bigg.iJO1366
>>> objective_function = biomass_product_coupled_yield('BIOMASS_iJO1366_core_53p95M', 'EX_succ_e', 'EX_glc__D_e')
>>> opt = MultiprocessGeneKnockoutOptimization(model=model,
>>>                                            objective_function=objective_function,
>>>                                            heuristic_method=inspyred.ec.GA,
>>>                                            max_migrants=1)
>>> result = opt.run()


"""
from .optimization import (
    MultiprocessGeneKnockoutOptimization,
    MultiprocessReactionKnockoutOptimization,
)
