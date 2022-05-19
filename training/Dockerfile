FROM python:3.9-slim

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y git curl

RUN mkdir /training
ADD *.py /training/
ADD train_and_commit.sh /training/

RUN chmod +x training/*.py

WORKDIR /training
CMD python