import argparse
import logging
import os
import sys

from straindesign._version import __app_name__
from straindesign.medium import associate_flux_env, load_medium
from straindesign.metabolic import gene_ko, gene_ou
from straindesign.preprocess import build_model, genes_annotate, save_results


def main():
    """CLI for StrainDesign"""

    desc = (
        __app_name__
        + " provides a cli interface to run OptGene with an heterologous pathway."
    )
    parser = argparse.ArgumentParser(description=desc, prog="python -m " + __app_name__)
    # Input
    parser_input = parser.add_argument_group("Input")
    parser_input.add_argument(
        "--input-model-file", type=str, required=True, help="GEM model file (SBML)"
    )
    parser_input.add_argument(
        "--input-pathway-file",
        type=str,
        required=False,
        help="SBML file that contains an heterologous pathway",
    )
    parser_input.add_argument(
        "--biomass-rxn-id",
        type=str,
        required=True,
        help="Biomass reaction ID",
    )
    parser_input.add_argument(
        "--target-rxn-id",
        type=str,
        required=False,
        help="Target reaction ID",
    )
    parser_input.add_argument(
        "--substrate-rxn-id",
        type=str,
        required=False,
        help="Substracte reaction ID (eg. carbon source)",
    )

    # Output
    parser_output = parser.add_argument_group("Output")
    parser_output.add_argument(
        "--output-file-csv",
        type=str,
        help="output file (csv)",
    )
    parser_output.add_argument(
        "--output-file-tsv",
        type=str,
        help="output file (tsv)",
    )

    # Simulation
    parser_sim = parser.add_argument_group("Simulation")
    parser_sim.add_argument(
        "--strategy",
        type=str,
        choices=["ko", "ou"],
        default="ko",
        help="Strategy to use : ko (knocking out) or ou "
        "(over-under expressing), (default: ko)",
    )
    parser_input.add_argument(
        "--max-knockouts",
        type=int,
        default=3,
        required=False,
        help="Number of maximum knockouts genes allowed",
    )

    # Medium
    parser_medium = parser.add_argument_group("Medium")
    parser_medium.add_argument(
        "--input-medium-file",
        type=str,
        help="Provide a csv or tsv file with an header as <coumpond_id>,"
        "<lower_bound>, <upper_bound>. This file "
        "provides information about metabolites (Metanetx Id) "
        "to add or remove.",
    )
    # Others.
    parser_helper = parser.add_argument_group("Technical")
    parser_helper.add_argument(
        "--thread",
        type=int,
        default=1,
        help="Number of threads to use",
    )
    parser_helper.add_argument(
        "--seed",
        type=int,
        default=0,
        help="Seed",
    )
    parser_helper.add_argument(
        "--max-time",
        type=int,
        help="Max time to search the best combination (minutes)",
    )

    parser_helper.add_argument(
        "--log-level",
        choices=["ERROR", "WARNING", "INFO", "DEBUG"],
        default="INFO",
        type=str,
        help="Log level",
    )
    parser_input.add_argument(
        "--email",
        type=str,
        required=False,
        help="Provide your email to annotate genes id with the NCBI website",
    )

    # Compute
    args = parser.parse_args()

    # Logging.
    logger = logging.getLogger(name="main")
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", datefmt="%d-%m-%Y %H:%M"
    )
    st_handler = logging.StreamHandler()
    st_handler.setFormatter(formatter)
    logger.addHandler(st_handler)
    logger.setLevel(args.log_level)

    # Check arguments.
    if not os.path.isfile(args.input_model_file):
        logger.error('Input model file doesn"t exist: %s' % (args.input_model_file,))
        parser.exit(1)
    if args.input_pathway_file is not None and not os.path.isfile(
        args.input_pathway_file
    ):
        logger.error('Input pathway file doesn"t exist')
        parser.exit(1)

    if args.output_file_csv and not os.path.isdir(
        os.path.dirname(args.output_file_csv)
    ):
        logger.debug("Create out directory: %s")
        os.makedirs(os.path.dirname(args.output_file_csv))
    if args.output_file_tsv and not os.path.isdir(
        os.path.dirname(args.output_file_tsv)
    ):
        logger.debug("Create out directory: %s")
        os.makedirs(os.path.dirname(args.output_file_tsv))

    # Load model
    logger.info("Build model")
    model = build_model(
        model_path=args.input_model_file,
        pathway_path=args.input_pathway_file,
        biomass_id=args.biomass_rxn_id,
        target_id=args.target_rxn_id,
        logger=logger,
    )
    if model is None:
        parser.exit(1)

    # Medium
    logger.info("Build medium")
    envcond = load_medium(path=args.input_medium_file)
    model = associate_flux_env(model=model, envcond=envcond, logger=logger)
    if model is None:
        parser.exit(1)

    # Simulation
    logger.info("Build gene ko")
    res = None
    if args.strategy == "ko":
        logger.info("Run OptGene")
        res = gene_ko(
            model=model,
            max_knockouts=args.max_knockouts,
            biomass_id=args.biomass_rxn_id,
            target_id=args.target_rxn_id,
            substrate_id=args.substrate_rxn_id,
            max_time=args.max_time,
            logger=logger,
            seed=args.seed,
            thread=args.thread,
        )
    elif args.strategy == "ou":
        logger.info("Run OptKnock")
        if args.substrate_rxn_id:
            logger.warning("Substrate reaction will be ignored with OptKnock")
        if args.seed:
            logger.warning("Seed will be ignored with OptKnock")
        res = gene_ou(
            model=model,
            max_knockouts=args.max_knockouts,
            biomass_id=args.biomass_rxn_id,
            target_id=args.target_rxn_id,
            max_time=args.max_time,
            logger=logger,
            thread=args.thread,
        )

    # Processing Results
    if res is not None:
        if args.email and args.strategy == "ko":
            logger.info("Perform gene annotation")
            res = genes_annotate(model=model, df=res, email=args.email, logger=logger)
        logger.info("Save results")
        if args.output_file_csv:
            save_results(res, path=args.output_file_csv, sep=",")
        if args.output_file_tsv:
            save_results(res, path=args.output_file_tsv, sep="\t")

    return 0


if __name__ == "__main__":
    sys.exit(main())
