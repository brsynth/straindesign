import logging

from typing import (
    List
)
from rptools.rplibs import (
    rpPathway,
    rpSBML
)
from rptools.rpfba.rpFBA import (
    build_rpsbml
)

def build_model(
    model_path: str,
    pathway_path: str,
    output_path: str,
    pathway_compartment: str,
    main_objective: str,
    target_objective: str,
    logger: logging.Logger
):
    logger.info('Load model')
    model = rpSBML(
        inFile=model_path,
        logger=logger
    )
    if pathway_path:
        logger.info('Load pathway')
        # Check if compartment exists in the main model
        pathway = rpPathway.from_rpSBML(
            infile=pathway_path,
            logger=logger
        )
        pathway = build_rpsbml(
            pathway=pathway,
            logger=logger
        )
        model_compartments = model.getModel().getListOfCompartments()
        model_compartments = [x.getId() for x in model_compartments]
        if pathway_compartment not in model_compartments:
            logger.error(
                'Compartment id provided is not in the model: %s' %
                (pathway_compartment,)
            )
            return 0

        logger.info('Merge model and pathway')
        (
            model,
            reactions_in_both,
            missing_species,
            compartment_id
        ) = rpSBML.merge(
            pathway=pathway,
            model=model,
            compartment_id=pathway_compartment,
            logger=logger
        )

    # Check if reactions are in the model
    logger.info('Check if main objective is in the model')
    if model.getModel().getReaction(main_objective) is None:
        logger.error(
            'Reaction not found in the model: %s' % (main_objective,)
        )
        return 0
    logger.info('Check if target reaction is in the model')
    if model.getModel().getReaction(target_objective) is None:
        logger.error(
            'Reaction not found in the model: %s' % (target_objective,)
        )
        return 0

    logger.info('Save model in file: %s' % (output_path,))
    with open(output_path, 'w') as fod:
        model.write_to_file(fod.name)
        fod.close()

    return 1


def load_non_target(
    path: str,
    model: None,
) -> List[str]:
    """Parse non target file

    :param path: A path for file
    :param model: A model to check if data is in the model

    :type path: str
    :type model: (optional)

    :return: A list of reaction id
    :rtype: List[str]
    """
    reactions = []
    with open(path, 'r') as fid:
        reactions = fid.read().splitlines()
    if model is not None:
        pass
    return reactions
