"""
This script is run by the heroku scheduler add on.
It is needed because telegram does not allow to view "old" messages or the chat history.
Therefor this script downloades the latest CSV and sends it as a new message every hour (configured in heroku).
"""
from TelegramStorage import TelegramStorage
import os
BOT_SENDER_TOKEN = os.environ['BOT_SENDER_TOKEN']
BOT_READER_TOKEN = os.environ['BOT_READER_TOKEN']
CHANNEL_ID = os.environ['CHANNEL_ID']

telage = TelegramStorage(CHANNEL_ID, BOT_READER_TOKEN, BOT_SENDER_TOKEN)
telage._sendLocalCSVToChannel()