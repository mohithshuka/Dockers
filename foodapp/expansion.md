# 🚀 Extension Guide - Adding New Features

This guide shows you how to extend the Food Delivery App with new features.

## 📝 Example 1: Add User Reviews

### Step 1: Create Review Model

Add to `models.py`:

```python
class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food_items.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='reviews')
    food_item = db.relationship('FoodItem', backref='reviews')
```

### Step 2: Add Routes

Add to `app.py`:

```python
@app.route('/add_review/<int:food_id>', methods=['GET', 'POST'])
@login_required
def add_review(food_id):
    food = FoodItem.query.get_or_404(food_id)
    
    if request.method == 'POST':
        rating = int(request.form.get('rating'))
        comment = request.form.get('comment')
        
        review = Review(
            user_id=session['user_id'],
            food_id=food_id,
            rating=rating,
            comment=comment
        )
        db.session.add(review)
        db.session.commit()
        
        flash('Review added successfully', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_review.html', food=food)

@app.route('/food/<int:food_id>')
def food_detail(food_id):
    food = FoodItem.query.get_or_404(food_id)
    reviews = Review.query.filter_by(food_id=food_id).all()
    
    # Calculate average rating
    avg_rating = 0
    if reviews:
        total = sum(r.rating for r in reviews)
        avg_rating = total / len(reviews)
    
    return render_template('food_detail.html', 
                         food=food, 
                         reviews=reviews,
                         avg_rating=avg_rating)
```

### Step 3: Create Templates

Create `templates/add_review.html`:

```html
{% extends "base.html" %}

{% block content %}
<div class="container my-5">
    <h2>Review {{ food.name }}</h2>
    
    <form method="POST">
        <div class="mb-3">
            <label class="form-label">Rating</label>
            <select name="rating" class="form-select" required>
                <option value="">Select rating</option>
                <option value="5">⭐⭐⭐⭐⭐ Excellent</option>
                <option value="4">⭐⭐⭐⭐ Good</option>
                <option value="3">⭐⭐⭐ Average</option>
                <option value="2">⭐⭐ Poor</option>
                <option value="1">⭐ Terrible</option>
            </select>
        </div>
        
        <div class="mb-3">
            <label class="form-label">Comment</label>
            <textarea name="comment" class="form-control" rows="4"></textarea>
        </div>
        
        <button type="submit" class="btn btn-primary">Submit Review</button>
    </form>
</div>
{% endblock %}
```

### Step 4: Update Database

```python
# In terminal
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
```

---

## 🎫 Example 2: Add Coupon System

### Step 1: Create Coupon Model

```python
class Coupon(db.Model):
    __tablename__ = 'coupons'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    discount_percent = db.Column(db.Float, nullable=False)
    max_uses = db.Column(db.Integer, default=1)
    used_count = db.Column(db.Integer, default=0)
    expires_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    def is_valid(self):
        if not self.is_active:
            return False, "Coupon is not active"
        if self.used_count >= self.max_uses:
            return False, "Coupon has been fully used"
        if self.expires_at and datetime.utcnow() > self.expires_at:
            return False, "Coupon has expired"
        return True, "Valid"
```

### Step 2: Add Apply Coupon Route

```python
@app.route('/apply_coupon', methods=['POST'])
@login_required
def apply_coupon():
    code = request.form.get('coupon_code').upper()
    coupon = Coupon.query.filter_by(code=code).first()
    
    if not coupon:
        flash('Invalid coupon code', 'danger')
        return redirect(url_for('cart'))
    
    is_valid, message = coupon.is_valid()
    if not is_valid:
        flash(message, 'danger')
        return redirect(url_for('cart'))
    
    # Store in session
    session['coupon_id'] = coupon.id
    session['discount_percent'] = coupon.discount_percent
    
    flash(f'Coupon applied! {coupon.discount_percent}% off', 'success')
    return redirect(url_for('cart'))
```

### Step 3: Update Cart Template

Add to `templates/cart.html`:

