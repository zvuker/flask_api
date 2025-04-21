from flask import Flask, request, jsonify

app = Flask(__name__)

# БД
db = {
    "products": [
        {"id": 1, "name": "Smartphone", "price": 599.99, "stock": 100},
        {"id": 2, "name": "Laptop", "price": 1299.99, "stock": 50}
    ],
    "orders": []
}


# товары
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify({"products": db["products"]})


@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in db["products"] if p["id"] == product_id), None)
    return jsonify(product) if product else ("Not found", 404)


@app.route('/products', methods=['POST'])
def create_product():
    data = request.json
    new_id = max(p["id"] for p in db["products"]) + 1
    new_product = {
        "id": new_id,
        "name": data["name"],
        "price": data["price"],
        "stock": data["stock"]
    }
    db["products"].append(new_product)
    return jsonify(new_product), 201


@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    global db  # Явно указываем, что работаем с глобальной переменной

    index = next((i for i, p in enumerate(db["products"]) if p["id"] == product_id), None)

    if index is None:
        return jsonify({"error": "Product not found"}), 404

    deleted_product = db["products"].pop(index)

    return jsonify({
        "success": True,
        "message": "Product deleted",
        "deleted_product": deleted_product
    }), 200


@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = next((p for p in db["products"] if p["id"] == product_id), None)

    if not product:
        return jsonify({"success": False, "error": "Product not found"}), 404

    data = request.json
    if not all(k in data for k in ["name", "price", "stock"]):
        return jsonify({"success": False, "error": "Missing required fields"}), 400

    product.update({
        "name": data["name"],
        "price": float(data["price"]),
        "stock": int(data["stock"])
    })

    return jsonify({"success": True, "product": product})


@app.route('/products/<int:product_id>', methods=['PATCH'])
def partial_update_product(product_id):
    product = next((p for p in db["products"] if p["id"] == product_id), None)

    if not product:
        return jsonify({"success": False, "error": "Product not found"}), 404

    data = request.json
    if not data:
        return jsonify({"success": False, "error": "No data provided"}), 400

    if "name" in data:
        product["name"] = data["name"]
    if "price" in data:
        product["price"] = float(data["price"])
    if "stock" in data:
        product["stock"] = int(data["stock"])

    return jsonify({"success": True, "product": product})


# заказы
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    order_items = []

    for item in data["items"]:
        product = next(p for p in db["products"] if p["id"] == item["product_id"])
        order_items.append({
            "product_id": product["id"],
            "quantity": item["quantity"],
            "price": product["price"]
        })
        product["stock"] -= item["quantity"]

    new_order = {"id": len(db["orders"]) + 1, "items": order_items}
    db["orders"].append(new_order)
    return jsonify(new_order), 201


# сброс сервера
@app.route('/reset', methods=['POST'])
def reset():
    db["products"] = [
        {"id": 1, "name": "Smartphone", "price": 599.99, "stock": 100},
        {"id": 2, "name": "Laptop", "price": 1299.99, "stock": 50}
    ]
    db["orders"] = []
    return "Database reset", 200


if __name__ == '__main__':
    app.run(debug=True)

