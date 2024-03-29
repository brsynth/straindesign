from __future__ import absolute_import, print_function

import re

from cobra import Reaction

from cameobrs.ui import notice
from cameobrs.util import in_ipnb

try:
    from IPython import display
except ImportError:
    pass

__all__ = ["create_adapter_reactions", "display_pathway"]


def create_adapter_reactions(
    original_metabolites, universal_model, mapping, compartment_regexp
):
    """Create adapter reactions that connect host and universal model.

    Parameters
    ----------
    original_metabolites : list
        List of host metabolites.
    universal_model : cobra.Model
        The universal model.
    mapping : dict
        A mapping between between host and universal model metabolite IDs.
    compartment_regexp : regex
        A compiled regex that matches metabolites that should be connected to the universal model.

    Returns
    -------
    list
        The list of adapter reactions.

    """
    adapter_reactions = []
    metabolites_in_main_compartment = [
        m for m in original_metabolites if compartment_regexp.match(m.compartment)
    ]
    if len(metabolites_in_main_compartment) == 0:
        raise ValueError(
            "no metabolites matching regex for main compartment %s" % compartment_regexp
        )
    for (
        metabolite
    ) in metabolites_in_main_compartment:  # model is the original host model
        name = re.sub(
            "_{}$".format(metabolite.compartment), "", metabolite.id
        )  # TODO: still a hack
        mapped_name = None
        for prefix in [
            "bigg:",
            "kegg:",
            "rhea:",
            "brenda:",
            "",
        ]:  # try no prefix at last
            if prefix + name in mapping:
                mapped_name = mapping[prefix + name]
                break
        if mapped_name is not None:
            adapter_reaction = Reaction(
                str("adapter_" + metabolite.id + "_" + mapped_name)
            )
            adapter_reaction.lower_bound = -1000
            try:
                adapter_reaction.add_metabolites(
                    {
                        metabolite: -1,
                        universal_model.metabolites.get_by_id(mapped_name): 1,
                    }
                )
            except KeyError:
                pass
            else:
                adapter_reactions.append(adapter_reaction)

    return adapter_reactions


def display_pathway(pathway, i):
    notice("Pathway %i" % i)
    if in_ipnb():
        display(pathway.data_frame)
    else:
        print(pathway.data_frame)