```html
<!-- Add before Place Order button -->
<div class="mb-3">
    <form method="POST" action="{{ url_for('apply_coupon') }}">
        <div class="input-group">
            <input type="text" name="coupon_code" class="form-control" 
                   placeholder="Enter coupon code">
            <button class="btn btn-outline-secondary" type="submit">Apply</button>
        </div>
    </form>
</div>

{% if session.discount_percent %}
<div class="alert alert-success">
    Coupon applied: {{ session.discount_percent }}% off
</div>
{% endif %}
```

### Step 4: Update Order Placement

Modify `place_order()` in `app.py`:

```python
@app.route('/place_order', methods=['POST'])
@login_required
def place_order():
    # ... existing code ...
    
    # Calculate total
    total = 0
    for food_id, quantity in session['cart'].items():
        food = FoodItem.query.get(int(food_id))
        if food:
            total += food.price * quantity
    
    # Apply coupon if exists
    if 'coupon_id' in session:
        coupon = Coupon.query.get(session['coupon_id'])
        discount = total * (coupon.discount_percent / 100)
        total -= discount
        
        # Increment usage
        coupon.used_count += 1
        
        # Clear coupon from session
        session.pop('coupon_id', None)
        session.pop('discount_percent', None)
    
    # ... rest of order creation ...
```

---

## 📍 Example 3: Add Delivery Address

### Step 1: Create Address Model

```python
class DeliveryAddress(db.Model):
    __tablename__ = 'delivery_addresses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    label = db.Column(db.String(50))  # Home, Work, etc.
    address_line1 = db.Column(db.String(200), nullable=False)
    address_line2 = db.Column(db.String(200))
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20))
    is_default = db.Column(db.Boolean, default=False)
    
    user = db.relationship('User', backref='addresses')
```

### Step 2: Add to Order Model

```python
class Order(db.Model):
    # ... existing fields ...
    delivery_address_id = db.Column(db.Integer, db.ForeignKey('delivery_addresses.id'))
    
    delivery_address = db.relationship('DeliveryAddress')
```

### Step 3: Create Address Management Routes

```python
@app.route('/addresses')
@login_required
def addresses():
    user_addresses = DeliveryAddress.query.filter_by(
        user_id=session['user_id']
    ).all()
    return render_template('addresses.html', addresses=user_addresses)

@app.route('/add_address', methods=['GET', 'POST'])
@login_required
def add_address():
    if request.method == 'POST':
        address = DeliveryAddress(
            user_id=session['user_id'],
            label=request.form.get('label'),
            address_line1=request.form.get('address_line1'),
            city=request.form.get('city'),
            state=request.form.get('state'),
            zip_code=request.form.get('zip_code'),
            phone=request.form.get('phone'),
            is_default=request.form.get('is_default') == 'on'
        )
        
        # If set as default, unset others
        if address.is_default:
            DeliveryAddress.query.filter_by(
                user_id=session['user_id'], 
                is_default=True
            ).update({'is_default': False})
        
        db.session.add(address)
        db.session.commit()
        
        flash('Address added successfully', 'success')
        return redirect(url_for('addresses'))
    
    return render_template('add_address.html')
```

---

## 💳 Example 4: Add Payment Methods

### Step 1: Create Payment Method Model

```python
class PaymentMethod(db.Model):
    __tablename__ = 'payment_methods'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    card_type = db.Column(db.String(20))  # Visa, Mastercard, etc.
    last_four = db.Column(db.String(4))  # Last 4 digits
    expiry_month = db.Column(db.Integer)
    expiry_year = db.Column(db.Integer)
    is_default = db.Column(db.Boolean, default=False)
    
    user = db.relationship('User', backref='payment_methods')
```

### Step 2: Update Order Model

```python
class Order(db.Model):
    # ... existing fields ...
    payment_method = db.Column(db.String(50))  # Cash, Card, UPI
    payment_status = db.Column(db.String(20), default='Pending')
```

