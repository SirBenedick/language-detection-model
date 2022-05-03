FROM python:3.9
EXPOSE 8501
WORKDIR /app
COPY requirements-deploy.txt ./requirements-deploy.txt
RUN pip3 install -r requirements-deploy.txt
COPY . .
CMD streamlit run app.py --server.port $PORT
