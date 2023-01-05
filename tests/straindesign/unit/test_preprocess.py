from straindesign.preprocess import (
    build_model,
    load_straindesign_simulate_deletion,
)
from tests.straindesign.main_test import Main_test


class TestPreprocess(Main_test):
    def test_load_straindesign_simulate_deletion(self):
        # Test 1
        genes = load_straindesign_simulate_deletion(
            path=self.gene_butanol, strategy="yield-max"
        )
        self.assertEqual(genes, ["b0529", "b3919"])
        # Test 2
        genes = load_straindesign_simulate_deletion(
            path=self.gene_butanol, strategy="gene-max"
        )
        self.assertEqual(genes, ["b3731", "b3732", "b3734", "b3735", "b3736"])
        # Test 3
        genes = load_straindesign_simulate_deletion(
            path=self.gene_butanol, strategy="gene-min"
        )
        self.assertEqual(genes, ["b3919"])
        # Test 4
        genes = load_straindesign_simulate_deletion(
            path=self.gene_empty, strategy="gene-min"
        )
        self.assertEqual(genes, [])
        # Test 5
        with self.assertRaises(ValueError):
            load_straindesign_simulate_deletion(
                path=self.gene_value_error, strategy="gene-min"
            )

    def test_build_model(self):
        # Test 1
        model = build_model(
            model_path=self.model_ecoli,
            pathway_path=None,
            biomass_id="EX_glc__D_e",
            target_id="BIOMASS_Ec_iAF1260_core_59p81M",
        )
        data = model.objective.to_json()
        b_ix, t_ix = 0, 0
        for ix, arg in enumerate(data["expression"]["args"]):
            if arg["args"][1]["name"] == "BIOMASS_Ec_iAF1260_core_59p81M":
                b_ix = ix
            if arg["args"][1]["name"] == "EX_glc__D_e":
                t_ix = ix
        self.assertEqual(data["expression"]["args"][b_ix]["args"][0]["value"], 0.5)
        self.assertEqual(data["expression"]["args"][t_ix]["args"][0]["value"], 1.0)
        with self.assertRaises(KeyError):
            model.reactions.get_by_id("EX_1btol_e"),
        # Test 2
        model = build_model(
            model_path=self.model_ecoli,
            pathway_path=self.pathway_butanol,
            biomass_id="BIOMASS_Ec_iAF1260_core_59p81M",
            target_id="EX_1btol_e",
        )
        data = model.objective.to_json()
        b_ix, t_ix = 0, 0
        for ix, arg in enumerate(data["expression"]["args"]):
            if arg["args"][1]["name"] == "BIOMASS_Ec_iAF1260_core_59p81M":
                b_ix = ix
            if arg["args"][1]["name"] == "EX_1btol_e":
                t_ix = ix
        self.assertEqual(data["expression"]["args"][b_ix]["args"][0]["value"], 1.0)
        self.assertEqual(data["expression"]["args"][t_ix]["args"][0]["value"], 0.5)
        self.assertIsNot(model.reactions.get_by_id("EX_1btol_e"), None)
        # Test 3
        model = build_model(
            model_path=self.model_ecoli,
            pathway_path=self.pathway_butanol,
            biomass_id="test",
            target_id="EX_1btol_e",
        )
        self.assertIs(model, None)
        # Test 4
        model = build_model(
            model_path=self.model_ecoli,
            pathway_path=self.pathway_butanol,
            biomass_id="BIOMASS_Ec_iAF1260_core_59p81M",
            target_id="test",
        )
        self.assertIs(model, None)
