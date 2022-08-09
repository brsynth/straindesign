import logging
from collections import OrderedDict

from cameo import load_model
from main_test import Main_test
from rpfbagr.medium import associate_flux_env, load_medium


class Test_functional(Main_test):
    def test_load_medium(self):
        medium = load_medium(self.medium_butanol)
        theorical_medium = OrderedDict(
            {"EX_glc__D_e": (-10.0, 10.0), "EX_o2_e": (-5.0, 5.0)}
        )
        self.assertEqual(medium, theorical_medium)

    def test_associate_flux_env(self):
        medium = load_medium(self.medium_butanol)
        model = load_model(self.model_ecoli)
        self.assertEqual(
            model.reactions.get_by_id("EX_glc__D_e").bounds, (-8.0, 999999.0)
        )
        associate_flux_env(
            model=model,
            envcond=medium,
            logger=logging.getLogger(),
        )
        self.assertEqual(model.reactions.get_by_id("EX_glc__D_e").bounds, (-10.0, 10.0))
        self.assertEqual(model.reactions.get_by_id("EX_o2_e").bounds, (-5.0, 5.0))
