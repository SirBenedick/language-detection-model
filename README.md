# language-detection-model-v2

## Run locally
```bash
# Run app
docker build -f Dockerfile-local .  -t language-detection-model-v2 
docker run -it -p 8501:8501 language-detection-model-v2

# Run api
docker image build -t flask_docker .
docker run -p 5055:5055 -d --env-file=env flask_docker
```

## API
The API has three exposed endpoints:
- /add
- /view
- /download

**/add** Lets you add a new entry to the CSV storage, and requires two paramters, "text" and "label":

`http:.../add?text=Jonas%20is%20nice&label=english`

**/view** displayes the content of the data.

**/download** downloads the stored CSV file. 



## Run web app locally
```bash
pip install -r requirements.txt

# if streamlit is on $PATH
streamlit run app.py  

# else
python -m streamlit run app.py
```