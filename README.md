Gaming Top-Up Management System - Django Backend
This project is a Django-based backend system simulating a Gaming Top-Up Management System. It covers model design, REST API implementation, validation logic, and basic analytics, demonstrating understanding of Django architecture, RESTful API development, and ORM query optimization.

Table of Contents
Setup Instructions

API Usage (/api/topup/)

Dashboard Access Info (/dashboard/)

Sample curl/Postman Request

Project Structure

Setup Instructions
Follow these steps to get the project up and running:

Clone the repository (or create the files as provided):
First, ensure you have Python and pip installed.

Navigate to the project root:

cd gaming_topup_project

Create a virtual environment (recommended):

python -m venv venv

Activate the virtual environment:

On Windows:

.\venv\Scripts\activate

On macOS/Linux:

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Apply database migrations:

python manage.py makemigrations topup
python manage.py migrate

Create a superuser (for Django Admin and Dashboard access):

python manage.py createsuperuser

Follow the prompts to create a username and password.

Run the development server:

python manage.py runserver

The server will typically run on http://127.0.0.1:8000/.

API Usage (/api/topup/)
This endpoint allows you to simulate a top-up transaction.

URL: POST http://127.0.0.1:8000/api/topup/

Method: POST

Content-Type: application/json

Request Body Example:
{
    "gamename": "PUBG Mobile",
    "game_id": "pubg123",
    "product_name": "UC Pack 500",
    "product_id": 1,
    "product_price": 399.00,
    "user_email": "player@example.com",
    "payment_status": "pending"
}

Before making requests:
Ensure you have created a Game and TopUpProduct in the Django Admin that matches the gamename, game_id, product_name, and product_id in your request. For example:

Go to http://127.00.1:8000/admin/.

Log in with your superuser credentials.

Add a Game:

Name: PUBG Mobile

Game ID: pubg123

Is Active: True

Add a TopUpProduct:

Game: (Select PUBG Mobile)

Name: UC Pack 500

Price: 399.00

In-game Currency: 500 UC

Note down the product_id (it's the ID assigned by Django, usually 1 for the first product).

Expected Responses:
Success (HTTP 201 Created):

{
    "id": 1,
    "user_email": "player@example.com",
    "product": 1,
    "status": "pending",
    "created_at": "2023-10-27T10:00:00.123456Z"
}

Validation Error (HTTP 400 Bad Request):

{
    "game_id": [
        "Game with provided name and ID does not exist."
    ]
}

or

{
    "non_field_errors": [
        "The specified game is currently inactive."
    ]
}

or

{
    "non_field_errors": [
        "Product with provided name and ID is not found or not associated with the specified game."
    ]
}

Dashboard Access Info (/dashboard/)
The analytics dashboard provides insights into top-up activities.

URL: http://127.0.0.1:8000/dashboard/

Access: This view is protected and requires a logged-in staff user.

Ensure you have created a superuser (python manage.py createsuperuser).

Access the Django Admin: http://127.0.0.1:8000/admin/ and log in.

Once logged in, navigate to http://127.0.0.1:8000/dashboard/.

The dashboard displays:

Top 5 Most Purchased Top-Up Products (from successful orders).

Daily Revenue (last 7 days) from successful orders.

Failed Payment Count (current month).

Sample curl/Postman Request
curl example:
curl -X POST \
  http://127.0.0.1:8000/api/topup/ \
  -H 'Content-Type: application/json' \
  -d '{
    "gamename": "PUBG Mobile",
    "game_id": "pubg123",
    "product_name": "UC Pack 500",
    "product_id": 1,
    "product_price": 399.00,
    "user_email": "player@example.com",
    "payment_status": "pending"
  }'

(Remember to replace product_id with the actual ID from your Django Admin setup.)

Postman/Insomnia:
Set the request type to POST, enter the URL, and in the "Body" tab, select "raw" and "JSON", then paste the JSON request body example.

Project Structure
gaming_topup_project/
├── manage.py
├── gaming_topup_project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py           # Main project settings (updated for DRF, app, templates)
│   ├── urls.py               # Main project URL configurations (includes app urls)
│   └── wsgi.py
├── topup/
│   ├── __init__.py
│   ├── admin.py              # Model registration for Django Admin
│   ├── apps.py
│   ├── migrations/
│   │   └── __init__.py
│   ├── models.py             # Defines Game, TopUpProduct, TopUpOrder models
│   ├── serializers.py        # DRF Serializers for API request/response
│   ├── urls.py               # App-specific URL configurations for API and dashboard
│   ├── views.py              # DRF APIView for top-up endpoint, Django view for dashboard
│   └── tests.py
├── templates/
│   └── dashboard.html        # HTML template for the analytics dashboard
└── requirements.txt          # Lists Python dependencies (Django, djangorestframework)

