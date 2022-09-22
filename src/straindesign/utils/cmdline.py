import argparse
import os


def abort(parser: argparse.ArgumentParser, msg: str = ""):
    """Abort the program

    Parameters
    ----------
    parser:
        The parser to use
    msg: str
        The message to throw from the parser

    Return
    ------
    """
    parser.error(msg)


def check_output_file(
    parser: argparse.ArgumentParser, path: str, overwrite: bool = False
) -> None:
    msg = None
    if path and not os.path.isdir(os.path.dirname(os.path.abspath(path))):
        msg = "Outdir does not exists: %s" % (path,)
    if overwrite and os.path.isfile(path):
        msg = "Outdir does not exists: %s" % (path,)
    if msg:
        abort(parser=parser, msg=msg)
