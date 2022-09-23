import tempfile
from typing import Tuple

import cobra
from tests.main_test import Main_test
from straindesign._version import __app_name__
from straindesign.io import sbml
from straindesign.utils import cmd
from straindesign.utils import model as utils_model


class TestReduceModel(Main_test):
    def test_one(self):
        # Delete: 2 genes, 3 reactions
        model_ecoli = sbml.from_sbml(path=self.model_ecoli_gz)
        nb_gene = utils_model.count_gene(model=model_ecoli)
        nb_reaction = utils_model.count_reaction(model=model_ecoli)

        with tempfile.NamedTemporaryFile() as fd:
            args = ["python", "-m", __app_name__, "reduce-model"]
            args += ["--input-model-file", self.model_ecoli_gz]
            args += ["--input-straindesign-file", self.gene_butanol]
            args += ["--output-file-sbml", fd.name]

            ret = cmd.run(args)
            if ret.returncode > 0:
                print(ret.stderr)
                print(ret.stdout)
                sys.exit(1)

            model, errors = cobra.io.validate_sbml_model(fd.name)
            self.assertIsNot(model, None)

            self.assertEqual(nb_gene, len(model.genes) + 2)
            self.assertEqual(nb_reaction, len(model.reactions) + 3)

    def test_two(self):
        # Delete: 3 genes, 7 reactions
        model_ecoli = sbml.from_sbml(path=self.model_ecoli_gz)
        nb_gene = utils_model.count_gene(model=model_ecoli)
        nb_reaction = utils_model.count_reaction(model=model_ecoli)

        with tempfile.NamedTemporaryFile() as fd:
            args = ["python", "-m", __app_name__, "reduce-model"]
            args += ["--input-model-file", self.model_ecoli_gz]
            args += ["--input-straindesign-file", self.gene_butanol]
            args += ["--input-gene-str", "b4208", "b4208", "b3919"]
            args += ["--output-file-sbml", fd.name]

            ret = cmd.run(args)
            if ret.returncode > 0:
                print(ret.stderr)
                print(ret.stdout)
                sys.exit(1)

            model, errors = cobra.io.validate_sbml_model(fd.name)
            self.assertIsNot(model, None)

            self.assertEqual(nb_gene, len(model.genes) + 3)
            self.assertEqual(nb_reaction, len(model.reactions) + 7)
