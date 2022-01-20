import logging

from main_test import Main_test
from rpfa.preprocess import (
    build_model,
)


class Test_functional(Main_test):

    def test_build_model(self):
        # Test 1
        model = build_model(
            model_path=self.model_ecoli,
            pathway_path=None,
            biomass_id='EX_glc__D_e',
            target_id='BIOMASS_Ec_iAF1260_core_59p81M',
            logger=logging.getLogger()
        )
        data = model.objective.to_json()
        self.assertEqual(
            data['expression']['args'][0]['args'][1]['name'],
            'BIOMASS_Ec_iAF1260_core_59p81M'
        )
        self.assertEqual(
            data['expression']['args'][0]['args'][0]['value'],
            0.5
        )
        self.assertEqual(
            data['expression']['args'][2]['args'][1]['name'],
            'EX_glc__D_e'
        )
        self.assertEqual(
            data['expression']['args'][2]['args'][0]['value'],
            1.0
        )
        with self.assertRaises(KeyError):
            model.reactions.get_by_id('EX_1btol_e'),
        # Test 2
        model = build_model(
            model_path=self.model_ecoli,
            pathway_path=self.pathway_butanol,
            biomass_id='BIOMASS_Ec_iAF1260_core_59p81M',
            target_id='EX_1btol_e',
            logger=logging.getLogger()
        )
        data = model.objective.to_json()
        self.assertEqual(
            data['expression']['args'][0]['args'][1]['name'],
            'BIOMASS_Ec_iAF1260_core_59p81M'
        )
        self.assertEqual(
            data['expression']['args'][0]['args'][0]['value'],
            1.0
        )
        self.assertEqual(
            data['expression']['args'][2]['args'][1]['name'],
            'EX_1btol_e'
        )
        self.assertEqual(
            data['expression']['args'][2]['args'][0]['value'],
            0.5
        )
        self.assertIsNot(
            model.reactions.get_by_id('EX_1btol_e'),
            None
        )
        # Test 3
        model = build_model(
            model_path=self.model_ecoli,
            pathway_path=self.pathway_butanol,
            biomass_id='test',
            target_id='EX_1btol_e',
            logger=logging.getLogger()
        )
        self.assertIs(
            model,
            None
        )
        # Test 4
        model = build_model(
            model_path=self.model_ecoli,
            pathway_path=self.pathway_butanol,
            biomass_id='BIOMASS_Ec_iAF1260_core_59p81M',
            target_id='test',
            logger=logging.getLogger()
        )
        self.assertIs(
            model,
            None
        )
