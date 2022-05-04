FROM python:3.9-slim
EXPOSE 8501
COPY requirements-deploy.txt ./requirements-deploy.txt
RUN pip install --no-cache-dir -r requirements-deploy.txt
COPY . /app
WORKDIR /app
CMD streamlit run app.py --server.port $PORT