import logging
from typing import List, Optional

import cameobrs
import cobra
import pandas as pd
import plotly
from cameobrs.flux_analysis.simulation import lmoma
from cameobrs.strain_design.deterministic.linear_programming import OptKnock
from cameobrs.strain_design.heuristic.evolutionary_based import OptGene
from cameobrs.visualization.plotting.with_plotly import PlotlyPlotter
from cobra.core.model import Model


def reduce_model(model: cobra.Model, genes: List[str]):
    # Check if gene is in the model.
    model_gene_ids = [x.id for x in model.genes]
    sgenes = set(genes)
    genes = list(genes)
    for gene in sgenes:
        if gene not in model_gene_ids:
            logging.warning(
                "Gene: %s not found in the model, it's a Gene ID provided ?" % (gene,)
            )
            genes.remove(gene)
    # Remove genes.
    number_of_reactions = len(model.reactions)
    cobra.manipulation.remove_genes(model, gene_list=genes, remove_reactions=True)
    # Clean model, functions highly dependent of the cobra's version.
    # model, reactions = cobra.manipulation.prune_unused_reactions(model=model)
    # model, metabolites = cobra.manipulation.delete.prune_unused_metabolites(model=model)

    logging.info("Number of Genes deleted: %s" % (len(genes),))
    logging.info(
        "Number of Reactions deleted: %s"
        % (number_of_reactions - len(model.reactions),)
    )
    return model


def gene_ko(
    model: Model,
    max_knockouts: int,
    biomass_id: str,
    target_id: str,
    substrate_id: str,
    max_time: Optional[int],
    seed: int,
    thread: int = 1,
) -> pd.DataFrame:
    optgene = OptGene(model)
    # Init.
    args = dict(
        target=target_id,
        biomass=biomass_id,
        substrate=substrate_id,
        max_knockouts=max_knockouts,
        simulation_method=lmoma,
        seed=seed,
    )
    if max_time:
        args.update(dict(max_time=(max_time, 0)))
    # Run.
    results = optgene.run(**args)

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
    max_time: Optional[int],
    thread: int = 1,
) -> pd.DataFrame:
    optknock = OptKnock(model, fraction_of_optimum=0.1)
    # Init.
    args = dict(
        target=target_id,
        biomass=biomass_id,
        max_knockouts=max_knockouts,
    )
    if max_time:
        args.update(dict(max_time=(max_time, 0)))
    # Run.
    results = optknock.run(**args)

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


def plot_pareto(
    model: cobra.Model,
    path: str,
    biomass_rxn_id: str,
    target_rxn_id: str,
    substrate_rxn_id: Optional[str] = None,
) -> None:
    # Init.
    abp = cameobrs.visualization.plotting.abstract.AbstractPlotter()
    grid = abp.grid()
    plotter = PlotlyPlotter()

    # Create graph.
    result = cameobrs.phenotypic_phase_plane(
        model,
        variables=[model.reactions.get_by_id(biomass_rxn_id)],
        objective=model.reactions.get_by_id(target_rxn_id),
        source=substrate_rxn_id,
    )
    result.plot(plotter, grid=grid)

    # Export graph.
    fig = dict(data=grid.plots[0].data[0], layout=grid.plots[0].layout)
    plotly.io.write_image(fig=fig, file=path, format="png", engine="orca")
