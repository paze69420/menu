import json
import pytest
from app import app
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

def test_get_single_item(client):
    response = client.get("/menu/1")      
    assert response.status_code == 200    
    data = response.get_json()            
    assert data["id"] == 1                

def test_add_new_item_and_retrieve(client):
    new_item = {"name": "test_item", "cuisine": "test_cuisine"}
    post_response = client.post("/menu", json=new_item)
    assert post_response.status_code == 201
    created_item = post_response.get_json()
    new_id = created_item['id']
    get_response = client.get(f"/menu/{new_id}")
    assert get_response.status_code == 200
    data = get_response.get_json()
    assert data["name"] == "test_item"
    assert data["cuisine"] == "test_cuisine"

