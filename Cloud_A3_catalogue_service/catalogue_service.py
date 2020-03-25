from flask import Flask, jsonify, abort, request, make_response
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Base Route
@app.route('/')
def index():
    return "Hello from catalogue service!"

# Route for error handling
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/write-data-to-catalogue', methods=['POST'])
def write_data_to_cat():
    req_data_1 = request.json
    req_data = req_data_1['data']
    book_data = {}
    new_file = False
    try:
        with open('catalogue.json') as json_file:
            book_data = json.load(json_file)
            json_file.close()
        print(book_data)
    except FileNotFoundError:
        new_file = True
        print("File Not found")
    
    for book in req_data:
        book_name = book['book_name']
        if new_file:
            book_data[book_name] = book['author_name']
        else:
            print(book_name)
            if book_name not in book_data:
                book_data[book_name] = book['author_name']
    
    with open('catalogue.json', 'w') as out:
        json.dump(book_data, out)
    return jsonify({'code': '200', 'data': "Data added successfully!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=7000, debug=True)
