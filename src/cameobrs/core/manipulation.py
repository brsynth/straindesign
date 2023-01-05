"""
Manage manipulations such as swapping reaction cofactors, over-express or down-regulate genes and reactions.

"""
from ast import Module
from typing import Any, Dict, List, Optional
from cobra import Gene, Model, Reaction


def increase_flux(reaction, ref_value, value):
    """
    lb                           0                           ub
    |--------------------------- ' ---------------------------|
                <- - -|----------'
                                 '----------|- - - ->

    Parameters
    ----------
    reaction: cobra.Reaction
        The reaction to over-express.
    ref_value: float
        The flux value to come from.
    value: float
        The flux value to achieve.

    """
    if abs(value) < abs(ref_value):
        raise ValueError(
            "'value' is lower than 'ref_value', this is increase_flux (%f < %f)"
            % (value, ref_value)
        )

    if value > 0:
        reaction.lower_bound = value
    elif value < 0:
        reaction.upper_bound = value
    else:
        reaction.knock_out()


def decrease_flux(reaction, ref_value, value):
    """
    lb                           0                           ub
    |--------------------------- ' ---------------------------|
                 |- - >----------'
                                 '----------<- - - -|

    Parameters
    ----------
    reaction: cobra.Reaction
        The reaction to down_regulate.
    ref_value: float
        The flux value to come from.
    value: float
        The flux value to achieve.

    """
    if abs(value) > abs(ref_value):
        raise ValueError(
            "'value' is higher than 'ref_value', this is decrease_flux (%f < %f)"
            % (value, ref_value)
        )

    if value > 0:
        reaction.upper_bound = value
    elif value < 0:
        reaction.lower_bound = value
    else:
        reaction.knock_out()


def reverse_flux(reaction, ref_value, value):
    """

    Forces a reaction to have a minimum flux level in the opposite direction of a reference state.

    lb                           0                           ub
    |--------------------------- ' ---------------------------|
                      <----------'- - - - - - - ->

    Parameters
    ----------
    reaction: cobra.Reaction
        The reaction that will be inverted.
    ref_value: float
        The flux value to come from.
    value: float
        The flux value to achieve.

    """
    if (value >= 0) == (ref_value >= 0):
        raise ValueError(
            "'value' and 'ref_value' cannot have the same sign (%.5f, %.5f)"
            % (value, ref_value)
        )

    if value > 0:
        reaction.upper_bound = value
    elif value < 0:
        reaction.lower_bound = value
    else:
        reaction.knock_out()


def swap_cofactors(reaction, model, swap_pairs, inplace=True):
    """
    Swaps the cofactors of a reaction. For speed, it can be done inplace which just changes the coefficients.
    If not done inplace, it will create a new Reaction, add it to the model, and knockout the original reaction.

    Parameters
    ----------
    reaction: cobra.Reaction
        The reaction to swap.
    model: cameo.cobra.Model
        A constraint-based model.
    swap_pairs: tuple
        A tuple of (cofactors, equivalent_cofactors)
    inplace: bool
        If replace is done inplace, it changes the coefficients in the matrix. Otherwise, it creates a new reaction
        with the other cofactors and adds it to the model.

    Returns
    -------
        Reaction
            A reaction with swapped cofactors (the same if inplace).
    """
    if all(reaction.metabolites.get(met, False) for met in swap_pairs[0]):
        new_coefficients = {met: -reaction.metabolites[met] for met in swap_pairs[0]}
        new_coefficients.update(
            {new_met: reaction.metabolites[met] for met, new_met in zip(*swap_pairs)}
        )
    elif all(reaction.metabolites.get(met, False) for met in swap_pairs[1]):
        new_coefficients = {met: -reaction.metabolites[met] for met in swap_pairs[1]}
        new_coefficients.update(
            {new_met: reaction.metabolites[met] for new_met, met in zip(*swap_pairs)}
        )
    else:
        raise ValueError(
            "%s: Invalid swap pairs %s (%s)"
            % (reaction.id, str(swap_pairs), reaction.reaction)
        )

    def _inplace(rxn, stoichiometry):
        rxn.add_metabolites(stoichiometry, combine=True)

    def _replace(rxn, stoichiometry):
        new_reaction = Reaction(
            id="%s_swap" % rxn.id,
            name=rxn.name,
            lower_bound=rxn.lower_bound,
            upper_bound=rxn.upper_bound,
        )
        new_reaction.stoichiometry = rxn
        new_reaction.add_metabolites(stoichiometry)
        return new_reaction

    if inplace:
        _inplace(reaction, new_coefficients)
        return reaction
    else:
        new_reaction = _replace(reaction, new_coefficients)
        model.add_reactions([new_reaction])
        reaction.knock_out()
        return new_reaction


def find_gene_knockout_reactions(
    model: Model,
    gene_list: List[Gene],
    compiled_gene_reaction_rules: Optional[Dict[Reaction, Any]] = None,
) -> List[Reaction]:
    """Identify reactions which will be disabled when genes are knocked out.

    Parameters
    ----------
    model: cobra.Model
        The model for which to find gene knock-out reactions.
    gene_list: list of cobra.Gene
        The list of genes to knock-out.
    compiled_gene_reaction_rules: dict of {reaction: compiled_string},
                                  optional
        If provided, this gives pre-compiled gene-reaction rule strings.
        The compiled rule strings can be evaluated much faster. If a rule
        is not provided, the regular expression evaluation will be used.
        Because not all gene-reaction rule strings can be evaluated, this
        dict must exclude any rules which can not be used with eval
        (default None).

    Returns
    -------
    list of cobra.Reaction
       The list of cobra.Reaction objects which will be disabled.

    Provided
    --------
    Copy from https://github.com/opencobra/cobrapy Release 0.24.0
    """
    potential_reactions = set()
    for gene in gene_list:
        if isinstance(gene, str):
            gene = model.genes.get_by_id(gene)
        potential_reactions.update(gene._reaction)
    gene_set = {str(i) for i in gene_list}
    if compiled_gene_reaction_rules is None:
        compiled_gene_reaction_rules = {r: r.gpr for r in potential_reactions}

    return [
        r
        for r in potential_reactions
        if not compiled_gene_reaction_rules[r].eval(gene_set)
    ]
