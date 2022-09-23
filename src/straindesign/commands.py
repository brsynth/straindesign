import argparse
import logging
import os

from straindesign._version import __app_name__, __version__
from straindesign.io import sbml
from straindesign.medium import associate_flux_env, load_medium
from straindesign.metabolic import gene_ko, gene_ou, reduce_model
from straindesign.preprocess import (
    build_model,
    genes_annotate,
    load_straindesign_simulate_deletion,
    save_results,
)
from straindesign.utils import cmdline

AP = argparse.ArgumentParser(
    description=__app_name__ + " provides a cli interface to predict gene knockout "
    "targets with an heterologous pathway",
    epilog="See online documentation: https://github.com/brsynth/" + __app_name__,
)
AP_subparsers = AP.add_subparsers(help="Sub-commnands (use with -h for more info)")


def _cmd_red_mod(args):
    logging.info("Start - reduce-model")
    # Check arguments.
    if not os.path.isfile(args.input_model_file):
        cmdline.abort(
            AP, "Input model file does not exist: %s" % (args.input_model_file,)
        )
    if args.input_straindesign_file and not os.path.isfile(
        args.input_straindesign_file
    ):
        cmdline.abort(
            AP,
            "Input %s file does not exist: %s"
            % (__app_name__, args.input_straindesign_file),
        )
    if args.input_straindesign_file is None and args.input_gene_str is None:
        cmdline.abort(
            AP,
            "Provide at least --input-straindesign-file or --input-genes-str to have genes to delete in the model",
        )
    cmdline.check_output_file(parser=AP, path=args.output_file_sbml)

    # Load model.
    logging.info("Load model")
    model = sbml.from_sbml(path=args.input_model_file)

    # Load genes.
    logging.info("Load genes")
    genes = []
    if args.input_straindesign_file:
        genes.extend(
            load_straindesign_simulate_deletion(
                path=args.input_straindesign_file, strategy=args.parameter_strategy_str
            )
        )
    if args.input_gene_str:
        genes.extend(args.input_gene_str)
    genes = list(set(genes))
    if len(genes) < 1:
        cmdline.abort(AP, "No genes are provided to be deleted into the model")

    # Remove genes in the model.
    logging.info("Remove genes in the model")
    logging.info("Genes to remove from the model are: %s" % (", ".join(genes)))
    model = reduce_model(model=model, genes=genes)

    # Save model
    logging.info("Write the model")
    sbml.to_sbml(model=model, path=args.output_file_sbml)

    logging.info("End - reduce-model")


P_red_mod = AP_subparsers.add_parser("reduce-model", help=_cmd_red_mod.__doc__)
# Input
P_red_mod_input = P_red_mod.add_argument_group("Input")
P_red_mod_input.add_argument(
    "--input-model-file", type=str, required=True, help="GEM model file (SBML)"
)
P_red_mod_input.add_argument(
    "--input-straindesign-file",
    type=str,
    help="CSV file produced by the command " + __app_name__ + " simulate-deletion",
)
P_red_mod_input.add_argument(
    "--input-gene-str",
    nargs="+",
    help="Gene ids to delete in the model",
)
# Output
P_red_mod_output = P_red_mod.add_argument_group("Output")
P_red_mod_output.add_argument(
    "--output-file-sbml",
    type=str,
    required=True,
    help="Model output file (SBML)",
)
# Parameters
P_red_mod_params = P_red_mod.add_argument_group("Parameters")
P_red_mod_params.add_argument(
    "--parameter-strategy-str",
    type=str,
    choices=["yield-max", "gene-max", "gene-min"],
    default="yield-max",
    help="Strategy to use when genes are provided from the args: "
    "yiel-max keeps the maximal yield, gene-max keeps the first association of genes combining "
    "the biggest number of genes, gene-min keeps the first association of genes combinning the "
    "lowest number of genes",
)
P_red_mod.set_defaults(func=_cmd_red_mod)


def _cmd_sim_del(args):
    """Build plan of experiment for BASIC protocol"""
    logging.info("Start - simulate-deletion")
    # Check arguments.
    if not os.path.isfile(args.input_model_file):
        cmdline.abort(
            AP, "Input model file does not exist: %s" % (args.input_model_file,)
        )
    if args.input_pathway_file is not None and not os.path.isfile(
        args.input_pathway_file
    ):
        cmdline.abort(AP, "Input pathway file does not exist")
    if args.output_file_csv and not os.path.isdir(
        os.path.dirname(args.output_file_csv)
    ):
        os.makedirs(os.path.dirname(args.output_file_csv))
    if args.output_file_tsv and not os.path.isdir(
        os.path.dirname(args.output_file_tsv)
    ):
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
        cmdline.abort(AP, "An error occured when the model was loaded")

    # Medium
    logging.info("Build medium")
    envcond = load_medium(path=args.input_medium_file)
    model = associate_flux_env(model=model, envcond=envcond)
    if model is None:
        cmdline.abort(AP, "An error occured when the pathway was merged to the model")

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


# Analyzing model
def _cmd_ana_mod(args):
    """Analyzing model"""
    logging.info("Start - analyzing-model")
    # Check arguments.
    if not os.path.isfile(args.input_model_file):
        cmdline.abort(
            AP, "Input model file does not exist: %s" % (args.input_model_file,)
        )
    cmdline.check_output_file(parser=AP, path=args.output_pareto_png)

    # Load model.
    model = sbml.from_sbml(path=args.input_model_file)

    # Medium.
    logging.info("Build medium")
    envcond = load_medium(path=args.input_medium_file)
    model = associate_flux_env(model=model, envcond=envcond)
    if model is None:
        cmdline.abort(AP, "An error occured when the pathway was merged to the model")

    # Check reactions.
    for rxn in [args.biomass_rxn_id, args.target_rxn_id]:
        if utils_model(model=model, reaction=rxn):
            cmdline.abort(AP, "Reaction is not found in the model: %s" % (rxn,))

    # Build pareto.

    "--biomass-rxn-id",
    "--target-rxn-id",
    "--output-pareto-png",

    logging.info("End - analysing-model")


P_ana_mod = AP_subparsers.add_parser("analyzing-model", help=_cmd_ana_mod.__doc__)
# Input
P_ana_mod_input = P_ana_mod.add_argument_group("Input")
P_ana_mod_input.add_argument(
    "--input-model-file", type=str, required=True, help="GEM model file (SBML)"
)
P_ana_mod_input.add_argument(
    "--biomass-rxn-id",
    type=str,
    required=True,
    help="Biomass reaction ID",
)
P_ana_mod_input.add_argument(
    "--target-rxn-id",
    type=str,
    help="Target reaction ID",
)
# Output
P_ana_mod_output = P_ana_mod.add_argument_group("Output")
P_ana_mod_output.add_argument(
    "--output-pareto-png",
    type=str,
    help="Output pareto file (PNG)",
)
# Parameters - Medium
P_ana_mod_medium = P_ana_mod.add_argument_group("Medium")
P_ana_mod_medium.add_argument(
    "--input-medium-file",
    type=str,
    help="Provide a csv or tsv file with an header as <coumpond_id>,"
    "<lower_bound>, <upper_bound>. This file "
    "provides information about metabolites (Metanetx Id) "
    "to add or remove.",
)
P_ana_mod.set_defaults(func=_cmd_ana_mod)

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
