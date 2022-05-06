# Dockerfile used for the CI/CD-GitHub-Actions-Pipeline to push to heroku
FROM python:3.9-slim
EXPOSE 8501
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
WORKDIR /app
CMD streamlit run app.py --server.port $PORT