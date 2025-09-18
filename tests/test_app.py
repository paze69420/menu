import os
import sys
import pytest

# Ensure we can import from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app, db, MenuItem

# Neon test database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg2://user:password@your-neon-host/test_db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.app_context():
        db.create_all()  # ensure tables exist
        yield app.test_client()
        # Cleanup between tests
        db.session.rollback()
        db.session.remove()


def test_get_single_item(client):
    # Create item in DB
    item = MenuItem(name="TestItem", cuisine="TestCuisine")
    db.session.add(item)
    db.session.commit()

    # Fetch it via API
    response = client.get(f"/menu/{item.id}")
    assert response.status_code == 200

    data = response.get_json()
    assert data["id"] == item.id
    assert data["name"] == "TestItem"
    assert data["cuisine"] == "TestCuisine"


def test_add_new_item_and_retrieve(client):
    new_item = {"name": "AnotherItem", "cuisine": "AnotherCuisine"}

    # Create via POST
    post_response = client.post("/menu", json=new_item)
    assert post_response.status_code == 201

    created_item = post_response.get_json()
    item_id = created_item["id"]

    # Retrieve via GET
    get_response = client.get(f"/menu/{item_id}")
    assert get_response.status_code == 200

    data = get_response.get_json()
    assert data["name"] == "AnotherItem"
    assert data["cuisine"] == "AnotherCuisine"
