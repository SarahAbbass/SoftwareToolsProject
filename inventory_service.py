from flask import Flask, request, jsonify
from flask_cors import CORS
from create_db import get_goods, get_good_by_good_id, insert_good, update_good, delete_good

app = Flask(__name__)
CORS(app, resources={r"/*":{"origins":"*"}})

@app.route('/api/goods', methods=['GET'])
def api_get_goods():
    return jsonify(get_goods())

@app.route('/api/goods/<good_id>', methods=['GET'])
def api_get_good(good_id):
    return jsonify(get_good_by_good_id(good_id))

@app.route('/api/goods/add', methods=['POST'])
def api_add_good():
    good = request.get_json()
    return jsonify(insert_good(good))

@app.route('/api/goods/update', methods=['PUT'])
def api_update_good():
    good = request.get_json()
    return jsonify(update_good(good))

@app.route('/api/goods/delete/<good_id>', methods=['DELETE'])
def api_delete_good(good_id):
    return jsonify(delete_good(good_id))

if __name__=="__main__":
    app.run()