from typing import List
import telegram
import csv


class TelegramStorage:
    csv_file_name = "storage.csv"

    def __init__(self, CHANNEL_ID, BOT_READER_TOKEN, BOT_SENDER_TOKEN):
        self.channel_id = CHANNEL_ID
        self.BOT_READER_TOKEN = BOT_READER_TOKEN
        self.BOT_SENDER_TOKEN = BOT_SENDER_TOKEN
        self.bot_reader = telegram.Bot(token=BOT_SENDER_TOKEN)
        self.bot_sender = telegram.Bot(token=BOT_READER_TOKEN)

        # on initiation download latest CSV and store locally
        file = self._getLatestDocumentFromChannelMessages()
        self._downloadLatestCSVandStoreLocally(file)

    def addEntry(self, newRow: List):
        try:
            self._appendMessageToCSV(newRow)
            self._sendUpdatedCSVToChannel()
            return True
        except Exception as e:
            print(e)
            return False

    def getCSVContent(self):
        return_content = ""
        with open(self.csv_file_name) as csvFile:
            CSVdata = csv.reader(csvFile, delimiter=',')
            for row in CSVdata:
                return_content += ', '.join(row) + '<br>'
            csvFile.close()

        return return_content

    def getCSVFileName(self):
        return self.csv_file_name

    def _getLatestDocumentFromChannelMessages(self):
        updates = self.bot_reader.get_updates(allowed_updates=["messages"])
        last_sent_document = None
        for i in range(len(updates) - 1, -1, -1):
            update = updates[i].to_dict()
            if 'channel_post' in update:
                channel_post = update["channel_post"]
                if 'document' in channel_post:
                    last_sent_document = channel_post["document"]
                    break
        return last_sent_document

    def _downloadLatestCSVandStoreLocally(self, file):
        newFile = self.bot_reader.get_file(file["file_id"])
        newFile.download(custom_path=self.csv_file_name)

    def _appendMessageToCSV(self, newRow: List):
        with open(self.csv_file_name, 'a', newline='') as f_object:
            writer_object = csv.writer(f_object)
            writer_object.writerow(newRow)
            f_object.close()

    def _sendUpdatedCSVToChannel(self):
        self.bot_sender.send_document(
            chat_id=self.channel_id, document=open(self.csv_file_name, 'rb'))
