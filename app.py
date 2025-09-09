from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

menu_items = [
    {"id": 1, "name": "momo", "cuisine": "chinese"},
    {"id": 2, "name": "Sushi", "cuisine": "japanese"},
    {"id": 3, "name": "burger", "cuisine": "american"}
]


@app.route('/menu', methods=['GET']) 
def get_menu():                        
    return jsonify(menu_items) 
   
@app.route('/menu/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next ((i for i in menu_items if i['id'] == item_id), None)
    if item:
        return jsonify(item)
    return make_response(jsonify({"error": "Item not found"}), 404)

@app.route('/menu', methods=['POST'])
def add_single_item():
    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({"error": "Expected a single JSON object"}), 400
    data['id'] = max([i['id'] for i in menu_items], default=0) + 1
    menu_items.append(data)
    return jsonify(data), 201

@app.route('/menu/bulk', methods=['POST'])
def add_multiple_items():
    data = request.get_json()
    if not isinstance(data, list):
        return jsonify({"error": "Expected a list of JSON objects"}), 400
    new_items = []
    start_id = max([i['id'] for i in menu_items], default=0) + 1
    for idx, item in enumerate(data, start=start_id):
        item['id'] = idx
        menu_items.append(item)
        new_items.append(item)
    return jsonify(new_items), 201

@app.route('/menu/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = next((i for i in menu_items if i["id"] == item_id), None)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    menu_items.remove(item)
    return jsonify({"message": "Item deleted successfully"}), 200

@app.route('/menu/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = next((i for i in menu_items if i["id"] == item_id), None)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    data = request.get_json()
    if "name" in data:
        item["name"] = data["name"]
    if "cuisine" in data:
        item["cuisine"] = data["cuisine"]
    return jsonify(item), 200

if __name__ == '__main__':
    app.run(debug=True)


