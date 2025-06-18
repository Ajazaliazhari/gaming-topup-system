#Gaming Top-Up Management System

A Django-based backend system to manage and analyze gaming top-up transactions. This project includes models, API endpoints, admin functionality, and a staff-only analytics dashboard.

---

##Features

- Game and Top-Up Product Management via Django Admin
- REST API to perform Top-Up requests with validation
- Protected Dashboard with:
  - Top 5 Purchased Products
  - 7-Day Daily Revenue Summary
  - Current Month Failed Transaction Count

---

## Tech Stack

- Python 3.10+
- Django 5.x
- Django REST Framework
- Mysql 

---

##Project Structure

gaming_topup_project/
├── topup/
│   ├── models.py          # Game, TopUpProduct, TopUpOrder models
│   ├── views.py           # API and Dashboard views
│   ├── serializers.py     # API request validation
│   ├── urls.py            # App-specific routes
│   └── templates/
│       └── topup/
│           └── dashboard.html  # Staff-only analytics dashboard
├── gaming_topup_project/
│   └── urls.py            # Main project routes
├── manage.py
└── requirements.txt
---

##Setup Instructions


# 2. Create virtual environment & activate
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Run development server
python manage.py runserver


---

##Django Admin Access

- Visit: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)
- Login using your superuser credentials
- Manage:
  - Game (Add game name, game ID, active status)
  - TopUpProduct (Set price, name, in-game currency, and game association)

---

##API Usage – /api/topup/

### Endpoint
POST /api/topup/


### Headers

Content-Type: application/json

### Sample Request
Json Body
{
  "gamename": "PUBG Mobile",
  "game_id": "pubg123",
  "product_name": "UC Pack 500",
  "product_id": 4,
  "product_price": 399,
  "user_email": "player@example.com",
  "payment_status": "pending"
}


### Validation Logic:
- Game must exist and be active
- Product must belong to that game
- Valid email required

### Possible Statuses
- pending
- success
- failed

---

## Analytics Dashboard – /dashboard/

### URL

GET /dashboard/


### Access Control
- Only accessible to staff users (is_staff=True)
- Login required (/admin login works)

### Metrics Displayed

- **Top 5 Purchased Products** (most ordered)
- **Daily Revenue (last 7 days)** (only successful payments)
- **Failed Payments** (current month only)

---

##Flow Diagram (Simplified)

User ➜ POST /api/topup/ ➜ Validate Game & Product ➜ Save TopUpOrder ➜ View Stats on /dashboard/


---

##Demo Video (Add your link)

[Watch here](https://drive.google.com/your-demo-video-link)


## Author

Ajaz Ali  
Python | Django | APIs | MySQL  
email: test@gmail.com

---


