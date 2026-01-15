# 🏗️ Food Delivery App - Architecture Guide

## 📐 System Architecture Overview

This application follows the **MVC (Model-View-Controller)** pattern adapted for Flask:

```
┌─────────────────────────────────────────────────────┐
│                    USER BROWSER                     │
│                  (Chrome, Firefox)                  │
└───────────────────┬─────────────────────────────────┘
                    │ HTTP Request
                    ▼
┌─────────────────────────────────────────────────────┐
│                  FLASK APPLICATION                  │
│  ┌─────────────────────────────────────────────┐   │
│  │          ROUTES (Controller Layer)          │   │
│  │  app.py - Handles requests & responses      │   │
│  └────────────┬──────────────────┬──────────────┘   │
│               │                  │                  │
│      ┌────────▼────────┐  ┌─────▼─────────┐        │
│      │  MODELS (Data)  │  │ TEMPLATES     │        │
│      │  models.py      │  │ (View Layer)  │        │
│      │  SQLAlchemy     │  │ Jinja2 HTML   │        │
│      └────────┬────────┘  └───────────────┘        │
└───────────────┼─────────────────────────────────────┘
                │
        ┌───────▼────────┐
        │  SQLite DB     │
        │ food_delivery  │
        └────────────────┘
```

## 🧩 Component Breakdown

### 1. **Entry Point: `app.py`**

This is the heart of the application. It contains:

#### a. Flask Initialization
```python
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'  # For sessions
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food_delivery.db'
```

#### b. Route Handlers (Controllers)
Each route is a function that:
- Receives HTTP request
- Processes data
- Interacts with database
- Returns HTML response

**Example Flow:**
```python
@app.route('/cart')
@login_required              # 1. Check if user is logged in
def cart():
    cart_items = []           # 2. Initialize data structure
    
    if 'cart' in session:     # 3. Get cart from session
        for food_id, qty in session['cart'].items():
            food = FoodItem.query.get(food_id)  # 4. Query database
            cart_items.append({...})            # 5. Prepare data
    
    return render_template('cart.html', cart_items=cart_items)  # 6. Render view
```

#### c. Decorators (Middleware)
```python
@login_required    # Ensures user is authenticated
@admin_required    # Ensures user is admin
```

These wrap functions to add authentication checks.

### 2. **Data Layer: `models.py`**

Defines database structure using SQLAlchemy ORM:

#### Database Models
```python
User ──┐
       │ has many
       └──> Order ──┐
                    │ has many
                    └──> OrderItem ──> FoodItem
```

**Key Concepts:**

**a. Table Definition**
```python
class User(db.Model):
    __tablename__ = 'users'  # Actual table name in database
    id = db.Column(db.Integer, primary_key=True)  # Auto-increment ID
    email = db.Column(db.String(120), unique=True)  # Unique constraint
```

**b. Relationships**
```python
class Order(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # This creates a convenient 'order.user' property
    # Also creates 'user.orders' on User model (backref)
    user = db.relationship('User', backref='orders')
```

**c. Cascade Deletes**
```python
orders = db.relationship('Order', cascade='all, delete-orphan')
# If user is deleted, all their orders are deleted too
```

### 3. **View Layer: `templates/`**

HTML files with Jinja2 templating:

#### Template Inheritance
```html
<!-- base.html - Parent template -->
<html>
  <head>...</head>
  <body>
    <nav>...</nav>
    {% block content %}{% endblock %}  <!-- Child content goes here -->
    <footer>...</footer>
  </body>
</html>

<!-- index.html - Child template -->
{% extends "base.html" %}
{% block content %}
  <h1>Food Menu</h1>
  <!-- This content replaces the block in base.html -->
{% endblock %}
```

