import ast
import logging

import pandas as pd

from Bio import Entrez
from cameo import load_model


def build_model(
    model_path: str,
    pathway_path: str,
    biomass_id: str,
    target_id: str,
    logger: logging.Logger
):
    logger.info('Load model')

    model = load_model(model_path)
    if pathway_path:
        logger.info('Load pathway')
        pathway_model = load_model(pathway_path)
        logger.info('Merge model and pathway')
        model.merge(
            pathway_model,
            inplace=True
        )

    # Check if reactions are in the model
    logger.info('Check if main objective is in the model')
    if model.reactions.get_by_id(biomass_id) is None:
        logger.error(
            'Reaction not found in the model: %s' % (biomass_id,)
        )
        return None
    logger.info('Check if target reaction is in the model')
    if model.reactions.get_by_id(target_id) is None:
        logger.error(
            'Reaction not found in the model: %s' % (target_id,)
        )
        return None

    logging.info('Set objective')
    model.objective = {
        model.reactions.get_by_id(biomass_id): 1.0,
        model.reactions.get_by_id(target_id): 0.5
    }

    return model


def genes_annotate(
    df: pd.DataFrame,
    email: str
) -> pd.DataFrame:
    if df.empty:
        return df
    cache = {}
    for ix in df.index:
        groups = df.loc[ix, 'genes']
        groups = ast.literal_eval(groups)

        # Build group
        groups = []
        for group in groups:
            labels = []
            for gene in group:
                if gene not in cache.keys():
                    hd = Entrez.esummary(db='gene', id=gene)
                    rec = Entrez.read(
                        hd,
                        validate=False
                    )
                    rec = rec.get('DocumentSummarySet', {})
                    rec = rec.get('DocumentSummary', [])
                    label = gene
                    if len(rec) > 0:
                        name = rec[0].get('Name', '')
                        desc = rec[0].get('Description', '')
                        syn = rec[0].get('OtherAliases', '')
                        label = '%s=%s - %s' % (name, syn, desc)
                    cache[gene] = label
                labels.append(cache[gene])
            labels = '(%s)' % (','.join(labels),)
            groups.append(labels)
        df.at[ix, 'genes_annotation'] = ','.join(groups)
    return df


def save_results(
    df: pd.DataFrame,
    path: str
) -> None:
    df.to_csv(
        path,
        index=False
    )
