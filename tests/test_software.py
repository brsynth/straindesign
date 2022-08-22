import csv
import os
import subprocess
import sys
import tempfile

from main_test import Main_test
from rpfbagr._version import __app_name__


class Test_software(Main_test):
    @staticmethod
    def launch(args):
        if isinstance(args, str):
            args = args.split()
        ret = subprocess.run(args, capture_output=True, encoding="utf8")
        return ret

    def test_software_butanol(self):
        # Be careful: can not test gene annotation into
        # worflows running simultaneously
        with tempfile.NamedTemporaryFile(delete=False) as fd:
            args = ["python", "-m", __app_name__]
            args += ["--input-model-file", self.model_ecoli_gz]
            args += ["--input-pathway-file", self.pathway_butanol]
            args += ["--biomass-rxn-id", "BIOMASS_Ec_iAF1260_core_59p81M"]
            args += ["--target-rxn-id", "EX_1btol_e"]
            args += ["--substrate-rxn-id", "EX_glc__D_e"]
            args += ["--output-file-csv", fd.name]
            args += ["--strategy", "ko"]
            args += ["--max-knockouts", "3"]
            args += ["--input-medium-file", self.medium_butanol_csv]
            args += ["--thread", "1"]

            ret = Test_software.launch(args)
            if ret.returncode > 0:
                print(ret.stderr)
                print(ret.stdout)
                sys.exit(1)
            lines = []
            with open(fd.name) as fid:
                lines = fid.read().splitlines()
            self.assertGreater(len(lines), 1)
        os.remove(fd.name)

    def test_software_butanol_light(self):
        # Be careful: can not test gene annotation into
        # worflows running simultaneously
        with tempfile.NamedTemporaryFile(delete=False) as fd:
            args = ["python", "-m", __app_name__]
            args += ["--input-model-file", self.model_ecoli_core]
            args += ["--input-pathway-file", self.pathway_butanol]
            args += ["--biomass-rxn-id", "BIOMASS_Ecoli_core_w_GAM"]
            args += ["--target-rxn-id", "EX_1btol_e"]
            args += ["--substrate-rxn-id", "EX_glc__D_e"]
            args += ["--output-file-csv", fd.name]
            args += ["--strategy", "ko"]
            args += ["--max-knockouts", "3"]
            args += ["--input-medium-file", self.medium_butanol_tsv]
            args += ["--thread", "1"]

            ret = Test_software.launch(args)
            if ret.returncode > 0:
                print(ret.stderr)
                print(ret.stdout)
                sys.exit(1)
            lines = []
            with open(fd.name) as fid:
                lines = fid.read().splitlines()
            self.assertGreater(len(lines), 0)

            # Check delimiter
            with open(fd.name) as fid:
                dialect = csv.Sniffer().sniff(fid.readline())
                assert dialect.delimiter == ","
        os.remove(fd.name)

    def test_software_butanol_iml1515(self):
        # Be careful: can not test gene annotation into
        # worflows running simultaneously
        with tempfile.NamedTemporaryFile(delete=False) as fd:
            args = ["python", "-m", __app_name__]
            args += ["--input-model-file", self.model_ecoli_iml1515]
            args += ["--input-pathway-file", self.pathway_butanol]
            args += ["--biomass-rxn-id", "biomass"]
            args += ["--target-rxn-id", "EX_1btol_e"]
            args += ["--substrate-rxn-id", "EX_glc__D_e"]
            args += ["--output-file-tsv", fd.name]
            args += ["--strategy", "ko"]
            args += ["--max-knockouts", "3"]
            args += ["--input-medium-file", self.medium_butanol_csv]
            args += ["--thread", "1"]

            ret = Test_software.launch(args)
            if ret.returncode > 0:
                print(ret.stderr)
                print(ret.stdout)
                sys.exit(1)
            lines = []
            with open(fd.name) as fid:
                lines = fid.read().splitlines()
            self.assertGreater(len(lines), 0)
            # Check delimiter
            with open(fd.name) as fid:
                dialect = csv.Sniffer().sniff(fid.readline())
                assert dialect.delimiter == "\t"

        os.remove(fd.name)

    def test_software_galaxy(self):
        # Be careful: can not test gene annotation into
        # worflows running simultaneously
        with tempfile.NamedTemporaryFile(delete=False) as fd:
            args = ["python", "-m", __app_name__]
            args += ["--input-model-file", self.model_ecoli_gz]
            args += ["--input-pathway-file", self.pathway_butanol]
            args += ["--biomass-rxn-id", "BIOMASS_Ec_iAF1260_core_59p81M"]
            args += ["--target-rxn-id", "EX_1btol_e"]
            args += ["--substrate-rxn-id", "EX_glc__D_e"]
            args += ["--output-file-tsv", fd.name]
            args += ["--strategy", "ko"]
            args += ["--max-knockouts", "3"]
            args += ["--input-medium-file", self.medium_butanol_tsv]
            args += ["--thread", "1"]

            ret = Test_software.launch(args)
            if ret.returncode > 0:
                print(ret.stderr)
                print(ret.stdout)
                sys.exit(1)
            lines = []
            with open(fd.name) as fid:
                lines = fid.read().splitlines()
            self.assertGreater(len(lines), 0)

            # Check delimiter
            with open(fd.name) as fid:
                dialect = csv.Sniffer().sniff(fid.readline())
                assert dialect.delimiter == "\t"
        os.remove(fd.name)
