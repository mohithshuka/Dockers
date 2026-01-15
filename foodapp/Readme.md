# 🍔 Food Delivery Web Application

A complete full-stack food delivery web application built with Flask, SQLAlchemy, and Bootstrap.

## 📋 Features

### User Features
- ✅ User Registration & Authentication
- ✅ Browse Food Menu with Search & Filter
- ✅ Add Items to Cart
- ✅ Manage Cart (Increase/Decrease Quantity)
- ✅ Place Orders
- ✅ View Order History
- ✅ Order Confirmation Page

### Admin Features
- ✅ Admin Dashboard with Statistics
- ✅ Add/Edit/Delete Food Items
- ✅ View All Orders
- ✅ Update Order Status (Pending → Processing → Delivered)

### Technical Features
- ✅ Clean MVC Architecture
- ✅ SQLite Database with SQLAlchemy ORM
- ✅ Session-based Authentication
- ✅ Responsive Bootstrap UI
- ✅ Form Validation
- ✅ Flash Messages
- ✅ Docker Ready

## 🗂️ Project Structure

```
food_delivery_app/
├── app.py                      # Main Flask application
├── models.py                   # Database models
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose config
├── README.md                   # This file
├── templates/                  # HTML templates
│   ├── base.html              # Base template with navbar
│   ├── index.html             # Home page (food menu)
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── cart.html              # Shopping cart
│   ├── orders.html            # Order history
│   ├── order_confirmation.html # Order success page
│   ├── admin_dashboard.html   # Admin dashboard
│   ├── add_food.html          # Add food item
│   ├── edit_food.html         # Edit food item
│   └── admin_orders.html      # Manage orders
└── static/                     # Static files
    └── images/                # Food images
        ├── default.jpg
        ├── pizza.jpg
        ├── burger.jpg
        ├── salad.jpg
        ├── pasta.jpg
        ├── wings.jpg
        └── cake.jpg
```

## 🚀 Installation & Setup

### Method 1: Local Installation

#### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

#### Steps

1. **Clone or Download the Project**
   ```bash
   cd food_delivery_app
   ```

2. **Create Virtual Environment (Recommended)**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create Required Directories**
   ```bash
   mkdir -p static/images
   ```

5. **Add Food Images** (Optional)
   Place food images in `static/images/` folder:
   - default.jpg (fallback image)
   - pizza.jpg, burger.jpg, salad.jpg, etc.

6. **Run the Application**
   ```bash
   python app.py
   ```

7. **Access the Application**
   Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

### Method 2: Docker Deployment

#### Prerequisites
- Docker
- Docker Compose

#### Steps

1. **Build and Run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the Application**
   ```
   http://localhost:5000
   ```

3. **Stop the Application**
   ```bash
   docker-compose down
   ```

## 👤 Default Credentials

### Admin Account
- **Email:** admin@food.com
- **Password:** admin123

### Create User Account
Register a new account through the registration page.

## 📊 Database Schema

### Users Table
- `id` - Primary Key
- `name` - User's full name
- `email` - Unique email address
- `password` - Hashed password
- `is_admin` - Admin flag (Boolean)
- `created_at` - Registration timestamp

### Food Items Table
- `id` - Primary Key
- `name` - Food item name
- `description` - Item description
- `price` - Price (Float)
- `category` - Category (Pizza, Burger, etc.)
- `image` - Image filename
- `created_at` - Creation timestamp

### Orders Table
- `id` - Primary Key
- `user_id` - Foreign Key to Users
- `total_amount` - Order total (Float)
- `status` - Order status (Pending, Processing, Delivered, Cancelled)
- `created_at` - Order timestamp

### Order Items Table
- `id` - Primary Key
- `order_id` - Foreign Key to Orders
- `food_id` - Foreign Key to Food Items
- `quantity` - Item quantity
- `price` - Price at time of order

## 🔧 Key Code Explanations

### 1. User Authentication (`app.py`)

```python
@login_required  # Decorator ensures user must be logged in
def cart():
    # Access user info from session
    user_id = session['user_id']
```

**How it works:**
- Password hashing with `werkzeug.security`
- Session-based authentication
- Custom decorators `@login_required` and `@admin_required`

### 2. Shopping Cart System