#### Jinja2 Features Used
```html
<!-- Variables -->
{{ food.name }}  → Outputs: "Pizza"

<!-- Filters -->
{{ "%.2f"|format(price) }}  → Outputs: "12.99"

<!-- Control Structures -->
{% if user_logged_in %}
  <a href="/logout">Logout</a>
{% else %}
  <a href="/login">Login</a>
{% endif %}

{% for item in items %}
  <div>{{ item.name }}</div>
{% endfor %}

<!-- URL Generation -->
{{ url_for('index') }}  → Outputs: "/"
{{ url_for('cart') }}   → Outputs: "/cart"
```

## 🔄 Request-Response Flow

### Example: Adding Item to Cart

```
1. USER CLICKS "Add to Cart"
   └─> Sends GET request to /add_to_cart/1

2. FLASK RECEIVES REQUEST
   └─> Matches route: @app.route('/add_to_cart/<int:food_id>')

3. DECORATOR CHECKS (@login_required)
   └─> Verifies 'user_id' in session
   └─> If not logged in: redirect to /login
   └─> If logged in: continue

4. FUNCTION EXECUTES
   └─> Get cart from session: session['cart']
   └─> Add/increment item: cart['1'] = 2
   └─> Save to session: session['cart'] = cart
   └─> Flash message: "Item added"

5. REDIRECT TO HOME
   └─> return redirect(url_for('index'))

6. RENDER HOME PAGE
   └─> Query all food items
   └─> Pass to template
   └─> Jinja2 generates HTML
   └─> Send HTML to browser
```

## 🗄️ Database Operations

### CRUD Examples

#### Create (Insert)
```python
new_user = User(name='John', email='john@email.com', password='hashed')
db.session.add(new_user)
db.session.commit()
```

#### Read (Query)
```python
# Get all
users = User.query.all()

# Get by ID
user = User.query.get(1)

# Filter
admins = User.query.filter_by(is_admin=True).all()

# Complex filter
orders = Order.query.filter(Order.total_amount > 50).all()
```

#### Update
```python
user = User.query.get(1)
user.name = 'New Name'
db.session.commit()  # No need to add() for existing objects
```

#### Delete
```python
user = User.query.get(1)
db.session.delete(user)
db.session.commit()
```

## 🔐 Authentication Flow

### Session-Based Authentication

```
┌─────────────────────────────────────────┐
│         LOGIN PROCESS                   │
└─────────────────────────────────────────┘
1. User submits login form
2. Query database for user by email
3. Verify password with check_password_hash()
4. Store user data in session:
   session['user_id'] = user.id
   session['user_name'] = user.name
5. Session cookie sent to browser
6. Browser includes cookie in all requests

┌─────────────────────────────────────────┐
│      PROTECTED ROUTE ACCESS             │
└─────────────────────────────────────────┘
1. User requests /cart
2. @login_required decorator checks session
3. If 'user_id' in session: allow access
4. If not: redirect to /login
```

### Password Security
```python
# Registration
hashed = generate_password_hash('password123')
# Stores: pbkdf2:sha256:260000$abc...xyz

# Login
is_valid = check_password_hash(stored_hash, entered_password)
# Returns: True or False
```

## 🛒 Cart System Architecture

### Session-Based Cart

```python
# Cart structure in session
session['cart'] = {
    '1': 3,   # food_id: quantity
    '5': 2,
    '12': 1
}
```

**Why Session?**
- Persists across requests
- No database writes for browsing
- Cleared when user logs out
- Simple to implement

**Cart Operations:**

```python
# Add to cart
cart = session.get('cart', {})
cart[food_id] = cart.get(food_id, 0) + 1
session['cart'] = cart

# Update quantity
cart[food_id] += 1  # increase
cart[food_id] -= 1  # decrease

# Remove item
del cart[food_id]

# Clear cart
session['cart'] = {}
```

## 📦 Order Processing Flow

