from __future__ import absolute_import, print_function

import os

import pandas as pd
import pytest
from cobra.exceptions import OptimizationError
from pandas import DataFrame

import cameobrs
from cameobrs.config import solvers
from cameobrs.strain_design.deterministic.flux_variability_based import (
    FSEOF,
    DifferentialFVA,
    FSEOFResult,
)
from cameobrs.strain_design.deterministic.linear_programming import (
    GrowthCouplingPotential,
    OptKnock,
)

CI = bool(os.getenv("CI", False))
TESTDIR = os.path.dirname(__file__)


@pytest.fixture(scope="module")
def cplex_optknock(model):
    cplex_core = model.copy()
    cplex_core.reactions.Biomass_Ecoli_core_N_lp_w_fsh_GAM_rp__Nmet2.lower_bound = 0.1
    cplex_core.solver = "cplex"
    return cplex_core, OptKnock(cplex_core)


@pytest.fixture(scope="module")
def diff_fva(model):
    return DifferentialFVA(model, model.reactions.EX_succ_lp_e_rp_, points=5)


@pytest.fixture(scope="module")
def glpk_growth_coupling_potential(model):
    glpk_core = model.copy()
    glpk_core.solver = "glpk"
    glpk_core.reactions.ATPM.knock_out()
    knockout_reactions = [r.id for r in glpk_core.reactions if r.genes]
    return glpk_core, GrowthCouplingPotential(
        glpk_core,
        target="PFL",
        knockout_reactions=knockout_reactions,
        biomass_id="Biomass_Ecoli_core_N_lp_w_fsh_GAM_rp__Nmet2",
        knockin_reactions=[],
        medium_additions=[],
        n_knockouts=1,
        n_knockin=0,
        n_medium=0,
    )


class TestFSEOF:
    def test_fseof(self, model):
        objective = model.objective
        fseof = FSEOF(model)
        fseof_result = fseof.run(target="EX_succ_lp_e_rp_")
        assert isinstance(fseof_result, FSEOFResult)
        assert objective.expression == model.objective.expression

    def test_fseof_result(self, model):
        fseof = FSEOF(model)
        fseof_result = fseof.run(target=model.reactions.EX_ac_lp_e_rp_)
        assert isinstance(fseof_result.data_frame, DataFrame)
        assert fseof_result.target is model.reactions.EX_ac_lp_e_rp_
        assert fseof_result.model is model


class TestDifferentialFVA:
    def test_minimal_input(self, diff_fva, ref_diffva1):
        result = diff_fva.run()
        ref_df = pd.read_csv(ref_diffva1, index_col=0)
        ref_df.sort_index(inplace=True)
        this_df = result.nth_panel(0)
        this_df.index.name = None
        this_df.sort_index(inplace=True)
        pd.testing.assert_frame_equal(
            this_df[ref_df.columns],
            ref_df,
            check_exact=False,
            rtol=1e-2,  # Number of digits for equality check.
        )

    def test_apply_designs(self, model, diff_fva):
        result = diff_fva.run()
        works = []
        for strain_design in result:
            with model:
                strain_design.apply(model)
                try:
                    solution = model.optimize(raise_error=True)
                    works.append(
                        solution["EX_succ_lp_e_rp_"] > 1e-6
                        and solution.objective_value > 1e-6
                    )
                except OptimizationError:
                    works.append(False)
        assert any(works)

    def test_diff_fva_benchmark(self, diff_fva, benchmark):
        benchmark(diff_fva.run)

    def test_with_reference_model(self, model, ref_diffva2):
        reference_model = model.copy()
        biomass_rxn = (
            reference_model.reactions.Biomass_Ecoli_core_N_lp_w_fsh_GAM_rp__Nmet2
        )
        biomass_rxn.lower_bound = 0.3
        target = reference_model.reactions.EX_succ_lp_e_rp_
        target.lower_bound = 2
        result = DifferentialFVA(
            model, target, reference_model=reference_model, points=5
        ).run()
        ref_df = pd.read_csv(ref_diffva2, index_col=0)
        ref_df.sort_index(inplace=True)
        this_df = result.nth_panel(0)
        this_df.index.name = None
        this_df.sort_index(inplace=True)
        pd.testing.assert_frame_equal(
            this_df[ref_df.columns],
            ref_df,
            check_exact=False,
            rtol=1e-2,  # Number of digits for equality check.
        )


