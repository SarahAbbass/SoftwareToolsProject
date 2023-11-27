import pytest
from inventory_service import app

@pytest.fixture
def client():
    """Pytest fixture to provide a Flask test client for API testing.

    :yield: A Flask test client
    """
    with app.test_client() as client:
        yield client

def test_api_get_goods(client):
    response = client.get('/api/goods')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_api_get_good(client):
    response = client.get('/api/goods/1')
    assert response.status_code == 200
    assert isinstance(response.json, dict)

def test_api_add_good(client):
    good_data = {
        "name": "Test Good", 
        "category": "Food",
        "price": 50.0, 
        "description": "Chocolate",
        "count": 10
        }
    response = client.post('/api/goods/add', json=good_data)
    assert response.status_code == 200
    assert isinstance(response.json, dict)

def test_api_update_good(client):
    good_data = {
        "name": "Test Good", 
        "category": "Drink",
        "price": 100.0, 
        "description": "Water",
        "count": 20
        }
    response = client.put('/api/goods/update', json=good_data)
    assert response.status_code == 200
    assert isinstance(response.json, dict)

def test_api_delete_good(client):
    response = client.delete('/api/goods/delete/1')
    assert response.status_code == 200
    assert isinstance(response.json, dict)