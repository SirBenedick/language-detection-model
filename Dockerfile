FROM python:3.9
EXPOSE 8080
WORKDIR /app
COPY . .
COPY requirements-deploy.txt ./requirements-deploy.txt
RUN pip3 install -r requirements-deploy.txt
COPY . .
CMD streamlit run app.py --server.port 8080
