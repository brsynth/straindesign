import logging

import pandas as pd

from collections import OrderedDict

from rptools.rplibs import (
    rpPathway,
    rpSBML
)
from rptools.rpfba.medium import (
    add_missing_specie,
    crossref_medium_id,
    df_to_medium,
    load_medium_file,
    merge_medium_exchange
)


def load_medium(
    path: str
):
    df = pd.read_csv(
        path,
        header=None,
        index_col=0,
        names=['reaction', 'lower', 'upper']
    )
    medium = df.to_dict('index')
    envcond = OrderedDict()
    for reaction, bounds in medium.items():
        envcond.update({reaction: (bounds['lower'], bounds['upper'])})
    return envcond


def build_env_condition(
    model_path: str,
    medium_path: str,
    medium_compartment_id: str,
    logger: logging.Logger
):

    df_exchange_reaction = pd.DataFrame()
    # Load file
    if medium_path is not None:
        # Check if compartment id is valid
        if medium_compartment_id is None:
            logger.error(
                'Need to fill medium compartment id: %s' %
                (medium_compartment_id,)
            )
            return {}
        model = rpSBML(
            inFile=model_path,
            logger=logger
        )
        model_rppathway = rpPathway.from_rpSBML(
            rpsbml=model,
            logger=logger
        )
        if medium_compartment_id not in model_rppathway.get_compartments():
            logger.error(
                'Compartment id provided is not in the model: %s' %
                (medium_compartment_id,)
            )
            return {}

        logger.info('Load medium file')
        df_medium = load_medium_file(
            filename=medium_path,
            logger=logger
        )

        logger.info('Crossref between medium in the model and provided')
        df_medium = crossref_medium_id(
            df=df_medium,
            model=model,
            compartment_id=medium_compartment_id,
            logger=logger
        )

        logger.info('Select exchange reaction')
        df_exchange_reaction = model.build_exchange_reaction(
            compartment_id=medium_compartment_id
        )

        logger.info('Merge df medium with exchange reactions')
        df_medium = merge_medium_exchange(
            medium=df_medium,
            exchange_reaction=df_exchange_reaction
        )

        logger.info('Add specie missing in the model')
        model = add_missing_specie(
            model=model,
            df=df_medium,
            compartment_id=medium_compartment_id,
            logger=logger
        )
        logging.info('Save model with compounds added')
        model.write_to_file(
            model_path
        )
    else:
        logger.info('Select exchange reaction')
        df_medium = model.build_exchange_reaction(
            compartment_id=medium_compartment_id
        )

    logger.info('Convert exchange reaction to medium')
    medium = df_to_medium(
        df=df_medium
    )
    mediumd = {}
    for compound, upper in medium.items():
        mediumd[compound] = (0, 1000)

    return mediumd
