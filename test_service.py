import pytest
from sales_service import app
from create_postgres_db import insert_good, insert_customer

@pytest.fixture
def client():
    """Pytest fixture to provide a Flask test client for API testing.

    :yield: A Flask test client
    """
    with app.test_client() as client:
        yield client

def test_api_get_goods(client):
    response = client.get('/api/get_goods')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_api_get_good(client):
    response = client.get('/api/good/1')
    assert response.status_code == 200
    assert isinstance(response.json, dict)

def test_api_make_sale(client):
    good_data = {
        "name": "Sold Good", 
        "category": "Food",
        "price": 50.0, 
        "description": "Chocolate",
        "count": 10
        }
    insert_good(good_data)
    customer_data = {
    "full_name": "test",
    "username": "testing", 
    "password": "testing",
    "address": "Beirut, Lebanon",
    "age": 50,
    "gender": "Male",
    "marital_status": "Single",
    "wallet_balance": 1000.0
        }
    insert_customer(customer_data)
    sale_data = {"good_name": "Sold Good", "customer_username": "testing"}
    response = client.post('/api/sale', json=sale_data)
    assert response.status_code == 200
    assert isinstance(response.json, dict)

def test_api_make_sale_invalid_request(client):
    response = client.post('/api/sale', json={})
    assert response.status_code == 400
    assert "error" in response.json

def test_api_make_sale_customer_not_found(client):
    sale_data = {"good_name": "Test Good", "customer_username": "nonexistent_user"}
    response = client.post('/api/sale', json=sale_data)
    assert response.status_code == 404
    assert "error" in response.json

def test_api_make_sale_good_not_found(client):
    sale_data = {"good_name": "Nonexistent Good", "customer_username": "test_user"}
    response = client.post('/api/sale', json=sale_data)
    assert response.status_code == 404
    assert "error" in response.json

def test_api_make_sale_insufficient_funds(client):
    good_data = {
    "name": "Expensive Good",
    "category": "Food", 
    "price": 10000,
    "description": "Caviar",
    "count": 22
    }
    insert_good(good_data)
    sale_data = {"good_name": "Expensive Good", "customer_username": "test_user"}
    response = client.post('/api/sale', json=sale_data)
    assert response.status_code == 400
    assert "error" in response.json

def test_api_make_sale_insufficient_goods(client):
    good_data = {
    "name": "Restock Good",
    "category": "Dairy", 
    "price": 10,
    "description": "Milk",
    "count": 0
    }
    insert_good(good_data)
    sale_data = {"good_name": "Restock Good", "customer_username": "test_user"}
    response = client.post('/api/sale', json=sale_data)
    assert response.status_code == 400
    assert "error" in response.json