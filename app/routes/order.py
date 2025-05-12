from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Order, OrderItem, Product, Inventory

order_bp = Blueprint('order', __name__)

@order_bp.route('/', methods=['POST'])
@jwt_required()
def place_order():
    data = request.get_json()
    items = data.get('items')  # [{"product_id": 1, "quantity": 2}, ...]
    paid = data.get('paid', False)

    if not items or not isinstance(items, list):
        return jsonify({"msg": "Invalid items"}), 400

    user = get_jwt_identity()
    order = Order(customer_id=user['id'], paid=paid)
    db.session.add(order)
    db.session.flush()

    for item in items:
        product = Product.query.get(item['product_id'])
        if not product or product.stock < item['quantity']:
            db.session.rollback()
            return jsonify({"msg": f"Product {item['product_id']} unavailable or insufficient stock"}), 400

        product.stock -= item['quantity']
        db.session.add(Inventory(product_id=product.id, quantity_change=-item['quantity']))

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item['quantity'],
            price=product.price
        )
        db.session.add(order_item)

    db.session.commit()
    return jsonify({"msg": "Order placed successfully", "order_id": order.id}), 201

@order_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_invoice(order_id):
    order = Order.query.get_or_404(order_id)
    items = [
        {
            "product_id": item.product_id,
            "quantity": item.quantity,
            "price": item.price
        } for item in order.items
    ]
    return jsonify({
        "order_id": order.id,
        "customer_id": order.customer_id,
        "paid": order.paid,
        "order_date": order.order_date,
        "items": items
    })