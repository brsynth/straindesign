import logging
import sys

from straindesign import commands


def main():
    """Entrypoint to commandline"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%d-%m-%Y %H:%M",
    )
    args = commands.parse_args()
    # No arguments or subcommands were given.
    if len(args.__dict__) < 1:
        commands.print_help()
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())
