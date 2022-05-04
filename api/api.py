import flask
from flask import request
import storage
import os 

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>Awesome telegram persistent storage – aka: the Next BIG THING</p>"

# A route to return all of the available entries in our catalog.
@app.route('/api', methods=['GET'])
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

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5055))
    app.run(debug=True, host='0.0.0.0', port=port)
