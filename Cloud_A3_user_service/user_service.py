from flask import Flask, jsonify, abort, request, make_response
from pymongo import MongoClient
from flask_cors import CORS, cross_origin
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

app = Flask(__name__)
CORS(app)

base_url = "http://54.85.124.206"

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def make_connection_to_db(target_db):
    cnx = MongoClient('mongodb://upendra:upendra@54.85.124.206:27017/cloud_a3')
    return cnx

@app.route('/', methods=['GET'])
@cross_origin()
def index():
    return "Hello from the User service"


# Route to fetch the distinct GEO locations
@app.route('/search-text', methods=['POST'])
@cross_origin()
def search_text():
    if request.method == 'POST':
        req_data = request.json
        searched_text = req_data['search_text']
        # searched_text = request.json['search_text']
        db_connection = make_connection_to_db('mongodb')
        response_list = []
        if db_connection is not None:
            db = db_connection.cloud_a3
            cursor = db.books.find({"$text": {"$search": searched_text}})
            session = requests.Session()
            retry = Retry(connect=3, backoff_factor=0.5)
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            log_service_response = session.post(base_url+str(":6000/write-data-to-search-log"), json={'keyword':searched_text})
            print(str(log_service_response))
            cursor_len = 0
            for c in cursor:
                cursor_len  = cursor_len + 1
                response_list.append({"book_name":c['book_name'], "author_name":c['author_name']})
            if cursor_len > 0:
                catalogue_service_response = requests.post(base_url+str(":7000/write-data-to-catalogue"), json={'data':response_list})
                print(str(catalogue_service_response))
        else:
            print("Connection not established")
        return jsonify({'code': '200', 'data': response_list, 'message':'Search results for ' + searched_text + ' : ' + str(len(response_list)) +' result(s)'}), 200
    else:
        return "GET Req"

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)
