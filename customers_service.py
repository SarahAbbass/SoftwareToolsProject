from flask import Flask, request, jsonify
from flask_cors import CORS
from create_db import get_customers, get_customer_by_username, insert_customer, update_customer, delete_customer
import requests

app = Flask(__name__)
CORS(app, resources={r"/*":{"origins":"*"}})

@app.route('/api/customers', methods=['GET'])
def api_get_customers():
    """API endpoint to retrieve a list of all customers.

    :return: JSON response containing the list of customers
    :rtype: JSON
    """
    return jsonify(get_customers())

@app.route('/api/customers/<username>', methods=['GET'])
def api_get_customer(username):
    """API endpoint to retrieve customer information based on the provided username.

    :param username: The username of the customer
    :type username: str
    :return: JSON response containing the customer information
    :rtype: JSON
    """
    return jsonify(get_customer_by_username(username))

@app.route('/api/customers/add', methods=['POST'])
def api_add_customer():
    """API endpoint to add a new customer.

    :return: JSON response containing the added customer information
    :rtype: JSON
    """
    customer = request.get_json()
    return jsonify(insert_customer(customer))

@app.route('/api/customers/update', methods=['PUT'])
def api_update_customer():
    """API endpoint to update customer information.

    :return: JSON response containing the updated customer information
    :rtype: JSON
    """
    customer = request.get_json()
    return jsonify(update_customer(customer))

@app.route('/api/customers/delete/<username>', methods=['DELETE'])
def api_delete_customer(username):
    """API endpoint to delete a customer based on the provided username.

    :param username: The username of the customer to be deleted
    :type username: str
    :return: JSON response containing the deleted customer confirmation message
    :rtype: JSON
    """
    return jsonify(delete_customer(username))

@app.route('/api/customers/charge', methods=['POST'])
def api_charge_customer():
    """API endpoint to charge a customer's wallet.

    :return: JSON response confirming the successful charge
    :rtype: JSON
    """
    data = request.get_json()
    username = data.get('username')
    amount = data.get('amount')

    customer = get_customer_by_username(username)

    if customer:
        new_balance = customer['wallet_balance'] + amount
        customer['wallet_balance'] = new_balance
        update_customer(customer)

        return jsonify({'message': f'Charged ${amount} to {username}. New balance: ${new_balance}'})
    else:
        return jsonify({'error': f'Customer with username {username} not found.'}), 404

@app.route('/api/customers/deduct', methods=['POST'])
def api_deduct_customer():
    """API endpoint to deduct an amount from a customer's wallet.

    :return: JSON response confirming the successful deduction.
    :rtype: JSON
    """
    data = request.get_json()
    username = data.get('username')
    amount = data.get('amount')

    customer = get_customer_by_username(username)

    if customer:
        if customer['wallet_balance'] >= amount:
            new_balance = customer['wallet_balance'] - amount
            customer['wallet_balance'] = new_balance
            update_customer(customer)

            return jsonify({'message': f'Deducted ${amount} from {username}. New balance: ${new_balance}'})
        else:
            return jsonify({'error': 'Insufficient funds.'}), 400
    else:
        return jsonify({'error': f'Customer with username {username} not found.'}), 404
    
@app.route('/api/customers/charge_goods', methods=['POST'])
def api_charge_goods():
    """API endpoint to charge a customer for goods.

    :return: JSON response confirming the successful charge for goods
    :rtype: JSON
    """
    data = request.get_json()
    username = data.get('username')
    amount = data.get('amount')

    # Make a request to the goods app to charge for goods
    goods_app_url = 'http://localhost:5001/api/goods/charge'
    goods_data = {'username': username, 'amount': amount}
    goods_response = requests.post(goods_app_url, json=goods_data)

    if goods_response.status_code == 200:
        # Goods charged successfully, you can do additional processing if needed
        return jsonify({'message': f'Goods charged successfully for {username}.'})
    else:
        # Handle error from goods app
        return jsonify({'error': f'Error charging goods for {username}. Check goods app.'}), goods_response.status_code

if __name__=="__main__":
    app.run(port=3000)