"""This package implement the high-level user interface of cameo.

Examples
--------
Compute strain designs for the target product vanillin.
    $ api.design(product='vanillin')

Search in the list of available target products.
    $ api.products.search('vanillin')

The available host organism models for E. coli.
    $ api.hosts.ecoli.models
"""

from __future__ import absolute_import

import logging

logger = logging.getLogger(__name__)

from cameobrs.api.designer import *
from cameobrs.api.hosts import *
from cameobrs.api.products import *
