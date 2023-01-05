from __future__ import absolute_import, print_function

__all__ = ["bigg2mnx", "mnx2bigg", "all2mnx", "mnx2all"]

import gzip
import json
import os

import pandas

import cameobrs

with gzip.open(os.path.join(cameobrs._cameo_data_path, "metanetx.json.gz"), "rt") as f:
    _METANETX = json.load(f)

bigg2mnx = _METANETX["bigg2mnx"]
mnx2bigg = _METANETX["mnx2bigg"]
all2mnx = _METANETX["all2mnx"]
mnx2all = {v: k for k, v in all2mnx.items()}

with gzip.open(
    os.path.join(cameobrs._cameo_data_path, "metanetx_chem_prop.json.gz"), "rt"
) as f:
    chem_prop = pandas.read_json(f)
