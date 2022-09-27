import os
import unittest


class Main_test(unittest.TestCase):
    dataset_path = os.path.join(os.path.dirname(__file__), "dataset")
    # Medium.
    medium_path = os.path.join(dataset_path, "medium")
    medium_butanol_csv = os.path.join(medium_path, "butanol.csv")
    medium_butanol_tsv = os.path.join(medium_path, "butanol.tsv")
    # Model.
    model_path = os.path.join(dataset_path, "model")
    model_ecoli = os.path.join(model_path, "iAF1260.xml")
    model_ecoli_gz = os.path.join(model_path, "iAF1260.xml.gz")
    model_ecoli_iml1515 = os.path.join(model_path, "iML1515.xml")
    model_ecoli_core = os.path.join(model_path, "e_coli_core.xml")
    # Pathway.
    pathway_path = os.path.join(dataset_path, "pathway")
    pathway_butanol = os.path.join(pathway_path, "butanol.xml")
    # Gene.
    gene_path = os.path.join(dataset_path, "gene")
    gene_butanol = os.path.join(gene_path, "simulate_deletion.butanol.iAF1260.csv")
    gene_value_error = os.path.join(gene_path, "gene.value_error.csv")
    gene_empty = os.path.join(gene_path, "gene.empty.csv")
