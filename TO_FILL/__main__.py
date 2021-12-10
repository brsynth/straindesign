#!/usr/bin/env python

from logging  import error as logging_error
from TO_FILL  import TO_FILL, build_args_parser


def _cli():
    parser = build_args_parser()
    args  = parser.parse_args()

    return TO_FILL


if __name__ == '__main__':
    _cli()
