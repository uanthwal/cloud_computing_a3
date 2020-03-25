from flask import Flask, jsonify, abort, request, make_response
from pymongo import MongoClient
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

# Route for error handling
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def make_connection_to_db(target_db):
    cnx = MongoClient('mongodb://upendra:upendra@54.85.124.206:27017/cloud_a3')
    return cnx

@app.route('/', methods=['GET'])
@cross_origin()
def index():
    return "Hello from the Notes service"


# Route to fetch the distinct GEO locations
@app.route('/search-notes', methods=['POST'])
@cross_origin()
def search_notes():
    if request.method == 'POST':
        req_data = request.json
        searched_text = req_data['search_text']
        print(searched_text)
        db_connection = make_connection_to_db('mongodb')
        response_list = []
        if db_connection is not None:
            db = db_connection.cloud_a3
            cursor = db.notes.find({'search_text':searched_text})
            for c in cursor:
                response_list.append({"search_text":c['search_text'], "notes_text":c['notes_text']})
        else:
            print("Connection not established")
        return jsonify({'code': '200', 'data': response_list, 'message':'Search results for ' + searched_text + ' : ' + str(len(response_list)) +' result(s)'}), 200
    else:
        return "GET Req"


@app.route('/save-notes', methods=['POST'])
@cross_origin()
def save_notes():
    if request.method == 'POST':
        req_data = request.json
        db_connection = make_connection_to_db('mongodb')
        if db_connection is not None:
            db = db_connection.cloud_a3
            db.notes.insert(req_data)
        else:
            print("Connection not established")
        return jsonify({'code': '200', 'data': "Inserted"}), 200
    else:
        return "GET Req"


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000, debug=True)
