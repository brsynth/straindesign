# rpFbaAnalysis

[![badge](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/guillaume-gricourt/dcbec0ab9a7556f091c36e48a58980dd/raw/version.json)](version)
[![GitHub Super-Linter](https://github.com/brsynth/rpFbaAnalysis/workflows/Tests/badge.svg)](https://github.com/marketplace/actions/super-linter)

## Description
*rpFbaAnalysis* provides a cli interface to run OptGene with an heterologous pathway.  

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

## Tests
*pytest* is installed with this package.
```bash
cd <repository>
python -m pytest
```

## Authors
* **Guillaume Gricourt**

## Licence
Released under the MIT licence. See the LICENCE file for details.
