import logging

from cobra import (
    Model,
)
from cameo.strain_design.deterministic.linear_programming import OptKnock
from cameo.strain_design.heuristic.evolutionary_based import OptGene
from cameo.flux_analysis.simulation import lmoma


def gene_ko(
    model: Model,
    max_knockouts: int,
    biomass_id: str,
    target_id: str,
    substrate_id: str,
    logger: logging.Logger,
    thread: int = 1
):
    optgene = OptGene(model)
    results = optgene.run(
        target=target_id,
        biomass=biomass_id,
        substrate=substrate_id,
        max_knockouts=max_knockouts,
        simulation_method=lmoma
    )
    return results.data_frame


def gene_ou(
    model: Model,
    max_knockouts: int,
    biomass_id: str,
    target_id: str,
    substrate_id: str,
    logger: logging.Logger,
    thread: int = 1
):
    optknock = OptKnock(
        model,
        fraction_of_optimum=0.1
    )
    results = optknock.run(
        target=target_id,
        biomass=biomass_id,
        max_knockouts=max_knockouts
    )
    return results.data_frame
