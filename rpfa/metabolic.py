import logging

import pandas as pd

from typing import (
    List
)

from reframed.io.sbml import load_cbmodel

from mewpy.optimization import EA, set_default_engine
from mewpy.optimization.evaluation import WYIELD, BPCY
from mewpy.problems.genes import GKOProblem
from mewpy.simulation import SimulationMethod, get_simulator
from mewpy.util.constants import EAConstants
from mewpy.util.io import population_to_csv


set_default_engine('jmetal')


def build_flux_reference(
    model_path: str,
    biomass_id: str,
    envcond: dict,
    logger: logging.Logger
):
    logger.info('Load model with Reframed')
    model = load_cbmodel(
        model_path,
        flavor='cobra'
    )
    model.set_objective({biomass_id: 1})

    logger.info('Simulate flux reference')

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
    output_path: str,
    envcond: dict,
    biomass_id: str,
    target_id: str,
    flux_reference: pd.Series,
    logger: logging.Logger,
    thread: int=1
):
    # Set threads
    EAConstants.NUM_CPUS = thread

    logger.info('Load model with Reframed')
    model = load_cbmodel(
        model_path,
        flavor='cobra'
    )
    model.set_objective({biomass_id: 1})

    logger.info('Create evaluators and problem')
    evaluator_1 = BPCY(
        biomass_id,
        target_id,
        method=SimulationMethod.lMOMA
    )
    evaluator_2 = WYIELD(
        biomass_id,
        target_id
    )
    problem = GKOProblem(
        model,
        fevaluation=[evaluator_1, evaluator_2],
        envcond=envcond,
        reference=flux_reference,
        target=[target_id]
    )

    logger.info('Launch simulation')
    ea = EA(
        problem,
        max_generations=10,
        mp=True
    )
    final_pop = ea.run()

    logger.info("Saving solutions to file")
    population_to_csv(
        problem,
        final_pop,
        output_path,
        simplify=True
    )
