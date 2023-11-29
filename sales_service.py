from flask import Flask, request, jsonify
from flask_cors import CORS
from create_db import get_goods, get_good_by_good_id, insert_good, update_good, delete_good, get_good_by_name
from create_db import get_customer_by_username, update_customer
from create_purchasesdb import insert_purchase

app = Flask(__name__)
CORS(app, resources={r"/*":{"origins":"*"}})

@app.route('/api/get_goods', methods=['GET'])
def api_get_goods():
    """API endpoint to retrieve a list of all good names and prices.

    :return: JSON response containing the list of customers
    :rtype: JSON
    """
    goods_list = get_goods()
    names_and_prices = [(good["name"], good["price"]) for good in goods_list]

    return jsonify(get_goods())

@app.route('/api/good/<good_id>', methods=['GET'])
def api_get_good(good_id):
    """API endpoint to retrieve a list of all good names and prices.

    :return: JSON response containing the list of customers
    :rtype: JSON
    """
    return jsonify(get_good_by_good_id(good_id))

@app.route('/api/sale', methods=['POST'])
def api_make_sale():
    """API endpoint to process a sale.
    :return: a JSON response with the result of the sale.
    "rtype: JSON
    """
    data = request.get_json()
    good_name = data.get('good_name')
    customer_username = data.get('customer_username')
    try:
        # Check if the required data is provided
        if not good_name or not customer_username:
            return jsonify({'error': 'Invalid request. Missing parameters.'}), 400

        # Retrieve customer details
        customer = get_customer_by_username(customer_username)
        if not customer:
            return jsonify({'error': 'Customer not found.'}), 404

        # Retrieve good details
        good = get_good_by_name(good_name)
        if not good:
            return jsonify({'error': 'Good not found.'}), 404

        # Check if the customer has enough money
        if customer['wallet_balance'] < good['price']:
            return jsonify({'error': 'Insufficient funds.'}), 400

        # Check if the good is available
        if good['count'] <= 0:
            return jsonify({'error': 'Good not available.'}), 400

        # Deduct money from customer wallet
        new_wallet_balance = customer['wallet_balance'] - good['price']
        customer['wallet_balance'] = new_wallet_balance
        update_customer(customer)

        # Decrease the count of the purchased good
        new_good_count = good['count'] - 1
        update_good({'good_id': good['good_id'], 'count': new_good_count})

        # Save historical purchase
        insert_purchase(customer_username, good['name'], good['price'])

        return jsonify({'message': 'Sale successful.'})

    except Exception as e:
        # Handle unexpected errors
        return jsonify({'error': f'Error: {str(e)}'})

if __name__=="__main__":
    app.run(port=8080)



