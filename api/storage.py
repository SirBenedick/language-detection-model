import telegram
import csv
import os
BOT_SENDER_TOKEN = os.environ['BOT_SENDER_TOKEN']
BOT_READER_TOKEN = os.environ['BOT_READER_TOKEN']
CHANNEL_ID = os.environ['CHANNEL_ID']


def getLatestFileFromChannelMessages(bot_reader):
    updates = bot_reader.get_updates()
    update = updates[-1]
    return update.channel_post.document


def downloadLatestCSVandStoreLocally(file, csv_file_name):
    # TODO: check if last meswsage has a document
    newFile = bot_reader.get_file(file.file_id)
    newFile.download(custom_path=csv_file_name)


def appendMessageToCSV(text, label, csv_file_name):
    list_data = [text, label.lower()]
    # First, open the old CSV file in append mode, hence mentioned as 'a'
    # Then, for the CSV file, create a file object
    with open(csv_file_name, 'a', newline='') as f_object:
        # Pass the CSV  file object to the writer() function
        writer_object = csv.writer(f_object)
        # Result - a writer object
        # Pass the data in the list as an argument into the writerow() function
        writer_object.writerow(list_data)
        # Close the file object
        f_object.close()


def sendUpdatedCSVToChannel(csv_file_name, bot_sender, channel_id):
    bot_sender.send_document(
        chat_id=channel_id, document=open(csv_file_name, 'rb'))


channel_id = CHANNEL_ID
csv_file_name = "storage.csv"
bot_reader = telegram.Bot(token=BOT_SENDER_TOKEN)
bot_sender = telegram.Bot(token=BOT_READER_TOKEN)


def updateCSV(text, label):
    try:
        file = getLatestFileFromChannelMessages(bot_reader=bot_reader)
        downloadLatestCSVandStoreLocally(file, csv_file_name)
        appendMessageToCSV(text, label, csv_file_name)
        sendUpdatedCSVToChannel(csv_file_name, bot_sender, channel_id)
        return "True"
    except:
        return "False"


def getCSVContent():
    return_content = ""
    with open(csv_file_name) as csvFile:
        CSVdata = csv.reader(csvFile, delimiter=',')
        for row in CSVdata: 
            return_content += ', '.join(row) + '<br>'
        csvFile.close() 

    return return_content


def getCSVFileName():
    return csv_file_name
