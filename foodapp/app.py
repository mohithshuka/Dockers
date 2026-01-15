"""
Food Delivery Web Application
Main Flask application file with all routes and business logic
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
from datetime import datetime
from models import db, User, FoodItem, Order, OrderItem

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food_delivery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Create tables and add sample data
with app.app_context():
    db.create_all()
    
    # Add admin user if not exists
    if not User.query.filter_by(email='admin@food.com').first():
        admin = User(
            name='Admin',
            email='admin@food.com',
            password=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
    
    # Add sample food items if database is empty
    if FoodItem.query.count() == 0:
        sample_foods = [
            FoodItem(name='Margherita Pizza', price=230, category='Pizza', 
                    description='Classic pizza with tomato sauce and mozzarella', 
                    image='pizza.jpg'),
            FoodItem(name='Cheeseburger', price=150, category='Burger', 
                    description='Juicy beef patty with cheese and vegetables', 
                    image='Burger.jpg'),
            FoodItem(name='Caesar Salad', price=200, category='Salad', 
                    description='Fresh romaine lettuce with caesar dressing', 
                    image='salad.jpg'),
            FoodItem(name='Pasta Carbonara', price=250, category='Pasta', 
                    description='Creamy pasta with bacon and parmesan', 
                    image='pasta.jpg'),
            FoodItem(name='Chicken Wings', price=300, category='Chicken', 
                    description='Crispy chicken wings with spicy sauce', 
                    image='Chickenwings.jpg'),
            FoodItem(name='Chocolate Cake', price=150, category='Dessert', 
                    description='Rich chocolate cake with frosting', 
                    image='Chocolatecake.jpg'),
        ]
        db.session.bulk_save_objects(sample_foods)
        db.session.commit()

# Decorator to require login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator to require admin access
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            flash('Admin access required', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# HOME PAGE - Display all food items
@app.route('/')
def index():
    search_query = request.args.get('search', '')
    category = request.args.get('category', '')
    
    # Build query
    query = FoodItem.query
    
    # Apply search filter
    if search_query:
        query = query.filter(FoodItem.name.contains(search_query))
    
    # Apply category filter
    if category:
        query = query.filter_by(category=category)
    
    food_items = query.all()
    categories = db.session.query(FoodItem.category).distinct().all()
    categories = [c[0] for c in categories]
    
    return render_template('index.html', 
                         food_items=food_items, 
                         categories=categories,
                         search_query=search_query,
                         selected_category=category)

# USER REGISTRATION
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not all([name, email, password, confirm_password]):
            flash('All fields are required', 'danger')
            return redirect(url_for('register'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))
        
        # Check if user already exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))
        
        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# USER LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['is_admin'] = user.is_admin
            
            flash(f'Welcome back, {user.name}!', 'success')
            
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

# USER LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'info')
    return redirect(url_for('index'))

# ADD TO CART
@app.route('/add_to_cart/<int:food_id>')
@login_required
def add_to_cart(food_id):
    # Initialize cart in session if not exists
    if 'cart' not in session:
        session['cart'] = {}
    
    cart = session['cart']
    food_id_str = str(food_id)
    
    # Add or increment quantity
    if food_id_str in cart:
        cart[food_id_str] += 1
    else:
        cart[food_id_str] = 1
    
    session['cart'] = cart
    flash('Item added to cart', 'success')
    return redirect(url_for('index'))

# VIEW CART
@app.route('/cart')
@login_required
def cart():
    cart_items = []
    total = 0
    
    if 'cart' in session and session['cart']:
        for food_id, quantity in session['cart'].items():
            food = FoodItem.query.get(int(food_id))
            if food:
                subtotal = food.price * quantity
                cart_items.append({
                    'food': food,
                    'quantity': quantity,
                    'subtotal': subtotal
                })
                total += subtotal
    
    return render_template('cart.html', cart_items=cart_items, total=total)

# UPDATE CART QUANTITY
@app.route('/update_cart/<int:food_id>/<action>')
@login_required
def update_cart(food_id, action):
    if 'cart' in session:
        cart = session['cart']
        food_id_str = str(food_id)
        
        if food_id_str in cart:
            if action == 'increase':
                cart[food_id_str] += 1
            elif action == 'decrease':
                cart[food_id_str] -= 1
                if cart[food_id_str] <= 0:
                    del cart[food_id_str]
        
        session['cart'] = cart
    
    return redirect(url_for('cart'))

# REMOVE FROM CART
@app.route('/remove_from_cart/<int:food_id>')
@login_required
def remove_from_cart(food_id):
    if 'cart' in session:
        cart = session['cart']
        food_id_str = str(food_id)
        
        if food_id_str in cart:
            del cart[food_id_str]
        
        session['cart'] = cart
    
    return redirect(url_for('cart'))

# PLACE ORDER
@app.route('/place_order', methods=['POST'])
@login_required
def place_order():
    if 'cart' not in session or not session['cart']:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('cart'))
    
    # Calculate total
    total = 0
    for food_id, quantity in session['cart'].items():
        food = FoodItem.query.get(int(food_id))
        if food:
            total += food.price * quantity
    
    # Create order
    order = Order(
        user_id=session['user_id'],
        total_amount=total,
        status='Pending'
    )
    db.session.add(order)
    db.session.commit()
    
    # Create order items
    for food_id, quantity in session['cart'].items():
        food = FoodItem.query.get(int(food_id))
        if food:
            order_item = OrderItem(
                order_id=order.id,
                food_id=food.id,
                quantity=quantity,
                price=food.price
            )
            db.session.add(order_item)
    
    db.session.commit()
    
    # Clear cart
    session['cart'] = {}
    
    flash('Order placed successfully!', 'success')
    return redirect(url_for('order_confirmation', order_id=order.id))

# ORDER CONFIRMATION PAGE
@app.route('/order_confirmation/<int:order_id>')
@login_required
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Check if order belongs to current user
    if order.user_id != session['user_id']:
        flash('Access denied', 'danger')
        return redirect(url_for('index'))
    
    return render_template('order_confirmation.html', order=order)

# ORDER HISTORY
@app.route('/orders')
@login_required
def orders():
    user_orders = Order.query.filter_by(user_id=session['user_id']).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=user_orders)

# ADMIN DASHBOARD
@app.route('/admin')
@admin_required
def admin_dashboard():
    food_items = FoodItem.query.all()
    total_orders = Order.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
    
    return render_template('admin_dashboard.html', 
                         food_items=food_items,
                         total_orders=total_orders,
                         total_revenue=total_revenue)

# ADMIN - ADD FOOD ITEM
@app.route('/admin/add_food', methods=['GET', 'POST'])
@admin_required
def add_food():
    if request.method == 'POST':
        name = request.form.get('name')
        price = float(request.form.get('price'))
        category = request.form.get('category')
        description = request.form.get('description')
        image = request.form.get('image', 'default.jpg')
        
        new_food = FoodItem(
            name=name,
            price=price,
            category=category,
            description=description,
            image=image
        )
        db.session.add(new_food)
        db.session.commit()
        
        flash('Food item added successfully', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('add_food.html')

# ADMIN - EDIT FOOD ITEM
@app.route('/admin/edit_food/<int:food_id>', methods=['GET', 'POST'])
@admin_required
def edit_food(food_id):
    food = FoodItem.query.get_or_404(food_id)
    
    if request.method == 'POST':
        food.name = request.form.get('name')
        food.price = float(request.form.get('price'))
        food.category = request.form.get('category')
        food.description = request.form.get('description')
        food.image = request.form.get('image')
        
        db.session.commit()
        flash('Food item updated successfully', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('edit_food.html', food=food)

# ADMIN - DELETE FOOD ITEM
@app.route('/admin/delete_food/<int:food_id>')
@admin_required
def delete_food(food_id):
    food = FoodItem.query.get_or_404(food_id)
    db.session.delete(food)
    db.session.commit()
    
    flash('Food item deleted successfully', 'success')
    return redirect(url_for('admin_dashboard'))

# ADMIN - VIEW ALL ORDERS
@app.route('/admin/orders')
@admin_required
def admin_orders():
    all_orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin_orders.html', orders=all_orders)

# ADMIN - UPDATE ORDER STATUS
@app.route('/admin/update_order_status/<int:order_id>/<status>')
@admin_required
def update_order_status(order_id, status):
    order = Order.query.get_or_404(order_id)
    order.status = status
    db.session.commit()
    
    flash('Order status updated', 'success')
    return redirect(url_for('admin_orders'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)