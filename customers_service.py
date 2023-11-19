from flask import Flask, request, jsonify
from flask_cors import CORS
from create_db import get_customers, get_customer_by_username, insert_customer, update_customer, delete_customer

app = Flask(__name__)
CORS(app, resources={r"/*":{"origins":"*"}})

@app.route('/api/customers', methods=['GET'])
def api_get_customers():
    return jsonify(get_customers())

@app.route('/api/customers/<username>', methods=['GET'])
def api_get_customer(username):
    return jsonify(get_customer_by_username(username))

@app.route('/api/customers/add', methods=['POST'])
def api_add_customer():
    customer = request.get_json()
    return jsonify(insert_customer(customer))

@app.route('/api/customers/update', methods=['PUT'])
def api_update_customer():
    customer = request.get_json()
    return jsonify(update_customer(customer))

@app.route('/api/customers/delete/<username>', methods=['DELETE'])
def api_delete_customer(username):
    return jsonify(delete_customer(username))

if __name__=="__main__":
    app.run()