# Food Express — Full Stack Food Delivery App

> A complete food delivery web application with user ordering, admin dashboard, cart management and Docker deployment — built with Flask, SQLAlchemy and Bootstrap.

[![Live Demo](https://img.shields.io/badge/Live_Demo-Visit_App-22C55E?logo=vercel&logoColor=white)](https://dockers-theta.vercel.app)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Backend-000000?logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?logo=python&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-UI-7952B3?logo=bootstrap&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white)

---

## Live Demo

**[dockers-theta.vercel.app](https://dockers-theta.vercel.app)**

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@food.com | admin123 |
| User | Register new account | — |

---

## Features

### User Features
- User registration and login with hashed passwords
- Browse full food menu with search and category filter
- Add items to cart, adjust quantities, remove items
- Place orders and view full order history
- Order confirmation page after checkout

### Admin Features
- Admin dashboard with live statistics (items, orders, revenue)
- Add, edit and delete food items with image support
- View all customer orders across the platform
- Update order status — Pending → Processing → Delivered

### Technical Features
- MVC architecture with clean separation of concerns
- SQLite database with SQLAlchemy ORM and relationships
- Session-based authentication with custom decorators
- Fully responsive Bootstrap UI (mobile, tablet, desktop)
- Docker and Docker Compose ready for one-command deployment.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Browser (User/Admin)                │
└─────────────────────────────────────────────────────┘
                          │
                    HTTP requests
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│              Flask Application (app.py)              │
│                                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │    Routes   │  │  Templates  │  │   Session   │ │
│  │  /home      │  │  Jinja2     │  │   Auth      │ │
│  │  /cart      │  │  Bootstrap  │  │   Cart      │ │
│  │  /orders    │  │  HTML       │  │   State     │ │
│  │  /admin     │  └─────────────┘  └─────────────┘ │
│  └─────────────┘                                     │
└─────────────────────────────────────────────────────┘
                          │
                    SQLAlchemy ORM
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│                  SQLite Database                      │
│                                                      │
│   Users ──── Orders ──── OrderItems ──── FoodItems  │
└─────────────────────────────────────────────────────┘
```

---

## Database Schema

```
Users                    FoodItems
─────────────────        ─────────────────
id (PK)                  id (PK)
name                     name
email (unique)           description
password (hashed)        price
is_admin                 category
created_at               image
                         created_at
      │
      │ 1:N
      ▼
Orders                   OrderItems
─────────────────        ─────────────────
id (PK)                  id (PK)
user_id (FK)             order_id (FK)
total_amount             food_id (FK)
status                   quantity
created_at               price
```

---

## Project Structure

```
Dockers/
├── foodapp/
│   ├── app.py                    # Flask routes and logic
│   ├── models.py                 # SQLAlchemy database models
│   ├── requirements.txt          # Python dependencies
│   ├── Dockerfile                # Container configuration
│   ├── docker-compose.yml        # Multi-container setup
│   ├── templates/
│   │   ├── base.html             # Base layout with navbar
│   │   ├── index.html            # Food menu homepage
│   │   ├── login.html            # Login page
│   │   ├── register.html         # Registration page
│   │   ├── cart.html             # Shopping cart
│   │   ├── orders.html           # Order history
│   │   ├── order_confirmation.html
│   │   ├── admin_dashboard.html  # Admin stats
│   │   ├── add_food.html         # Add food item
│   │   ├── edit_food.html        # Edit food item
│   │   └── admin_orders.html     # Manage all orders
│   └── static/
│       └── images/               # Food item images
├── instance/                     # SQLite database instance
├── .gitignore
└── README.md
```

---

## Getting Started

### Option 1 — Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/mohithshuka/Dockers.git
cd Dockers/foodapp

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Open: `http://localhost:5000`

### Option 2 — Run with Docker

```bash
cd Dockers/foodapp

# Build and start
docker-compose up --build

# Stop
docker-compose down
```

Open: `http://localhost:5000`

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Backend | Python + Flask | Routes, logic, session auth |
| ORM | SQLAlchemy | Database models and queries |
| Database | SQLite | Lightweight persistent storage |
| Frontend | HTML + Jinja2 | Server-side rendered templates |
| UI Framework | Bootstrap 5 | Responsive layout and components |
| Containerization | Docker + Compose | Portable one-command deployment |
| Deployment | Vercel | Live production hosting |

---

## Key Implementation Details

### Session-based Cart
```python
# Cart stored in Flask session as {food_id: quantity}
session['cart'] = {'1': 2, '3': 1}
```

### Custom Auth Decorators
```python
@login_required    # blocks unauthenticated users
@admin_required    # blocks non-admin users
```

### Search + Filter
```python
query = FoodItem.query
if search:    query = query.filter(FoodItem.name.contains(search))
if category:  query = query.filter_by(category=category)
```

### Password Security
```python
# Stored as hash, never plain text
generate_password_hash(password)
check_password_hash(stored_hash, input_password)
```

---

## Security Features

- Passwords hashed with Werkzeug — never stored plain text
- SQL injection prevention via SQLAlchemy parameterized queries
- Session secret key for CSRF protection
- Admin routes protected with `@admin_required` decorator
- Input validation on all forms

---

## Responsive Design

Works across all screen sizes:

| Device | Columns |
|--------|---------|
| Mobile (< 768px) | 1 column |
| Tablet (768–1199px) | 2 columns |
| Desktop (1200px+) | 3 columns |

---

## Roadmap

- [ ] Payment gateway integration (Stripe / Razorpay)
- [ ] Email notifications on order status change
- [ ] Real-time order tracking with WebSockets
- [ ] Image upload for food items (Cloudinary)
- [ ] Coupon and discount code system
- [ ] Push Docker image to Docker Hub via GitHub Actions
- [ ] Kubernetes deployment with auto-scaling

---

## Author

**Mohith Shuka**
GitHub: [@mohithshuka](https://github.com/mohithshuka)

---

## License

MIT

---

> If you found this project useful, consider giving it a star!
