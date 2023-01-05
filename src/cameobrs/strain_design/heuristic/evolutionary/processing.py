from cameobrs import flux_variability_analysis
from cameobrs.core.manipulation import swap_cofactors, find_gene_knockout_reactions


def process_reaction_knockout_solution(
    model,
    solution,
    simulation_method,
    simulation_kwargs,
    biomass,
    target,
    substrate,
    objective_function,
):
    """

    Parameters
    ----------

    model: cobra.Model
        A constraint-based model
    solution: tuple - (reactions, knockouts)
        The output of a decoder
    simulation_method: function
        See see cameo.flux_analysis.simulation
    simulation_kwargs: dict
        Keyword arguments to run the simulation method
    biomass: Reaction
        Cellular biomass reaction
    target: Reaction
        The strain design target
    substrate: Reaction
        The main carbon source uptake rate
    objective_function: cameo.strain_design.heuristic.evolutionary.objective_functions.ObjectiveFunction
        The objective function used for evaluation.

    Returns
    -------
    list
        A list with: reactions, size, fva_min, fva_max, target flux, biomass flux, yield, fitness

    """

    with model:
        reactions = [model.reactions.get_by_id(rid) for rid in solution]
        for reaction in reactions:
            reaction.knock_out()

        flux_dist = simulation_method(
            model,
            reactions=objective_function.reactions,
            objective=biomass,
            **simulation_kwargs
        )
        model.objective = biomass
        fva = flux_variability_analysis(
            model, fraction_of_optimum=0.99, reactions=[target]
        )
        target_yield = flux_dist[target] / abs(flux_dist[substrate])
        return [
            solution,
            len(solution),
            fva.lower_bound(target),
            fva.upper_bound(target),
            flux_dist[target],
            flux_dist[biomass],
            target_yield,
            objective_function(model, flux_dist, reactions),
        ]


def process_gene_knockout_solution(
    model,
    solution,
    simulation_method,
    simulation_kwargs,
    biomass,
    target,
    substrate,
    objective_function,
):
    """

    Parameters
    ----------
    model: cobra.Model
        A constraint-based model
    solution: tuple
        The genes
    simulation_method: function
        See see cameo.flux_analysis.simulation
    simulation_kwargs: dict
        Keyword arguments to run the simulation method
    biomass: Reaction
        Cellular biomass reaction
    target: Reaction
        The strain design target
    substrate: Reaction
        The main carbon source uptake rate
    objective_function: cameo.strain_design.heuristic.evolutionary.objective_functions.ObjectiveFunction
        The objective function used for evaluation.

    Returns
    -------
    list
        A list with: reactions, genes, size, fva_min, fva_max, target flux, biomass flux, yield, fitness

    """

    with model:
        genes = [model.genes.get_by_id(gid) for gid in solution]
        reactions = find_gene_knockout_reactions(model, solution)
        for reaction in reactions:
            reaction.knock_out()

        reaction_ids = [r.id for r in reactions]
        flux_dist = simulation_method(
            model,
            reactions=objective_function.reactions,
            objective=biomass,
            **simulation_kwargs
        )
        model.objective = biomass

        fva = flux_variability_analysis(
            model, fraction_of_optimum=0.99, reactions=[target]
        )
        target_yield = flux_dist[target] / abs(flux_dist[substrate])

        return [
            tuple(reaction_ids),
            solution,
            len(solution),
            fva.lower_bound(target),
            fva.upper_bound(target),
            flux_dist[target],
            flux_dist[biomass],
            target_yield,
            objective_function(model, flux_dist, genes),
        ]


def process_reaction_swap_solution(
    model,
    solution,
    simulation_method,
    simulation_kwargs,
    biomass,
    target,
    substrate,
    objective_function,
    swap_pairs,
):
    """

    Parameters
    ----------
    model: cobra.Model
        A constraint-based model
    solution: tuple - (reactions, knockouts)
        The output of a decoder
    simulation_method: function
        See see cameo.flux_analysis.simulation
    simulation_kwargs: dict
        Keyword arguments to run the simulation method
    biomass: Reaction
        Cellular biomass reaction
    target: Reaction
        The strain design target
    substrate: Reaction
        The main carbon source uptake rate
    objective_function: cameo.strain_design.heuristic.evolutionary.objective_functions.ObjectiveFunction
        The objective function used for evaluation.
    swap_pairs:
        The metabolites to swap

    Returns
    -------
    list
        A list with: reactions, size, fva_min, fva_max, target flux, biomass flux, yield, fitness,
        [fitness, [fitness]]

    """

    with model:
        reactions = [model.reactions.get_by_id(rid) for rid in solution]
        for reaction in reactions:
            swap_cofactors(reaction, model, swap_pairs)

        flux_dist = simulation_method(
            model,
            reactions=objective_function.reactions,
            objective=biomass,
            **simulation_kwargs
        )
        model.objective = biomass
        fva = flux_variability_analysis(
            model, fraction_of_optimum=0.99, reactions=[target]
        )
        target_yield = flux_dist[target] / abs(flux_dist[substrate])
        return [
            solution,
            fva.lower_bound(target),
            fva.upper_bound(target),
            flux_dist[target],
            flux_dist[biomass],
            target_yield,
            objective_function(model, flux_dist, reactions),
        ]
