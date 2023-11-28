from flask import Flask, request, jsonify
from flask_cors import CORS
from create_postgres_db import get_goods, get_good_by_good_id, insert_good, update_good, delete_good

app = Flask(__name__)
CORS(app, resources={r"/*":{"origins":"*"}})

@app.route('/api/goods', methods=['GET'])
def api_get_goods():
    """API endpoint to retrieve a list of all goods.

    :return: JSON response containing the list of goods
    :rtype: JSON
    """
    return jsonify(get_goods())

@app.route('/api/goods/<good_id>', methods=['GET'])
def api_get_good(good_id):
    """API endpoint to retrieve good information based on the provided good_id.

    :param good_id: The good_id of the good
    :type good_id: str
    :return: JSON response containing the good information
    :rtype: JSON
    """
    return jsonify(get_good_by_good_id(good_id))

@app.route('/api/goods/add', methods=['POST'])
def api_add_good():
    """API endpoint to add a new good.

    :return: JSON response containing the added good information
    :rtype: JSON
    """
    good = request.get_json()
    return jsonify(insert_good(good))

@app.route('/api/goods/update', methods=['PUT'])
def api_update_good():
    """API endpoint to update good information.

    :return: JSON response containing the updated good information
    :rtype: JSON
    """
    good = request.get_json()
    return jsonify(update_good(good))

@app.route('/api/goods/delete/<good_id>', methods=['DELETE'])
def api_delete_good(good_id):
    """API endpoint to delete a good based on the provided good_id.

    :param good_id: The good_id of the good to be deleted
    :type good_id: str
    :return: JSON response containing the deleted good confirmation message
    :rtype: JSON
    """
    return jsonify(delete_good(good_id))

if __name__=="__main__":
    app.run()