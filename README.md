# rpFbaAnalysis

[![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/guillaume-gricourt/dcbec0ab9a7556f091c36e48a58980dd/raw/version.json)](version)
[![DOI](https://zenodo.org/badge/436924636.svg)](https://zenodo.org/badge/latestdoi/436924636)  
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub Super-Linter](https://github.com/brsynth/rpFbaAnalysis/workflows/Tests/badge.svg)](https://github.com/marketplace/actions/super-linter)
[![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/guillaume-gricourt/dcbec0ab9a7556f091c36e48a58980dd/raw/coverage.json)](code_coverage)  
[![Conda Recipe](https://img.shields.io/badge/recipe-rpfa-green.svg)](https://anaconda.org/bioconda/rpfa)
[![Conda Downloads](https://img.shields.io/conda/dn/bioconda/rpfa.svg)](https://anaconda.org/bioconda/rpfa)
[![Conda Version](https://img.shields.io/conda/vn/bionconda/rpfa.svg)](https://anaconda.org/bioconda/rpfa)
[![Conda Platforms](https://img.shields.io/conda/pn/bioconda/rpfa.svg)](https://anaconda.org/bioconda/rpfa)  
[![Gitter](https://badges.gitter.im/BioRetroSynth/SynBioCAD.svg)](https://gitter.im/BioRetroSynth/SynBioCAD?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

## Description
*rpFbaAnalysis* provides a cli interface to run OptGene/OptKnock with an heterologous pathway.  

## Installation
Download asset from the last *Releases*.  

* Unzip asset  
```sh
unzip <folder>
```  
* Install *wheel* with *pip*  
```sh
pip install <unzipped file>.whl
```

## Usage
Example: Define the best combination of genes deletion to optimize a target.

```python
python -m rpfa \
    [input files]
    --input-model-file <SBML file>
    --input-pathway-file <SBML file>
    --input-medium-file <CSV file>
    [input parameters]
    --biomass-rxn-id <id reaction, str>
    --target-rxn-id <id reaction, str>
    --substrate-rxn-id <id reaction, str>
    [output file]
    --output-file <CSV file>
```
Or with docker:  
```sh
docker run \
    -it \
    --rm \
    -v $PWD:/data \
    rpfbaanalysis:latest \
    --input-model /data/<SBML file> \
    --input-pathway-file /data/<SBML file> \
    --input-medium-file /data/<CSV file> \
    --biomass-rxn-id <id reaction, str> \
    --target-rxn-id <id reaction, str> \
    --substrate-rxn-id <id reaction, str>
    --output-file /data/<CSV file>
```

## Tests
*pytest* is installed with this package.
```bash
cd <repository>
python -m pytest
```

## Built with these main libraries

* [cameo](https://github.com/biosustain/cameo) - Computer aided metabolic engineering & optimization
* [cobrapy](https://github.com/opencobra/cobrapy) - Constraint-based modeling of metabolic networks
* [Pandas](https://github.com/pandas-dev/pandas) - Essential dataframe object

## Authors
* **Guillaume Gricourt**

## Licence
Released under the Apache-2.0 licence.  
See the LICENCE file for details.
