import cameobrs
import cobra


def from_sbml(path: str) -> cobra.Model:
    return cameobrs.load_model(path)


def to_sbml(model: cobra.Model, path: str) -> None:
    cobra.io.write_sbml_model(model, path)
