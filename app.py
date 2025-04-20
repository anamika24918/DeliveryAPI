from flask import Flask, request, jsonify

app = Flask(__name__)

# Warehouse product mappings
warehouse_products = {
    "C1": ["A", "B", "C"],
    "C2": ["D", "E", "F"],
    "C3": ["G", "H", "I"]
}

# Distances from each center to L1
distances = {
    "C1": 10,
    "C2": 20,
    "C3": 30
}

def calculate_cost(order):
    required_centers = set()

    for center, products in warehouse_products.items():
        if any(order.get(p, 0) > 0 for p in products):
            required_centers.add(center)

    # Try starting from each center and calculate cost
    min_cost = float("inf")
    for start in required_centers:
        visited = [start]
        cost = 0

        # First delivery from starting center
        cost += 2 * distances[start]

        # Visit remaining centers
        for center in required_centers:
            if center == start:
                continue
            # Pickup and drop again
            cost += 2 * distances[center]

        min_cost = min(min_cost, cost)

    return min_cost if required_centers else 0

@app.route("/calculate", methods=["POST"])
def calculate():
    order = request.get_json()
    cost = calculate_cost(order)
    return jsonify({"minimum_cost": cost})

if __name__ == "__main__":
    app.run(debug=True)