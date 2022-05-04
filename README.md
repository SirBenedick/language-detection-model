# language-detection-model

## Run web app locally
```bash
pip install -r requirements.txt

# if streamlit is on $PATH
streamlit run app.py  

# else
python -m streamlit run app.py
```

## Run app locally
```bash
docker build -f Dockerfile-local .  -t language-detection-model-v2 

docker run -it -p 8501:8501 language-detection-model-v2
```