import argparse
import logging
import os
import sys

from straindesign._version import __app_name__, __version__
from straindesign.medium import associate_flux_env, load_medium
from straindesign.metabolic import gene_ko, gene_ou
from straindesign.preprocess import build_model, genes_annotate, save_results
from straindesign.utils import cmdline, log

AP = argparse.ArgumentParser(
    description=__app_name__ + " provides a cli interface to predict gene knockout "
    "targets with an heterologous pathway",
    epilog="See online documentation: https://github.com/brsynth/straindesign",
)
AP_subparsers = AP.add_subparsers(help="Sub-commnands (use with -h for more info)")


def _cmd_sim_del(args):
    """Build plan of experiment for BASIC protocol"""
    logging.info("Start - simulate-deletion")
    # Check arguments.
    if not os.path.isfile(args.input_model_file):
        logging.error('Input model file doesn"t exist: %s' % (args.input_model_file,))
        parser.exit(1)
    if args.input_pathway_file is not None and not os.path.isfile(
        args.input_pathway_file
    ):
        logging.error('Input pathway file doesn"t exist')
        parser.exit(1)

    if args.output_file_csv and not os.path.isdir(
        os.path.dirname(args.output_file_csv)
    ):
        logging.debug("Create out directory: %s")
        os.makedirs(os.path.dirname(args.output_file_csv))
    if args.output_file_tsv and not os.path.isdir(
        os.path.dirname(args.output_file_tsv)
    ):
        logging.debug("Create out directory: %s")
        os.makedirs(os.path.dirname(args.output_file_tsv))

    # Load model
    logging.info("Build model")
    model = build_model(
        model_path=args.input_model_file,
        pathway_path=args.input_pathway_file,
        biomass_id=args.biomass_rxn_id,
        target_id=args.target_rxn_id,
    )
    if model is None:
        parser.exit(1)

    # Medium
    logging.info("Build medium")
    envcond = load_medium(path=args.input_medium_file)
    model = associate_flux_env(model=model, envcond=envcond)
    if model is None:
        parser.exit(1)

    # Simulation
    logging.info("Build gene ko")
    res = None
    if args.strategy == "ko":
        logging.info("Run OptGene")
        res = gene_ko(
            model=model,
            max_knockouts=args.max_knockouts,
            biomass_id=args.biomass_rxn_id,
            target_id=args.target_rxn_id,
            substrate_id=args.substrate_rxn_id,
            max_time=args.max_time,
            seed=args.seed,
            thread=args.thread,
        )
    elif args.strategy == "ou":
        logging.info("Run OptKnock")
        if args.substrate_rxn_id:
            logging.warning("Substrate reaction will be ignored with OptKnock")
        if args.seed:
            logging.warning("Seed will be ignored with OptKnock")
        res = gene_ou(
            model=model,
            max_knockouts=args.max_knockouts,
            biomass_id=args.biomass_rxn_id,
            target_id=args.target_rxn_id,
            max_time=args.max_time,
            thread=args.thread,
        )

    # Processing Results
    if res is not None:
        if args.email and args.strategy == "ko":
            logging.info("Perform gene annotation")
            res = genes_annotate(model=model, df=res, email=args.email)
        logging.info("Save results")
        if args.output_file_csv:
            save_results(res, path=args.output_file_csv, sep=",")
        if args.output_file_tsv:
            save_results(res, path=args.output_file_tsv, sep="\t")

    logging.info("End - simulate-deletion")


P_sim_del = AP_subparsers.add_parser("simulate-deletion", help=_cmd_sim_del.__doc__)
# Input
P_sim_del_input = P_sim_del.add_argument_group("Input")
P_sim_del_input.add_argument(
    "--input-model-file", type=str, required=True, help="GEM model file (SBML)"
)
P_sim_del_input.add_argument(
    "--input-pathway-file",
    type=str,
    required=False,
    help="SBML file that contains an heterologous pathway",
)
P_sim_del_input.add_argument(
    "--biomass-rxn-id",
    type=str,
    required=True,
    help="Biomass reaction ID",
)
P_sim_del_input.add_argument(
    "--target-rxn-id",
    type=str,
    help="Target reaction ID",
)
P_sim_del_input.add_argument(
    "--substrate-rxn-id",
    type=str,
    help="Substracte reaction ID (eg. carbon source)",
)
# Output
P_sim_del_output = P_sim_del.add_argument_group("Output")
P_sim_del_output.add_argument(
    "--output-file-csv",
    type=str,
    help="output file (csv)",
)
P_sim_del_output.add_argument(
    "--output-file-tsv",
    type=str,
    help="output file (tsv)",
)
# Parameters - Simulation
P_sim_del_sim = P_sim_del.add_argument_group("Simulation")
P_sim_del_sim.add_argument(
    "--strategy",
    type=str,
    choices=["ko", "ou"],
    default="ko",
    help="Strategy to use : ko (knocking out) or ou "
    "(over-under expressing), (default: ko)",
)
P_sim_del_sim.add_argument(
    "--max-knockouts",
    type=int,
    default=3,
    required=False,
    help="Number of maximum knockouts genes allowed",
)
# Parameters - Medium
P_sim_del_medium = P_sim_del.add_argument_group("Medium")
P_sim_del_medium.add_argument(
    "--input-medium-file",
    type=str,
    help="Provide a csv or tsv file with an header as <coumpond_id>,"
    "<lower_bound>, <upper_bound>. This file "
    "provides information about metabolites (Metanetx Id) "
    "to add or remove.",
)
# Parameters - Others.
P_sim_del_helper = P_sim_del.add_argument_group("Technical")
P_sim_del_helper.add_argument(
    "--thread",
    type=int,
    default=1,
    help="Number of threads to use",
)
P_sim_del_helper.add_argument(
    "--seed",
    type=int,
    default=0,
    help="Seed",
)
P_sim_del_helper.add_argument(
    "--max-time",
    type=int,
    help="Max time to search the best combination (minutes)",
)
P_sim_del_helper.add_argument(
    "--email",
    type=str,
    required=False,
    help="Provide your email to annotate genes id with the NCBI website",
)
P_sim_del.set_defaults(func=_cmd_sim_del)


# Version.
def print_version(_args):
    """Display this program"s version"""
    print(__version__)


P_version = AP_subparsers.add_parser("version", help=print_version.__doc__)
P_version.set_defaults(func=print_version)


# Help.
def print_help():
    """Display this program"s help"""
    print(AP_subparsers.help)
    AP.exit()


# Main.
def parse_args(args=None):
    """Parse the command line"""
    return AP.parse_args(args=args)


if __name__ == "__main__":
    sys.exit(main())