@pytest.mark.skipif("cplex" not in solvers, reason="No cplex interface available")
class TestOptKnock:
    def test_optknock_runs(self, cplex_optknock):
        _, optknock = cplex_optknock
        result = optknock.run(
            max_knockouts=0,
            target="EX_ac_lp_e_rp_",
            biomass="Biomass_Ecoli_core_N_lp_w_fsh_GAM_rp__Nmet2",
            max_results=1,
        )
        assert len(result) == 1
        assert len(result.knockouts[0]) == 0
        assert len(list(result)) == 1
        assert isinstance(result.data_frame, DataFrame)

    def test_optknock_benchmark(self, cplex_optknock, benchmark):
        _, optknock = cplex_optknock
        benchmark(
            optknock.run,
            max_knockouts=2,
            target="EX_ac_lp_e_rp_",
            biomass="Biomass_Ecoli_core_N_lp_w_fsh_GAM_rp__Nmet2",
            max_results=1,
        )

    def test_result_is_correct(self, cplex_optknock):
        model, optknock = cplex_optknock
        result = optknock.run(
            max_knockouts=1,
            target="EX_ac_lp_e_rp_",
            biomass="Biomass_Ecoli_core_N_lp_w_fsh_GAM_rp__Nmet2",
            max_results=1,
        )
        production = result.production[0]
        knockouts = result.knockouts[0]
        for knockout in knockouts:
            model.reactions.get_by_id(knockout).knock_out()
        fva = cameobrs.flux_variability_analysis(
            model,
            fraction_of_optimum=1,
            remove_cycles=False,
            reactions=["EX_ac_lp_e_rp_"],
        )
        assert abs(fva["upper_bound"][0] - production) < 1e-6

    def test_invalid_input(self, cplex_optknock):
        _, optknock = cplex_optknock
        with pytest.raises(ValueError):
            optknock.run(target="EX_ac_lp_e_rp_")
        with pytest.raises(ValueError):
            optknock.run(biomass="Biomass_Ecoli_core_N_lp_w_fsh_GAM_rp__Nmet2")


# @pytest.mark.skipif('gurobi' not in solvers, reason="No gurobi interface available")
class TestGrowthCouplingPotential:
    def test_growth_coupling_potential_runs(self, glpk_growth_coupling_potential):
        _, growth_coupling_potential = glpk_growth_coupling_potential
        result = growth_coupling_potential.run()
        assert "obj_val" in result
        assert "knockouts" in result
        assert "knockins" in result
        assert "medium" in result

    @pytest.mark.skip()
    def test_growth_coupling_potential_benchmark(
        self, glpk_growth_coupling_potential, benchmark
    ):
        _, growth_coupling_potential = glpk_growth_coupling_potential
        benchmark(growth_coupling_potential.run)

    def test_result_is_correct(self, glpk_growth_coupling_potential):
        model, growth_coupling_potential = glpk_growth_coupling_potential
        result = growth_coupling_potential.run()

        knockouts = result["knockouts"]
        fva = cameobrs.flux_variability_analysis(
            model, fraction_of_optimum=1, remove_cycles=False, reactions=["PFL"]
        )
        assert fva["lower_bound"][0] <= 0 <= fva["upper_bound"][0]
        with model:
            for knockout in knockouts:
                model.reactions.get_by_id(knockout).knock_out()
            fva = cameobrs.flux_variability_analysis(
                model, fraction_of_optimum=1, remove_cycles=False, reactions=["PFL"]
            )
            assert abs(fva["lower_bound"][0]) > 4
