import os
import unittest


class Main_test(unittest.TestCase):
    dataset_path = os.path.join(os.path.dirname(__file__), "dataset")
    # Medium.
    medium_path = os.path.join(dataset_path, "medium")
    medium_butanol = os.path.join(medium_path, "butanol.csv")
    # Model.
    model_path = os.path.join(dataset_path, "model")
    model_ecoli = os.path.join(model_path, "iAF1260.xml")
    model_ecoli_gz = os.path.join(model_path, "iAF1260.xml.gz")
    model_ecoli_iml1515 = os.path.join(model_path, "iML1515.xml")
    model_ecoli_core = os.path.join(model_path, "e_coli_core.xml")
    # Pathway.
    pathway_path = os.path.join(dataset_path, "pathway")
    pathway_butanol = os.path.join(pathway_path, "butanol.xml")
