FROM python:3.9-slim

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir /training
ADD *.py /training/

RUN chmod +x training/*.py

WORKDIR /training
CMD python