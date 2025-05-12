from flask import Blueprint, request, jsonify
from app.models import Product, ProductCategory, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.decorators import role_required

product_bp = Blueprint('product', __name__)

# ------------------------
# CATEGORY CRUD (Admin only)
# ------------------------

@product_bp.route('/categories', methods=['POST'])
@jwt_required()
@role_required('admin')
def create_category():
    data = request.get_json()
    name = data.get('name')
    if ProductCategory.query.filter_by(name=name).first():
        return jsonify({'msg': 'Category already exists'}), 409

    category = ProductCategory(name=name)
    db.session.add(category)
    db.session.commit()
    return jsonify({'msg': 'Category created'}), 201

@product_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    categories = ProductCategory.query.all()
    return jsonify([{'id': c.id, 'name': c.name} for c in categories]), 200

@product_bp.route('/categories/<int:category_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_category(category_id):
    data = request.get_json()
    category = ProductCategory.query.get_or_404(category_id)
    category.name = data.get('name', category.name)
    db.session.commit()
    return jsonify({'msg': 'Category updated'}), 200

@product_bp.route('/categories/<int:category_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_category(category_id):
    category = ProductCategory.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'msg': 'Category deleted'}), 200

# ------------------------
# PRODUCT CRUD (Admin, Seller)
# ------------------------

@product_bp.route('', methods=['POST'])
@jwt_required()
@role_required('admin', 'seller')
def create_product():
    data = request.get_json()
    identity = get_jwt_identity()
    product = Product(
        name=data.get('name'),
        category_id=data.get('category_id'),
        price=data.get('price'),
        stock=data.get('stock', 0),
        seller_id=identity['id']
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({'msg': 'Product created'}), 201

@product_bp.route('', methods=['GET'])
@jwt_required()
def list_products():
    products = Product.query.all()
    result = []
    for p in products:
        result.append({
            'id': p.id,
            'name': p.name,
            'price': p.price,
            'stock': p.stock,
            'category_id': p.category_id,
            'seller_id': p.seller_id
        })
    return jsonify(result), 200

@product_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
@role_required('admin', 'seller')
def update_product(product_id):
    identity = get_jwt_identity()
    product = Product.query.get_or_404(product_id)

    if identity['role'] == 'seller' and product.seller_id != identity['id']:
        return jsonify({"msg": "Not allowed"}), 403

    data = request.get_json()
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.stock = data.get('stock', product.stock)
    product.category_id = data.get('category_id', product.category_id)
    db.session.commit()
    return jsonify({'msg': 'Product updated'}), 200

@product_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin', 'seller')
def delete_product(product_id):
    identity = get_jwt_identity()
    product = Product.query.get_or_404(product_id)

    if identity['role'] == 'seller' and product.seller_id != identity['id']:
        return jsonify({"msg": "Not allowed"}), 403

    db.session.delete(product)
    db.session.commit()
    return jsonify({'msg': 'Product deleted'}), 200
