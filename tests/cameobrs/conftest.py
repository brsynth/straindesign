import os
import pytest

import cobra
import pandas as pd
from cameobrs import load_model
from cameobrs.config import solvers

cur_dir = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(cur_dir, "data")


@pytest.fixture(scope="session")
def data_directory():
    return data_dir


@pytest.fixture(scope="session")
def model(data_directory):
    m = load_model(os.path.join(data_directory, "EcoliCore.xml"))
    m.solver = "glpk"
    return m


@pytest.fixture(scope="session")
def ecore_path(data_directory):
    return os.path.join(data_directory, "EcoliCore.xml")


@pytest.fixture(scope="session")
def salmonella(data_directory):
    return load_model(os.path.join(data_directory, "iYS1720.xml"))


@pytest.fixture(scope="session", params=list(solvers))
def ijo1366(request, data_directory):
    ijo = load_model(os.path.join(data_directory, "iJO1366.xml"), sanitize=False)
    ijo.solver = request.param
    return ijo


@pytest.fixture(scope="session", params=list(solvers))
def ijo1366_path(request, data_directory):
    return os.path.join(data_directory, "iJO1366.xml")


@pytest.fixture(scope="session")
def iaf1260(data_directory):
    return load_model(os.path.join(data_directory, "iAF1260.xml"))


@pytest.fixture(scope="session")
def universal_model(data_directory):
    universal = load_model(os.path.join(data_directory, "iJO1366.xml"), sanitize=False)
    universal.remove_reactions(universal.boundary)
    return universal


@pytest.fixture(scope="session", params=list(solvers))
def imm904(request, data_directory):
    imm = load_model(os.path.join(data_directory, "iMM904.xml"))
    imm.solver = request.param
    return imm.copy()


# FIXME: should be possible to scope at least to class
@pytest.fixture(scope="function", params=list(solvers))
def toy_model(request, data_directory):
    toy = load_model(os.path.join(data_directory, "toy_model_Papin_2003.xml"))
    toy.solver = request.param
    return toy


# FIXME: should be possible to scope at least to class
@pytest.fixture(scope="function", params=list(solvers))
def core_model(request, data_directory):
    ecoli_core = load_model(
        os.path.join(data_directory, "EcoliCore.xml"), sanitize=False
    )
    ecoli_core.solver = request.param
    return ecoli_core


@pytest.fixture(scope="session")
def ref_fva(data_directory):
    # REFERENCE_FVA_SOLUTION_ECOLI_CORE
    return pd.read_csv(
        os.path.join(data_directory, "REFERENCE_flux_ranges_EcoliCore.csv"),
        index_col=0,
    )


@pytest.fixture(scope="session")
def ref_ecore(data_directory):
    # REFERENCE_PPP_o2_EcoliCore
    return pd.read_csv(os.path.join(data_directory, "REFERENCE_PPP_o2_EcoliCore.csv"))


@pytest.fixture(scope="session")
def ref_ecore_ac(data_directory):
    # REFERENCE_PPP_o2_EcoliCore_ac
    return pd.read_csv(
        os.path.join(data_directory, "REFERENCE_PPP_o2_EcoliCore_ac.csv")
    )


@pytest.fixture(scope="session")
def ref_ecore_glc(data_directory):
    # REFERENCE_PPP_o2_glc_EcoliCore
    return pd.read_csv(
        os.path.join(data_directory, "REFERENCE_PPP_o2_glc_EcoliCore.csv")
    )


@pytest.fixture(scope="session")
def fix_size_candidates(data_directory):
    return os.path.join(data_directory, "fix_size_candidates.pkl")


@pytest.fixture(scope="session")
def variable_size_candidates(data_directory):
    return os.path.join(data_directory, "variable_size_candidates.pkl")


@pytest.fixture(scope="session")
def ref_diffva1(data_directory):
    return os.path.join(data_directory, "REFERENCE_DiffFVA1.csv")


@pytest.fixture(scope="session")
def ref_diffva2(data_directory):
    return os.path.join(data_directory, "REFERENCE_DiffFVA2.csv")
