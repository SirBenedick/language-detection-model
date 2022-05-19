#!/bin/bash

set -eux

if [[ $(git rev-parse --abbrev-ref HEAD) != "main" ]]; then
 echo "Must be on branch main. Exit"
 exit 2
fi
if [[ -n $(git diff --name-only) ]]; then
  echo "Uncommited changes in git repo, please commit or stash. Exit"
  exit 1
fi


git pull
cd "$(dirname -- "$(readlink -f "${BASH_SOURCE}")")"
cd ..

curl -o training/data/feedback.csv https://language-detection-api-v2.herokuapp.com/download
#docker run -v $(pwd)/training/data:/training/data -v $(pwd)/app/data/trained_models:/training/trained_models -it training ./train.py
python training/train.py
git add app/data/trained_models

REPORT_DIFF=$(git diff app/data/trained_models/report.json)
git commit -m "Update model $(date -u +'%Y-%m-%dT%H:%M')\n \
``` \
$REPORT_DIFF \
```"
git push
