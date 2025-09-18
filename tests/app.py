from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
db = SQLAlchemy(app)

class MenuItem(db.Model):
    __tablename__ = "menu_items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    cuisine = db.Column(db.String(100))

@app.route('/menu', methods=['GET'])
def get_menu():
    items = MenuItem.query.all()
    return jsonify([{"id": i.id, "name": i.name, "cuisine": i.cuisine} for i in items])

@app.route('/menu/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = MenuItem.query.get(item_id)
    if not item:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"id": item.id, "name": item.name, "cuisine": item.cuisine})

@app.route('/menu', methods=['POST'])
def add_item():
    data = request.get_json()
    item = MenuItem(name=data["name"], cuisine=data["cuisine"])
    db.session.add(item)
    db.session.commit()
    return jsonify({"id": item.id, "name": item.name, "cuisine": item.cuisine}), 201

@app.route('/menu/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = MenuItem.query.get(item_id)
    if not item:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    item.name = data.get("name", item.name)
    item.cuisine = data.get("cuisine", item.cuisine)
    db.session.commit()
    return jsonify({"id": item.id, "name": item.name, "cuisine": item.cuisine})

@app.route('/menu/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = MenuItem.query.get(item_id)
    if not item:
        return jsonify({"error": "Not found"}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Deleted"})

if __name__ == '__main__':
    app.run(debug=True)
