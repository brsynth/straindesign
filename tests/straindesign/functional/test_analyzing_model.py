import imghdr
import sys
import tempfile

from straindesign._version import __app_name__
from straindesign.utils import cmd
from tests.straindesign.main_test import Main_test


class TestAnalyzingModel(Main_test):
    def test_base(self):
        with tempfile.NamedTemporaryFile(suffix=".png") as fd:
            args = ["python", "-m", __app_name__, "analyzing-model"]
            args += ["--input-model-file", self.model_ecoli_gz]
            args += ["--biomass-rxn-id", "BIOMASS_Ec_iAF1260_core_59p81M"]
            args += ["--target-rxn-id", "EX_tyrp_e"]
            args += ["--output-pareto-png", fd.name]

            ret = cmd.run(args)
            if ret.returncode > 0:
                print(ret.stderr)
                print(ret.stdout)
                sys.exit(1)

            self.assertEqual(imghdr.what(fd.name), "png")

    def test_medium(self):
        with tempfile.NamedTemporaryFile(suffix=".png") as fd:
            args = ["python", "-m", __app_name__, "analyzing-model"]
            args += ["--input-model-file", self.model_ecoli_gz]
            args += ["--biomass-rxn-id", "BIOMASS_Ec_iAF1260_core_59p81M"]
            args += ["--target-rxn-id", "EX_tyrp_e"]
            args += ["--output-pareto-png", fd.name]
            args += ["--input-medium-file", self.medium_butanol_csv]

            ret = cmd.run(args)
            if ret.returncode > 0:
                print(ret.stderr)
                print(ret.stdout)
                sys.exit(1)

            self.assertEqual(imghdr.what(fd.name), "png")

    def test_pathway(self):
        with tempfile.NamedTemporaryFile(suffix=".png") as fd:
            args = ["python", "-m", __app_name__, "analyzing-model"]
            args += ["--input-model-file", self.model_ecoli_gz]
            args += ["--biomass-rxn-id", "BIOMASS_Ec_iAF1260_core_59p81M"]
            args += ["--target-rxn-id", "EX_tyrp_e"]
            args += ["--output-pareto-png", fd.name]
            args += ["--input-medium-file", self.medium_butanol_csv]
            args += ["--input-pathway-file", self.pathway_butanol]

            ret = cmd.run(args)
            if ret.returncode > 0:
                print(ret.stderr)
                print(ret.stdout)
                sys.exit(1)

            self.assertEqual(imghdr.what(fd.name), "png")

    def test_substrate(self):
        with tempfile.NamedTemporaryFile(suffix=".png") as fd:
            args = ["python", "-m", __app_name__, "analyzing-model"]
            args += ["--input-model-file", self.model_ecoli_gz]
            args += ["--biomass-rxn-id", "BIOMASS_Ec_iAF1260_core_59p81M"]
            args += ["--target-rxn-id", "EX_tyrp_e"]
            args += ["--output-pareto-png", fd.name]
            args += ["--substrate-rxn-id", "EX_glc__D_e"]

            ret = cmd.run(args)
            if ret.returncode > 0:
                print(ret.stderr)
                print(ret.stdout)
                sys.exit(1)

            self.assertEqual(imghdr.what(fd.name), "png")
