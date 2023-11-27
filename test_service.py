import pytest
from sales_service import app

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
    sale_data = {"good_name": "Test Good", "customer_username": "test_user"}
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
    sale_data = {"good_name": "Expensive Good", "customer_username": "test_user"}
    response = client.post('/api/sale', json=sale_data)
    assert response.status_code == 400
    assert "error" in response.json
