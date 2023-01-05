"""This sub-package provides access (an function internet connection is needed
to models available on the BiGG database (http://bigg.ucsd.edu) and a model repository
hosted by the University of Minho (http://optflux.org/models).
Furthermore, it provides universal reaction database models compiled from different
sources (KEGG, RHEA, BIGG, BRENDA) and that have been obtained from http://metanetx.org"""

from .universal import *
from .webmodels import *
