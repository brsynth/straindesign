# Module skeleton

This repository contains the skeleton to create, test and publish a Python module.

## Create new module

Before all, a new repository has to be created.

### Download
```sh
git clone https://github.com/brsynth/module.git
```

### Customize
```sh
bash custom.sh
```
After this process, there will be some details to customise on your own. Locations will be displayed after the script ended.

## Adding code
The fresh new code is to placed into module folder, a first empty file has been created. The code has to follow the team's guidelines (https://github.com/brsynth/Coding-Guidelines).

## Checking
Code checking is achieved by `flake` and `bandit` that scan (without running it) the code and highlight errors.

Checking occurs automatically through GitHub actions each time some commits are pushed on branches `dev` and `master`. The workflow is defined in `.github/check.yml` file.

### Check manually
Checking can be processed locally by running:
```sh
cd tests
./check-in-docker.sh
```

## Testing
Code testing is achieved by Python code under `tests/*.py`.

Testing occurs automatically through GitHub actions each time some commits are pushed on branch `master`. The workflow is defined in `.github/test.yml` file.

### Test manually
Checking can be processed locally by running:
```sh
cd tests
./test-in-docker.sh
```

## Publishing
Code is published on PyPi (pypi.org) and Anaconda (anaconda.org) platforms.

Publishing occurs automatically through GitHub actions each time some commits related to `RELEASE` file are pushed on branch `stable`. The workflow is defined in `.github/publish.yml` file.
