import logging

import pandas as pd
from cameo.flux_analysis.simulation import lmoma
from cameo.strain_design.deterministic.linear_programming import OptKnock
from cameo.strain_design.heuristic.evolutionary_based import OptGene
from cobra import Model


def gene_ko(
    model: Model,
    max_knockouts: int,
    biomass_id: str,
    target_id: str,
    substrate_id: str,
    logger: logging.Logger,
    seed: int,
    thread: int = 1,
) -> pd.DataFrame:
    optgene = OptGene(model)
    results = optgene.run(
        target=target_id,
        biomass=biomass_id,
        substrate=substrate_id,
        max_knockouts=max_knockouts,
        simulation_method=lmoma,
        seed=seed,
    )
    df = pd.DataFrame(
        columns=[
            "reactions",
            "genes",
            "size",
            "fva_min",
            "fva_max",
            "target_flux",
            "biomass_flux",
            "yield",
            "fitness",
        ]
    )
    try:
        df = results.data_frame
    except Exception:
        logging.warning("An error occurred, maybe there is no solution")
    return df


def gene_ou(
    model: Model,
    max_knockouts: int,
    biomass_id: str,
    target_id: str,
    logger: logging.Logger,
    thread: int = 1,
) -> pd.DataFrame:
    optknock = OptKnock(model, fraction_of_optimum=0.1)
    results = optknock.run(
        target=target_id,
        biomass=biomass_id,
        max_knockouts=max_knockouts,
    )
    df = pd.DataFrame(
        columns=[
            "reactions",
            "size",
            target_id,
            "biomass",
            "fva_min",
            "fva_max",
        ]
    )
    try:
        df = results.data_frame
    except Exception:
        logging.warning("An error occurred, maybe there is no solution")
    return df
