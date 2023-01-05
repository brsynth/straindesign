from __future__ import absolute_import

import glob
import os
import sys
import types
from functools import partial

from lazy_object_proxy import Proxy

import cameobrs
from cameobrs import util
from cameobrs.io import load_model

__all__ = ["universal"]


class ModelDB(object):
    pass


universal = ModelDB()

for file_path in glob.glob(
    os.path.join(
        os.path.dirname(cameobrs.__file__), "models", "universal_models", "*.json"
    )
):
    model_id = os.path.splitext(os.path.basename(file_path))[0]
    setattr(
        universal,
        util.str_to_valid_variable_name(model_id),
        Proxy(partial(load_model, file_path)),
    )

# sys.modules[__name__] = universal