---

## 📊 Example 5: Add Admin Analytics

### Step 1: Create Analytics Route

```python
@app.route('/admin/analytics')
@admin_required
def admin_analytics():
    # Total revenue
    total_revenue = db.session.query(
        db.func.sum(Order.total_amount)
    ).scalar() or 0
    
    # Revenue by category
    category_revenue = db.session.query(
        FoodItem.category,
        db.func.sum(OrderItem.price * OrderItem.quantity)
    ).join(OrderItem).group_by(FoodItem.category).all()
    
    # Top selling items
    top_items = db.session.query(
        FoodItem.name,
        db.func.sum(OrderItem.quantity).label('total_sold')
    ).join(OrderItem).group_by(FoodItem.id).order_by(
        db.desc('total_sold')
    ).limit(5).all()
    
    # Orders by status
    order_stats = db.session.query(
        Order.status,
        db.func.count(Order.id)
    ).group_by(Order.status).all()
    
    return render_template('admin_analytics.html',
                         total_revenue=total_revenue,
                         category_revenue=category_revenue,
                         top_items=top_items,
                         order_stats=order_stats)
```

### Step 2: Create Analytics Template

```html
{% extends "base.html" %}

{% block content %}
<div class="container my-5">
    <h2>Analytics Dashboard</h2>
    
    <!-- Revenue Card -->
    <div class="card mb-4">
        <div class="card-body">
            <h3>Total Revenue</h3>
            <h1 class="text-success">${{ "%.2f"|format(total_revenue) }}</h1>
        </div>
    </div>
    
    <!-- Top Selling Items -->
    <div class="card mb-4">
        <div class="card-header">
            <h5>Top Selling Items</h5>
        </div>
        <div class="card-body">
            <table class="table">
                <thead>
                    <tr>
                        <th>Item</th>
                        <th>Units Sold</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item, sold in top_items %}
                    <tr>
                        <td>{{ item }}</td>
                        <td>{{ sold }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}
```

---

## 🔔 Example 6: Add Email Notifications

### Step 1: Install Flask-Mail

Add to `requirements.txt`:
```
Flask-Mail==0.9.1
```

### Step 2: Configure Email

Add to `app.py`:

```python
from flask_mail import Mail, Message

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-password'

mail = Mail(app)
```

### Step 3: Send Order Confirmation Email

```python
def send_order_email(order):
    msg = Message(
        'Order Confirmation',
        sender='noreply@foodexpress.com',
        recipients=[order.user.email]
    )
    
    msg.body = f'''
    Hello {order.user.name},
    
    Your order #{order.id} has been placed successfully!
    
    Order Total: ${order.total_amount:.2f}
    Status: {order.status}
    
    Thank you for ordering from FoodExpress!
    '''
    
    mail.send(msg)

# Call in place_order()
@app.route('/place_order', methods=['POST'])
@login_required
def place_order():
    # ... existing code ...
    db.session.commit()
    
    # Send email
    send_order_email(order)
    
    # ... rest of code ...
```

---

## 🔍 Best Practices for Extensions

### 1. **Follow Existing Patterns**
- Use decorators for authentication
- Follow naming conventions
- Keep routes organized

### 2. **Database Migrations**
After adding models:
```python
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
```

### 3. **Error Handling**
```python
@app.route('/example')
def example():
    try:
        # Your code
        pass
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('index'))
```

### 4. **Testing New Features**
1. Test as regular user
2. Test as admin
3. Test edge cases (empty cart, invalid data)
4. Test error scenarios

### 5. **Code Organization**
For large features, consider splitting into modules:
```
food_delivery_app/
├── app.py
├── models.py
├── routes/
│   ├── auth.py
│   ├── cart.py
│   └── admin.py
```

---

## 📚 Additional Resources

- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [SQLAlchemy Relationships](https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html)
- [Bootstrap Components](https://getbootstrap.com/docs/5.3/components/)

---

Start with small extensions and gradually add more complex features!