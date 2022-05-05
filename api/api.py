from flask import request, send_file, Flask
import storage
import os
app = Flask(__name__)

app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Awesome telegram persistent storage – aka: the Next BIG THING</p>"

# A route to add a new entry to the storage
# parameters "text" and "label"
@app.route('/add', methods=['GET'])
def update_storage():
    if 'text' in request.args:
        text = str(request.args['text'])
    else:
        return "Error: No text field provided. Please specify a text."

    if 'label' in request.args:
        label = str(request.args['label'])
    else:
        return "Error: No label field provided. Please specify an label (on of the following ['english', 'german', 'spanish'])."

    result = storage.updateCSV(text, label)
    return f"<h1>API – {result}</h1>"

# # A route to return all of the available entries of the csv.
@app.route('/view', methods=['GET'])
def return_csv_content():
    return_content = storage.getCSVContent()
    return return_content

# # A route to download the csv
@app.route('/download')
def post():
    csv_file_name = storage.getCSVFileName()
    return send_file(csv_file_name, as_attachment=True, download_name=csv_file_name)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5055))
    app.run(debug=True, host='0.0.0.0', port=port)
