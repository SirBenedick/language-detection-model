curl -o data/feedback.csv https://language-detection-api-v2.herokuapp.com/download
python3 train.py --input data --epochs 10 --output app/data/trained_models/
