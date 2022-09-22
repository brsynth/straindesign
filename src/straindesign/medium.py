import csv
import logging
from collections import OrderedDict

import pandas as pd
from cobra.core.model import Model


def load_medium(path: str) -> dict:
    # Find delimiter.
    with open(path) as fid:
        dialect = csv.Sniffer().sniff(fid.readline())
    # Load.
    df = pd.read_csv(
        path,
        header=None,
        index_col=0,
        names=["reaction", "lower", "upper"],
        sep=dialect.delimiter,
    )
    medium = df.to_dict("index")
    envcond = OrderedDict()
    for reaction, bounds in medium.items():
        envcond.update({reaction: (bounds["lower"], bounds["upper"])})
    return envcond


def associate_flux_env(model: Model, envcond: dict) -> Model:
    for reaction_id, bounds in envcond.items():
        reaction = model.reactions.get_by_id(reaction_id)
        if reaction is None:
            logging.error("Reaction: %s not found in the model" % (reaction_id,))
            return None
        reaction.bounds = bounds
    return model
