#!/usr/bin/env python
# coding: utf8

import argparse
import logging
import os
import tempfile
import shutil
import sys

from rpfa.preprocess import (
    build_model,
    load_non_target
)
from rpfa.medium import (
    load_medium,
    build_env_condition
)
from rpfa.metabolic import (
    build_flux_reference,
    gene_ko
)


def main():
    """CLI for rpFbaAnalysis"""

    desc = ""  \
        ""

    parser = argparse.ArgumentParser(
        description=desc,
        prog='python -m rpfa'
    )
    # Input
    parser_input = parser.add_argument_group(
        'Input'
    )
    parser_input.add_argument(
        '--input-model-file',
        type=str,
        required=True,
        help='GEM model file (SBML)'
    )
    parser_input.add_argument(
        '--input-pathway-file',
        type=str,
        required=False,
        help='SBML file that contains an heterologous pathway'
    )
    parser_input.add_argument(
        '--input-pathway-compartment',
        type=str,
        required=False,
        help='Compartment in which the pathway is located'
    )
    parser_input.add_argument(
        '--biomass-rxn-id',
        type=str,
        required=True,
        help='Biomass reaction ID'
    )
    parser_input.add_argument(
        '--target-rxn-id',
        type=str,
        required=False,
        help='Target reaction ID'
    )
    # Output
    parser_output = parser.add_argument_group(
        'Output'
    )
    parser_output.add_argument(
        '--output-file',
        type=str,
        required=True,
        help='output file'
    )
    # Simulation
    parser_sim = parser.add_argument_group(
        'Simulation'
    )
    parser_sim.add_argument(
        '--strategy',
        type=str,
        choices=['ko', 'ou'],
        default='ko',
        help='Strategy to use : ko (knocking out) or ou '
             '(over-under expressing), (default: ko)'
    )
    # Medium
    parser_medium = parser.add_argument_group(
        'Medium'
    )
    parser_medium.add_argument(
        '--medium-compartment-id',
        type=str,
        default='MNXC2',
        help='Model compartiment id corresponding '
             'to the extra-cellular compartment'
    )
    parser_medium.add_argument(
        '--input-medium-file',
        type=str,
        help='Provide a csv file with an header as <coumpond_id>,'
             '<lower_bound>, <upper_bound>. This file '
             'provides information about metabolites (Metanetx Id) '
             'to add or remove.'
    )
    # Others.
    parser_helper = parser.add_argument_group(
        'Technical'
    )
    parser_helper.add_argument(
        '--thread',
        type=int,
        default=1,
        help='Number of threads to use'
    )
    parser_helper.add_argument(
        '--log-level',
        choices=['ERROR', 'WARNING', 'INFO', 'DEBUG'],
        default='INFO',
        type=str,
        help='Log level'
    )

    # Compute
    args = parser.parse_args()

    # Logging.
    logger = logging.getLogger(name='main')
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%d-%m-%Y %H:%M'
    )
    st_handler = logging.StreamHandler()
    st_handler.setFormatter(formatter)
    logger.addHandler(st_handler)
    logger.setLevel(args.log_level)

    # Check arguments.
    if not os.path.isfile(args.input_model_file):
        logger.error(
            "Input model file doesn't exist" %
            (args.input_model_file,)
        )
        parser.exit(1)
    if args.input_pathway_file is not None \
        and not os.path.isfile(args.input_pathway_file):
        logger.error("Input pathway file doesn't exist")
        parser.exit(1)

    if not os.path.isdir(os.path.dirname(args.output_file)):
        logger.debug('Create out directory: %s')
        os.makedirs(os.path.dirname(args.output_file))

    # Init tmp file to store model
    tmpfile = tempfile.NamedTemporaryFile(delete=False)

    # Load model
    logger.info('Build model')
    if args.input_pathway_file is not None:
        res = build_model(
            model_path=args.input_model_file,
            pathway_path=args.input_pathway_file,
            output_path=tmpfile.name,
            pathway_compartment=args.input_pathway_compartment,
            main_objective=args.biomass_rxn_id,
            target_objective=args.target_rxn_id,
            logger=logger
        )
        if res == 0:
            parser.exit(1)
    else:
        shutil.copyfile(
            src=args.input_model_file,
            dst=tmpfile.name
        )

    # Medium
    logger.info('Build medium')
    medium = load_medium(
        path=args.input_medium_file
    )

    # Simulation
    logger.info('Build reference')
    flux_reference = build_flux_reference(
        model_path=tmpfile.name,
        biomass_id=args.biomass_rxn_id,
        envcond=medium,
        logger=logger
    )
    logger.info('Build gene ko')
    gene_ko(
        model_path=tmpfile.name,
        output_path=args.output_file,
        envcond=medium,
        biomass_id=args.biomass_rxn_id,
        target_id=args.target_rxn_id,
        flux_reference=flux_reference,
        logger=logger,
        thread=args.thread
    )

    # Clean up.
    os.remove(tmpfile.name)
    return 0


if __name__ == '__main__':
    sys.exit(main())
