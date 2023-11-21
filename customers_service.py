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

@app.route('/api/customers/charge', methods=['POST'])
def api_charge_customer():
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

if __name__=="__main__":
    app.run()