The cart is stored in Flask sessions as a dictionary:

```python
session['cart'] = {
    '1': 2,  # food_id: quantity
    '3': 1
}
```

**Cart Operations:**
- Add item: Creates or increments quantity
- Update: Increase/decrease quantity
- Remove: Deletes item from cart
- Clear: Empties cart after order

### 3. Database Relationships (`models.py`)

```python
class Order(db.Model):
    # One user has many orders
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # One order has many order items
    order_items = db.relationship('OrderItem', backref='order')
```

**Relationships:**
- User → Orders (One-to-Many)
- Order → OrderItems (One-to-Many)
- FoodItem → OrderItems (One-to-Many)

### 4. Order Processing

When user places order:
1. Calculate total from cart
2. Create Order record
3. Create OrderItem records for each cart item
4. Clear cart
5. Redirect to confirmation page

### 5. Admin Features

Admin can:
- View statistics (total items, orders, revenue)
- Add new food items with form validation
- Edit existing items
- Delete items (with confirmation)
- Manage order status

## 🎨 Frontend Components

### Bootstrap Classes Used
- **Cards:** `.card`, `.card-body` for content containers
- **Grid:** `.row`, `.col-md-*` for responsive layout
- **Forms:** `.form-control`, `.form-select` for inputs
- **Buttons:** `.btn`, `.btn-primary`, `.btn-success`
- **Badges:** `.badge` for categories and status
- **Navbar:** `.navbar`, `.navbar-nav` for navigation

### Custom CSS
- Hover effects on food cards
- Smooth transitions
- Custom color scheme
- Responsive design adjustments

## 🔍 Search & Filter Functionality

Users can:
- **Search by name:** Enter keywords in search box
- **Filter by category:** Select category from dropdown
- **Combine filters:** Search + category filter work together

```python
# In app.py
query = FoodItem.query
if search_query:
    query = query.filter(FoodItem.name.contains(search_query))
if category:
    query = query.filter_by(category=category)
```

## 📱 Responsive Design

The application is fully responsive and works on:
- 💻 Desktop (1200px+)
- 📱 Tablet (768px - 1199px)
- 📱 Mobile (< 768px)

Bootstrap's grid system automatically adjusts:
```html
<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3">
  <!-- 1 column on mobile, 2 on tablet, 3 on desktop -->
</div>
```

## 🛡️ Security Features

- ✅ Password hashing with Werkzeug
- ✅ CSRF protection with secret key
- ✅ SQL injection prevention (SQLAlchemy)
- ✅ Session-based authentication
- ✅ Admin route protection
- ✅ Input validation

## 🧪 Testing the Application

### Test User Flow
1. Register a new account
2. Browse food menu
3. Search and filter items
4. Add items to cart
5. Update quantities
6. Place order
7. View order history

### Test Admin Flow
1. Login as admin (admin@food.com / admin123)
2. Access admin dashboard
3. Add new food item
4. Edit existing item
5. View all orders
6. Update order status

## 🚨 Troubleshooting

### Common Issues

**1. "Module not found" Error**
```bash
pip install -r requirements.txt
```

**2. "Database locked" Error**
- Close all connections to database
- Delete `food_delivery.db` and restart

**3. Images Not Loading**
- Check `static/images/` folder exists
- Verify image filenames match database entries
- Default to `default.jpg` if image missing

**4. Port 5000 Already in Use**
Change port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## 📈 Future Enhancements

Potential features to add:
- [ ] Payment gateway integration
- [ ] Email notifications
- [ ] Real-time order tracking
- [ ] User profile management
- [ ] Restaurant ratings and reviews
- [ ] Coupon/discount system
- [ ] Multiple delivery addresses
- [ ] Order history export (PDF)
- [ ] Image upload for food items
- [ ] Advanced analytics dashboard

## 🤝 Contributing

Feel free to fork this project and submit pull requests for improvements!

## 📄 License

This project is open source and available for educational purposes.

## 📧 Support

For questions or issues:
- Create an issue in the repository
- Email: support@foodexpress.com

---

**Built with ❤️ using Flask, SQLAlchemy, and Bootstrap**
<!-- python -u "d:\Dockers\Flaskapp\app.py" -->