# StrainDesign

[![Github Version](https://img.shields.io/github/v/release/brsynth/straindesign?display_name=tag&sort=semver)](version) [![Conda Version](https://img.shields.io/conda/vn/bioconda/straindesign.svg)](https://anaconda.org/bioconda/straindesign)  
[![GitHub Super-Linter](https://github.com/brsynth/straindesign/workflows/Tests/badge.svg)](https://github.com/marketplace/actions/super-linter) [![Coverage](https://img.shields.io/coveralls/github/brsynth/straindesign)](coveralls)  
[![License](https://img.shields.io/github/license/brsynth/straindesign)](license) [![DOI](https://zenodo.org/badge/436924636.svg)](https://zenodo.org/badge/latestdoi/436924636) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Gitter](https://badges.gitter.im/BioRetroSynth/SynBioCAD.svg)](https://gitter.im/BioRetroSynth/SynBioCAD?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)  

## Description

*straindesign* provides a cli interface to predict gene knockout targets with an heterologous pathway.
Integrate an hard fork from [cameo](https://github.com/biosustain/cameo) (v0.13.6) named `cameobrs` to add features.

## Installation

```sh
conda install -c bioconda straindesign
```

## Usage

### Define the best combination of genes deletion to optimize a target

```sh
python -m straindesign simulate-deletion \
    [input files]
    --input-model-file <SBML file>
    --input-pathway-file <SBML file>
    --input-medium-file <CSV/TSV file>
    [parameters]
    --biomass-rxn-id <id reaction, str>
    --target-rxn-id <id reaction, str>
    --substrate-rxn-id <id reaction, str>
    [output file]
    --output-file <CSV/TSV file>
```

### Delete genes in a model

```sh
python -m straindesign reduce-model \
    [input files]
    --input-model-file <SBML file>
    --input-straindesign-file <CSV file>
    and/or
    --input-gene-str <id gene, str>
    [parameters]
    --parameter-strategy-str <yield-max, gene-max, gene-min>
    [output file]
    --output-file-sbml <SBML file>
```

You can provide a list of genes to delete in the model or the file produced by the command `simulate-deletion`.
If this file is provided, the combination of genes is choosen among three strategies:

* yield-max: genes are sorted by the best yield
* gene-max: the combination of the maximum number of genes
* gene-min: the combination of the minimum number of genes

### Produce a pareto plot

```sh
python -m straindesign analyzing-model \
    [input files]
    --input-model-file <SBML file>
    --input-medium-file <CSV/TSV file>
    --input-pathway-file <SBML file>
    [parameters]
    --biomass-rxn-id <id reaction, str>
    --target-rxn-id <id reaction, str>
    --substrate-rxn-id <id reaction, str>
    [output file]
    --output-pareto-png <PNG file>
```
You can provide an heterologous pathway to implement the metabolic pathway producing the targeted compound represented by the `target-rxn-id`, the reaction which produces this compound.  
The `substrate-rxn-id` argument lets you to choose the main carbon source.

## Tests

Requires:
* *pytest*
* *pytest-benchmark*

```sh
python -m pytest
```
