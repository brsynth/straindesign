#!/bin/bash

# Commitizen
npm init
npm install --silent node-jq --save

# Read informations from package.json
name=$(./node_modules/node-jq/bin/jq -r ".name"  package.json)
descr=$(./node_modules/node-jq/bin/jq -r ".description"  package.json)
url=$(./node_modules/node-jq/bin/jq -r ".repository.url"  package.json)
authors=$(./node_modules/node-jq/bin/jq -r ".author"  package.json)
read -p 'Corresponding author(s) ('"$authors"'): ' corr_authors
if [ -z "$corr_authors" ]
then
      corr_authors=$authors
fi

# escape strings
name_e=$(printf '%s\n' "$name" | sed -e 's/[\/&]/\\&/g')
descr_e=$(printf '%s\n' "$descr" | sed -e 's/[\/&]/\\&/g')
url_e=$(printf '%s\n' "$url" | sed -e 's/[\/&]/\\&/g')
authors_e=$(printf '%s\n' "$authors" | sed -e 's/[\/&]/\\&/g')
corr_authors_e=$(printf '%s\n' "$corr_authors" | sed -e 's/[\/&]/\\&/g')


# README.md
mv pre_README.md README.md
sed -i "" "s/# TO_FILL/# $name/"                                               README.md
sed -i "" "s/brsynth\/TO_FILL/brsynth\/test/g"                                 README.md
sed -i "" "s/DESCR: TO_FILL/$descr/"                                           README.md
sed -i "" "s/python -m pip install TO_FILL/python -m pip install $name/"       README.md
sed -i "" "s/conda install -c brsynth TO_FILL/conda install -c brsynth $name/" README.md
sed -i "" "s/from TO_FILL import TO_FILL/from $name import $name/"             README.md
sed -i "" "s/python -m TO_FILL/python -m $name/"                               README.md
sed -i "" "s/* \*\*TO_FILL\*\*$/* **$corr_authors**/"                          README.md
sed -i "" "s/* TO_FILL$/* $authors/"                                           README.md

# RELEASE.md
cat <<EOT >> RELEASE.md
# Release history

## 1.0.0
- chore(release): first release
EOT

# src
mv TO_FILL $name
touch $name/$name.py
sed -i "" "s/from TO_FILL.TO_FILL import TO_FILL/from $name.$name import $name/" $name/__init__.py
sed -i "" "s/\"TO_FILL\"/\"$name\"/"                                             $name/__init__.py
sed -i "" "s/from TO_FILL import TO_FILL/from $name import $name/"               $name/__main__.py

# extras
sed -i "" "s/PACKAGE=TO_FILL/PACKAGE=$name_e/"                 extras/.env
sed -i "" "s/DESCR='TO_FILL'/DESCR='$descr_e'/"                extras/.env
sed -i "" "s/URL=TO_FILL/URL=$url_e/"                          extras/.env
sed -i "" "s/AUTHORS='TO_FILL'/AUTHORS='$authors_e'/"          extras/.env
sed -i "" "s/CORR_AUTHOR=TO_FILL/CORR_AUTHOR=$corr_authors_e/" extras/.env

# tests
sed -i "" "s/mod_name = 'TO_FILL'/mod_name = '$name'/" tests/module.py

# recipe
sed -i "" "s/TO_FILL/$name/" recipe/meta.yaml

# GitHub
sed -i "" "s/TO_FILL/$name/" .github/workflows/publish.yml
git remote set-url origin $url
echo custom.sh >> .gitignore

# Commitizen
commitizen init cz-conventional-changelog --save-dev --save-exact

echo
echo Customisation is completed!
echo
echo There is still some missing fields to replace:
grep -rnw '.' --exclude='custom.sh' --exclude='./.git/*' -e 'TO_FILL'

echo
echo
echo "This file (custom.sh) can be removed."
