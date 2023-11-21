import pytest
from customers_service import app

@pytest.fixture
def client():
    """Pytest fixture to provide a Flask test client for API testing.

    :yield: A Flask test client
    """
    with app.test_client() as client:
        yield client

def test_api_get_customers(client):
    """Test the 'api_get_customers' API endpoint.

    :param client: The Flask test client
    """
    response = client.get('/api/customers')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_api_get_customer(client):
    """Test the 'api_get_customer' API endpoint.

    :param client: The Flask test client
    """
    response = client.get('/api/customers/SaraA')
    assert response.status_code == 200
    assert isinstance(response.json, dict)

def test_api_add_customer(client):
    """Test the 'api_add_customer' API endpoint.

    :param client: The Flask test client
    """
    customer_data = {"full_name": "Test User", 
                     "username": "test_user", 
                     "password": "password", 
                     "address": "Beirut, Lebanon",
                     "age": 30,
                     "gender": "Female",
                     "marital_status": "Single", 
                     "wallet_balance": 100}
    response = client.post('/api/customers/add', json=customer_data)
    assert response.status_code == 200
    assert isinstance(response.json, dict)

def test_api_update_customer(client):
    """Test the 'api_update_customer' API endpoint.

    :param client: The Flask test client
    """
    customer_data = {"username": "FirasA", "wallet_balance": 150}
    response = client.put('/api/customers/update', json=customer_data)
    assert response.status_code == 200
    assert isinstance(response.json, dict)

def test_api_delete_customer(client):
    """Test the 'api_delete_customer' API endpoint.

    :param client: The Flask test client
    """
    response = client.delete('/api/customers/delete/username')
    assert response.status_code == 200
    assert isinstance(response.json, dict)

def test_api_charge_customer(client):
    """Test the 'api_charge_customer' API endpoint.

    :param client: The Flask test client
    """
    charge_data = {"username": "test_user", "amount": 50}
    response = client.post('/api/customers/charge', json=charge_data)
    assert response.status_code == 200
    assert isinstance(response.json, dict)

def test_api_deduct_customer(client):
    """Test the 'api_deduct_customer' API endpoint.

    :param client: The Flask test client
    """
    deduct_data = {"username": "test_user", "amount": 30}
    response = client.post('/api/customers/deduct', json=deduct_data)
    assert response.status_code == 200
    assert isinstance(response.json, dict)

def test_api_charge_customer_not_found(client):
    """Test the 'api_charge_customer' API endpoint with a non-existent user.

    :param client: The Flask test client
    """
    charge_data = {"username": "nonexistent_user", "amount": 50}
    response = client.post('/api/customers/charge', json=charge_data)
    assert response.status_code == 404
    assert "error" in response.json

def test_api_deduct_insufficient_funds(client):
    """Test the 'api_deduct_customer' API endpoint with insufficient funds.

    :param client: The Flask test client
    """
    deduct_data = {"username": "test_user", "amount": 200}
    response = client.post('/api/customers/deduct', json=deduct_data)
    assert response.status_code == 400
    assert "error" in response.json
