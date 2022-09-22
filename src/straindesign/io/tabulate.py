import csv

import pandas as pd


class Tabulate(object):
    """Tabulate is a class loading/saving DataFrame from CSV, TSV files"""

    @classmethod
    def from_tabulate(
        cls,
        path: str,
        sep: str = "infer",
        **kwargs,
    ) -> pd.DataFrame:
        # Find delimiter.
        if sep == "infer":
            with open(path) as fid:
                dialect = csv.Sniffer().sniff(fid.readline())
            sep = dialect.delimiter
        # Load.
        df = pd.read_csv(
            path,
            sep=sep,
            **kwargs,
        )
        return df

    @classmethod
    def to_tabulate(
        cls, path: str, df: pd.DataFrame, sep: str = "infer", index: bool = False
    ) -> None:
        if sep == "infer":
            if path.endswith("tsv"):
                sep = "\t"
            elif path.endswith("csv"):
                sep = ","
        df.to_csv(path, sep=sep, index=index)
