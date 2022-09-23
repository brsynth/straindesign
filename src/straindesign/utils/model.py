import logging

import cobra


def count_gene(model: cobra.Model) -> int:
    return len(model.genes)


def count_reaction(model: cobra.Model) -> int:
    return len(model.reactions)


def has_reaction(model: cobra.Model, reaction: str) -> bool:
    if reaction in [x.id for x in model.reactions]:
        return True
    return False