```
┌─────────────────────────────────────────┐
│      PLACE ORDER WORKFLOW               │
└─────────────────────────────────────────┘

1. USER CLICKS "Place Order"
   └─> POST to /place_order

2. VALIDATE CART
   └─> Check cart not empty
   └─> Calculate total price

3. CREATE ORDER RECORD
   └─> order = Order(user_id=..., total=..., status='Pending')
   └─> db.session.add(order)
   └─> db.session.commit()  # Gets order.id

4. CREATE ORDER ITEMS
   └─> For each item in cart:
       └─> order_item = OrderItem(order_id=order.id, ...)
       └─> db.session.add(order_item)
   └─> db.session.commit()

5. CLEAR CART
   └─> session['cart'] = {}

6. REDIRECT TO CONFIRMATION
   └─> /order_confirmation/<order_id>
```

## 🎨 Frontend Architecture

### Bootstrap Grid System

```html
<div class="container">           <!-- Max-width container -->
  <div class="row">                <!-- Flexbox row -->
    <div class="col-md-6">         <!-- 6/12 columns on medium+ screens -->
      Content here
    </div>
    <div class="col-md-6">         <!-- Another 6/12 columns -->
      More content
    </div>
  </div>
</div>
```

**Responsive Breakpoints:**
- `col-` = Extra small (< 576px)
- `col-sm-` = Small (≥ 576px)
- `col-md-` = Medium (≥ 768px)
- `col-lg-` = Large (≥ 992px)

### Component Structure

```html
<!-- Food Card Component -->
<div class="card food-card">              <!-- Bootstrap card -->
  <img class="card-img-top">              <!-- Image -->
  <div class="card-body">                 <!-- Content area -->
    <h5 class="card-title">Food Name</h5>
    <p class="card-text">Description</p>
    <button class="btn">Add to Cart</button>
  </div>
</div>
```

## 🔍 Search & Filter Implementation

```python
# Build dynamic query
query = FoodItem.query

# Add search filter if provided
if search_query:
    query = query.filter(FoodItem.name.contains(search_query))
    # SQL: WHERE name LIKE '%search_query%'

# Add category filter if provided
if category:
    query = query.filter_by(category=category)
    # SQL: WHERE category = 'category'

# Execute query
food_items = query.all()
```

## 🚀 Performance Considerations

### Database Queries
```python
# ❌ Bad: N+1 Query Problem
orders = Order.query.all()
for order in orders:
    print(order.user.name)  # Queries database for each order!

# ✅ Good: Eager Loading
orders = Order.query.options(db.joinedload('user')).all()
# Single query with JOIN
```

### Session Storage
- Cart stored in session (client-side cookie)
- Limited to ~4KB
- Automatically encrypted
- No database load for cart operations

## 🔄 State Management

### Application State
```
Session (Client) ────> Flask (Server) ────> Database
     │                     │                     │
   cart: {}            processes              persistent
   user_id: 1          requests               data storage
   is_admin: False     validates
```

### State Flow
1. **Session**: Temporary user data (cart, auth)
2. **Request Context**: Available during request
3. **Database**: Permanent storage

## 🏛️ Design Patterns Used

### 1. **MVC Pattern**
- **Model**: `models.py` (Data)
- **View**: `templates/` (Presentation)
- **Controller**: `app.py` routes (Logic)

### 2. **Decorator Pattern**
```python
@login_required  # Wraps function with authentication
def protected_route():
    pass
```

### 3. **Template Method Pattern**
```html
<!-- base.html defines structure -->
{% block content %}{% endblock %}

<!-- Children implement specific content -->
```

### 4. **Repository Pattern**
```python
# SQLAlchemy acts as repository
User.query.all()  # Abstract away SQL
```

## 🎯 Extension Points

To add new features:

### 1. Add New Route
```python
@app.route('/new-feature')
def new_feature():
    return render_template('new_feature.html')
```

### 2. Add New Model
```python
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food_items.id'))
    rating = db.Column(db.Integer)
```

### 3. Add New Template
```html
{% extends "base.html" %}
{% block content %}
  <!-- Your content -->
{% endblock %}
```

## 📚 Further Reading

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/14/orm/)
- [Jinja2 Templates](https://jinja.palletsprojects.com/)
- [Bootstrap 5](https://getbootstrap.com/docs/5.3/)

---

This architecture provides a solid foundation for a production-ready food delivery application while remaining easy to understand and extend.