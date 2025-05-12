from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Product, Inventory

inventory_bp = Blueprint('inventory', __name__)

# Route to get current stock of a product
@inventory_bp.route('/<int:product_id>', methods=['GET'])
@jwt_required()
def get_inventory(product_id):
    """
    Get the current inventory (stock) of a product by product ID.
    """
    product = Product.query.get_or_404(product_id)
    inventory = Inventory.query.filter_by(product_id=product.id).all()
    
    # Calculate the current stock by summing all inventory changes (if any)
    total_stock = sum(item.quantity_change for item in inventory)

    return jsonify({
        'product_id': product.id,
        'product_name': product.name,
        'current_stock': product.stock + total_stock
    })

# Route to update stock after an order
@inventory_bp.route('/update', methods=['POST'])
@jwt_required()
def update_inventory():
    """
    Update the inventory (stock) after an order is placed.
    This will decrease stock based on the products ordered.
    """
    data = request.get_json()
    product_id = data.get('product_id')
    quantity_change = data.get('quantity_change')  # Negative value for stock decrease

    if not product_id or not quantity_change:
        return jsonify({"msg": "Product ID and quantity change are required"}), 400

    product = Product.query.get_or_404(product_id)

    # Update stock and record in inventory
    product.stock += quantity_change
    db.session.add(Inventory(product_id=product.id, quantity_change=quantity_change))

    db.session.commit()

    return jsonify({
        "msg": f"Stock updated successfully for product {product.name}",
        "product_id": product.id,
        "new_stock": product.stock
    }), 200

