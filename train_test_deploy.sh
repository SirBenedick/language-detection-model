#!/bin/bash

set -eux

if [[ -n $(git diff --name-only --cached) ]]; then
  echo "Uncommited changes in git repo, please commit or stash. Exit"
  exit 1
fi

cd "$(dirname -- "$(readlink -f "${BASH_SOURCE}")")"

curl -o data/feedback.csv https://language-detection-api-v2.herokuapp.com/download
python3 train.py --input data --epochs 10 --output app/data/trained_models/
git add app/data/trained_models
git commit -m "Update model $(date -u +'%Y-%m-%dT%H:%M')"
git push