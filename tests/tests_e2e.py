import os
import json
os.environ["TESTING"] = "1"

from playwright.sync_api import sync_playwright

def test_crud_workflow():
    with sync_playwright() as p:
        request_context = p.request.new_context(base_url="http://127.0.0.1:5000")

        # GET /menu
        response = request_context.get("/menu")
        assert response.status == 200
        menu = response.json()
        assert isinstance(menu, list)

        # POST /menu
        new_item = {"name": "Pizza", "cuisine": "Italian"}
        response = request_context.post(
            "/menu",
            data=json.dumps(new_item),
            headers={"Content-Type": "application/json"}
        )
        assert response.status == 201
        added_item = response.json()
        item_id = added_item["id"]
        assert added_item["name"] == "Pizza"
        assert added_item["cuisine"] == "Italian"

        # GET /menu/:id
        response = request_context.get(f"/menu/{item_id}")
        assert response.status == 200
        fetched_item = response.json()
        assert fetched_item["name"] == "Pizza"

        # PUT /menu/:id
        response = request_context.put(
            f"/menu/{item_id}",
            data=json.dumps({"name": "Veg Pizza"}),
            headers={"Content-Type": "application/json"}
        )
        assert response.status == 200
        updated_item = response.json()
        assert updated_item["name"] == "Veg Pizza"

        # DELETE /menu/:id
        response = request_context.delete(f"/menu/{item_id}")
        assert response.status == 200

        # GET /menu/:id after deletion
        response = request_context.get(f"/menu/{item_id}")
        assert response.status == 404
