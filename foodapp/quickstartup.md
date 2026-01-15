# 🚀 Quick Start Guide

Get the Food Delivery App running in 5 minutes!

## ⚡ Super Quick Setup (Recommended)

### Windows
```bash
# 1. Run setup script
setup.bat

# 2. Activate environment
venv\Scripts\activate

# 3. Run the app
python app.py
```

### Mac/Linux
```bash
# 1. Make script executable
chmod +x setup.sh

# 2. Run setup script
./setup.sh

# 3. Activate environment
source venv/bin/activate

# 4. Run the app
python app.py
```

### Open Browser
```
http://localhost:5000
```

## 🔑 Login Credentials

**Admin Account** (Full Access)
- Email: `admin@food.com`
- Password: `admin123`

**Regular User**
- Click "Register" to create your account

## 🎯 What to Try First

### As a Customer:
1. Browse the food menu
2. Use search to find "Pizza"
3. Click "Add to Cart" on items
4. Go to Cart and adjust quantities
5. Click "Place Order"
6. View your order history

### As Admin:
1. Login with admin credentials
2. View dashboard statistics
3. Click "Add New Food Item"
4. Fill form and submit
5. Go to "Manage Orders" to see all orders
6. Update order status to "Processing" or "Delivered"

## 📁 File Structure Quick Reference

```
food_delivery_app/
├── app.py              ← Main application (start here)
├── models.py           ← Database models
├── requirements.txt    ← Dependencies
├── templates/          ← HTML files
│   ├── base.html       ← Navigation bar template
│   ├── index.html      ← Home page
│   ├── cart.html       ← Shopping cart
│   └── ...
└── static/
    └── images/         ← Put food images here
```

## 🖼️ Adding Food Images

Place images in `static/images/` folder:

**Required:**
- `default.jpg` - Fallback image

**Optional (for sample data):**
- `pizza.jpg`
- `burger.jpg`
- `salad.jpg`
- `pasta.jpg`
- `wings.jpg`
- `cake.jpg`

If images are missing, the app will use `default.jpg` automatically.

## 🐛 Common Issues & Fixes

### "Module not found"
```bash
pip install -r requirements.txt
```

### "Port 5000 in use"
Edit `app.py` line 211:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change to 5001
```

### Database locked
```bash
# Delete database and restart
rm food_delivery.db  # Mac/Linux
del food_delivery.db  # Windows
python app.py
```

## 🐳 Docker Quick Start

```bash
# Build and run
docker-compose up --build

# Access app
http://localhost:5000

# Stop app
docker-compose down
```

## 📚 Learning Path

1. **Start Simple**: Run the app and explore as a user
2. **Understand Routes**: Look at `@app.route` decorators in `app.py`
3. **Study Models**: Check `models.py` for database structure
4. **Explore Templates**: See how data flows from Python to HTML
5. **Customize**: Try changing colors, adding features

## 🎓 Key Concepts to Understand

### 1. Flask Routes
```python
@app.route('/cart')  # URL path
def cart():          # Function name
    return render_template('cart.html')  # Response
```

### 2. Sessions (Cart Storage)
```python
session['cart'] = {'1': 2, '3': 1}  # food_id: quantity
```

### 3. Database Queries
```python
FoodItem.query.all()           # Get all items
User.query.get(user_id)        # Get by ID
Order.query.filter_by(user_id=1).all()  # Filter
```

### 4. Templates (Jinja2)
```html
{% for food in food_items %}   <!-- Loop -->
    {{ food.name }}             <!-- Variable -->
{% endfor %}
```

## 💡 Next Steps

- Read full `README.md` for detailed documentation
- Explore `app.py` to understand all routes
- Try adding new features (see README for ideas)
- Customize the design in templates

## 🆘 Need Help?

- Check `README.md` for detailed explanations
- Review code comments in `app.py` and `models.py`
- Troubleshooting section in `README.md`

---

**Happy Coding! 🚀**