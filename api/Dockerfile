ARG BOT_READER_TOKEN
ARG BOT_SENDER_TOKEN
ARG CHANNEL_ID

FROM python:3.9-alpine

ENV BOT_READER_TOKEN=$BOT_READER_TOKEN
ENV BOT_SENDER_TOKEN=$BOT_SENDER_TOKEN
ENV CHANNEL_ID=$CHANNEL_ID

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
WORKDIR /app
CMD python api.py
