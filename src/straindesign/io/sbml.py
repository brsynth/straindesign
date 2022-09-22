import cobra
from cobra.io import read_sbml_model, write_sbml_model


def cobra_from_sbml(path: str) -> cobra.Model:
    return read_sbml_model(path)


def cobra_to_sbml(model: cobra.Model, path: str) -> None:
    write_sbml_model(model, path)
