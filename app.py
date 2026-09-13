from flask import Flask, request
from models import db
import services

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'

db.init_app(app)


@app.route('/')
def home():
    return "Library API is running!"


@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    result, status = services.create_book(data)
    return result, status


@app.route('/books', methods=['GET'])
def get_books():
    result, status = services.get_all_books()
    return result, status


@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    result, status = services.get_book_by_id(book_id)
    return result, status


@app.route('/members', methods=['POST'])
def add_member():
    data = request.get_json()
    result, status = services.create_member(data)
    return result, status


@app.route('/loans', methods=['POST'])
def create_loan():
    data = request.get_json()
    result, status = services.borrow_book(data)
    return result, status


@app.route('/loans/<int:loan_id>/return', methods=['POST'])
def return_book(loan_id):
    result, status = services.return_loan(loan_id)
    return result, status


@app.route('/members/<int:member_id>/loans', methods=['GET'])
def get_member_loans(member_id):
    result, status = services.get_member_current_loans(member_id)
    return result, status


@app.route('/reports/overdue', methods=['GET'])
def get_overdue_loans():
    result, status = services.get_overdue_loans()
    return result, status


@app.route('/reports/stats', methods=['GET'])
def get_stats():
    result, status = services.get_stats()
    return result, status


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)