from __future__ import absolute_import, print_function

import os

import cobra
import pytest

import cameobrs
from cameobrs import load_model
from cameobrs.config import solvers

try:
    import libsbml
except ImportError:
    libsbml = None

TESTDIR = os.path.dirname(__file__)


@pytest.fixture(scope="module", params=list(solvers))
def solver_interface(request):
    return solvers[request.param]


class TestModelLoading(object):
    def test_load_model_sbml_path(self, solver_interface, ijo1366_path):
        model = load_model(ijo1366_path, solver_interface=solver_interface)
        assert abs(model.slim_optimize() - 0.9823718127269768) < 10e-6

    def test_load_model_sbml_handle(self, solver_interface, ijo1366_path):
        with open(ijo1366_path) as handle:
            model = load_model(handle, solver_interface=solver_interface)
        assert abs(model.slim_optimize() - 0.9823718127269768) < 10e-6

    def test_load_model_sbml_path_set_none_interface(self, ecore_path):
        model = load_model(ecore_path, solver_interface=None)
        assert abs(model.slim_optimize() - 0.8739215069684306) < 10e-6
        assert isinstance(model, cobra.Model)

    def test_import_model_bigg(self):
        model = cameobrs.models.bigg.e_coli_core
        assert model.id == "e_coli_core"

    @pytest.mark.skipif(
        libsbml is None, reason="minho has fbc < 2, requiring missing lisbml"
    )
    def test_import_model_minho(self):
        model = cameobrs.models.minho
        if model.status != "indexed":
            pytest.skip("failed to index minho db")
        assert model.__getattr__("Ecoli core Model").id == "Ecoli_core_model"

    def test_invalid_path(self):
        with pytest.raises(Exception):
            load_model("blablabla_model")
