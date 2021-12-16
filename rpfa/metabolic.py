import logging

import pandas as pd

from typing import (
    List
)

from reframed.io.sbml import load_cbmodel

from mewpy.optimization import EA, set_default_engine
from mewpy.optimization.evaluation import WYIELD, BPCY
from mewpy.simulation import SimulationMethod, get_simulator
from mewpy.util.io import population_to_csv


ITERATIONS = 50
set_default_engine('jmetal')


def build_flux_reference(
    model_path: str,
    biomass_id: str,
    envcond: dict
):
    logging.info('Load model with Reframed')
    model = load_cbmodel(
        model_path,
        flavor='cobra'
    )
    model.set_objective({biomass_id: 1})

    logging.info('Simulate flux reference')
    simulation = get_simulator(
        model,
        envcond=envcond
    )
    res = simulation.simulate(
        method=SimulationMethod.pFBA
    )
    return res.fluxes


def gene_ko(
    model_path,
    envcond: dict,
    biomass_id: str,
    target_id: str,
    flux_reference: pd.Series,
):

    print('biomass id', biomass_id)
    print('target id', target_id)
    print('flux reference', flux_reference)

    logging.info('Load model with Reframed')
    model = load_cbmodel(
        model_path,
        flavor='cobra'
    )
    model.set_objective({biomass_id: 1})

    logging.info('Create evaluators and problem')
    evaluator_1 = BPCY(
        biomass_id,
        target_id,
        method=SimulationMethod.lMOMA
    )
    evaluator_2 = WYIELD(
        biomass_id,
        target_id
    )
    from mewpy.problems.genes import GKOProblem
    problem = GKOProblem(
        model,
        fevaluation=[evaluator_1, evaluator_2],
        envcond=envcond,
        reference=flux_reference,
        target=[target_id]
    )

    logging.info('Launch simulation')
    ea = EA(
        problem,
        max_generations=ITERATIONS,
        mp=True
    )
    final_pop = ea.run()

    individual = max(final_pop)
    best = list(problem.decode(individual.candidate).keys())
    print('Best Solution: \n{0}'.format(str(best)))

    print("Simplifying and saving solutions to file")
    population_to_csv(
        problem,
        final_pop,
        '/opt/pathway/genes/test.csv',
        simplify=False
    )
