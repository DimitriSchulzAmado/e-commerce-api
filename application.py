from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import (UserMixin, login_user, LoginManager,
                         login_required, logout_user, current_user)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

login_manager = LoginManager()
db = SQLAlchemy(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
CORS(app)


class User(db.Model, UserMixin):
    """ User model for authentication """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    cart = db.relationship('CartItem', backref='user', lazy=True)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Double, nullable=False)
    description = db.Column(db.Text, nullable=False)


class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(
        db.Integer, db.ForeignKey('product.id'),
        nullable=False
    )


# Product
# -----------------------------------------------------------------------------
@app.route("/api/products/add", methods=["POST"])
@login_required
def add_product():
    """ Add a new product to the database """
    data = request.json

    if 'name' in data and 'price' in data:
        product = Product(
            name=data["name"],
            price=data["price"],
            description=data.get("description", "")
        )
        db.session.add(product)
        db.session.commit()

        return jsonify({"message": "Product added successfully"})

    return jsonify({"error": "Invalid product data"}), 400


@app.route("/api/products/delete/<int:product_id>", methods=["DELETE"])
@login_required
def delete_product(product_id):
    """ Delete a product by its ID """
    product = Product.query.get(product_id)

    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted successfully"})

    return jsonify({"message": "Product not found"}), 404


@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product_details(product_id):
    """ Get details of a product by its ID """

    product = Product.query.get(product_id)

    if product:
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "description": product.description
        })

    return jsonify({"message": "Product not found"}), 404


@app.route("/api/products/update/<int:product_id>", methods=["PUT"])
@login_required
def update_product(product_id):
    """ Update a product by its ID """
    data = request.json
    product = Product.query.get(product_id)

    if not product:
        return jsonify({"message": "Product not found"}), 404

    if 'name' in data:
        product.name = data["name"]
    if 'price' in data:
        product.price = data["price"]
    if 'description' in data:
        product.description = data["description"]

    db.session.commit()
    return jsonify({"message": "Product updated successfully"})


@app.route("/api/products", methods=["GET"])
def get_products():
    """ Get all products """
    products = Product.query.all()

    product_list = []
    for product in products:
        product_list.append({
            "id": product.id,
            "name": product.name,
            "price": product.price
        })

    return jsonify(product_list)


# Autentication Endpoints
# -----------------------------------------------------------------------------
@login_manager.user_loader
def load_user(user_id):
    """ Load user for Flask-Login """
    return User.query.get(int(user_id))


@app.route("/api/login", methods=["POST"])
def login():
    """ User login endpoint """
    data = request.json
    user = User.query.filter_by(username=data.get("username")).first()
    
    if user and data.get("password") == user.password:
        login_user(user)
        return jsonify({"message": "Logged in successfully"})
        
    return jsonify({"message": "Unauthorized. Invalid credentials"}), 401


@app.route("/api/logout", methods=["POST"])
@login_required
def logout():
    """ User logout endpoint """

    logout_user()
    return jsonify({"message": "Logged out successfully"})


# Cart
# -----------------------------------------------------------------------------
@app.route("/api/cart/add/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id):
    """ Add a product to the user's cart """
    user = User.query.get(int(current_user.id))
    product = Product.query.get(product_id)

    if user and product:
        cart_item = CartItem(
            user_id=user,
            product_id=product
        )
        db.session.add(cart_item)
        db.session.commit()

        return jsonify({"message", "Item added to the cart successfully"})

    return jsonify({"message", "Failed to add item to the cart"}), 400


@app.route("/api/cart/remove/<int:item_id>", methods=["DELETE"])
@login_required
def delete_from_cart(project_id):
    """ Remove a product from the user's cart """
    cart_item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_id=project_id
    ).first()

    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({"message": "Item removed from the cart successfully"})

    return jsonify({"message": "Failed to remove item from the cart"}), 400


@app.route("/api/cart", methods=["GET"])
@login_required
def view_cart():
    """ View the user's cart """
    user = User.query.get(int(current_user.id))
    cart_items = user.cart

    cart_content = []
    for cart_item in cart_items:
        # fazer essa requisição fora do for, prezando a performance
        product = Product.query.get(cart_item.product_id)
        cart_content.append({
            "id": cart_item.id,
            "user_id": cart_item.user_id,
            "product_id": cart_item.product_id,
            "product_name": product.name,
            "product_price": product.price
        })

        return jsonify(cart_content)


@app.route("api/cart/checkout", methods=["POST"])
@login_required
def checkout():
    """ Checkout the user's cart and clear it """
    user = User.query.get(int(current_user.id))
    cart_items = user.cart

    for cart_item in cart_items:
        db.session.delete(cart_item)
    db.session.commit()

    return jsonify({"message": "Checkout successful. Cart has been cleared."})


# -----------------------------------------------------------------------------
@app.route("/")
def initial():
    return "API up and running!"


if __name__ == "__main__":
    app.run(debug=True)
