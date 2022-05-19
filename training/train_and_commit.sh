#!/bin/bash

set -eux

cd "$(dirname -- "$(readlink -f "${BASH_SOURCE}")")"
cd ..

if [[ $(git rev-parse --abbrev-ref HEAD) != "main" ]]; then
 echo "Must be on branch main. Exit"
 exit 2
fi
if [[ -n $(git diff --name-only) ]]; then
  echo "Uncommited changes in git repo, please commit or stash. Exit"
  exit 1
fi

curl -o training/data/feedback.csv https://language-detection-api-v2.herokuapp.com/download
python training/train.py --input training/data --output app/data/trained_models
git add app/data/trained_models
git add training/data

REPORT_DIFF=$(git diff app/data/trained_models/report.json)
git commit -m "Update model $(date -u +'%Y-%m-%dT%H:%M')" -m "$REPORT_DIFF"