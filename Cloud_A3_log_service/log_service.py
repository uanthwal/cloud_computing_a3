from flask import Flask, jsonify, abort, request, make_response
from flask_cors import CORS
import json
import time
import datetime

app = Flask(__name__)
CORS(app)

# Base Route
@app.route('/')
def index():
    return "Hello from log service!"

# Route for error handling
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/write-data-to-search-log', methods=['POST'])
def write_data_to_cat():
    req_data = request.json
    log_lines = []
    searched_text = req_data['keyword']
    new_string = str(searched_text) + " was searched at " + str(datetime.datetime.now())
    count = 0
    try:
        with open('search_log.txt') as log_file:
            log_lines = log_file.readlines()
            
        print(log_lines)
    except FileNotFoundError:
        print("File Not found")

    for line in log_lines:
        if searched_text in line:
            count = count + 1
    
    count = count + 1

    new_string = new_string + str(" Total count: " + str(count) +".\n")
    log_lines.append(new_string)
    with open('search_log.txt', 'w') as log_file:
        log_file.write("".join(log_lines))
    return jsonify({'code': '200', 'data': "Search log updated!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=6000, debug=True)
