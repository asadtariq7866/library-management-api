# Library Management API

A simple Library Management System built with Flask, SQLite, and Flask-SQLAlchemy. Manages Books, Members, and Loans with real relational data modeling.

## Tech Stack
- Python / Flask
- Flask-SQLAlchemy (SQLite database)

## Project Structure

library-api/
├── app.py          # Flask app + routes
├── models.py       # SQLAlchemy models (Book, Member, Loan)
├── services.py     # Business logic (borrow/return, reports, validation)
├── requirements.txt
└── .gitignore

## How to Run
`
1. Clone the repository:

git clone https://github.com/asadtariq7866/library-management-api.git
cd library-management-api

2. Install dependencies:

pip install -r requirements.txt

3. Run the app:

python app.py

The API will be available at http://127.0.0.1:5000

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /books | Add a new book |
| GET | /books | List all books |
| GET | /books/<id> | Get a specific book |
| POST | /members | Register a new member |
| POST | /loans | Borrow a book |
| POST | /loans/<id>/return | Return a borrowed book |
| GET | /members/<id>/loans | Get a member's current loans |
| GET | /reports/overdue | List overdue loans |
| GET | /reports/stats | Library statistics |

## Business Rules
- A book cannot be borrowed if no copies are available (400 error)
- A loan cannot be returned twice (400 error)
- Member emails must be unique (400 error)
- Missing required fields return a clear 400 error instead of crashing

## What I Found Challenging

SQLAlchemy relationships (db.relationship and backref) were new to me — understanding how it automatically pulls Book and Member data through a Loan without writing manual queries took some practice. Separating business logic from routes into services.py was also a new pattern for me, but it made the code much cleaner once I understood the reasoning behind it.