FROM python:3.9-alpine

# used for receiving the env variables through github actions
# for local development use "--env-file=env"
ARG BOT_READER_TOKEN_ARG
ENV BOT_READER_TOKEN=$BOT_READER_TOKEN_ARG
ARG BOT_SENDER_TOKEN_ARG
ENV BOT_SENDER_TOKEN=$BOT_SENDER_TOKEN_ARG
ARG CHANNEL_ID_ARG
ENV CHANNEL_ID=$CHANNEL_ID_ARG

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
WORKDIR /app
CMD python api.py
