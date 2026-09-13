from datetime import date, timedelta
from models import db, Book, Member, Loan


def validate_fields(data, required_fields):
    """Check ke saare required fields maujood hain. Missing fields ka error message deta hai, warna None."""
    missing = []
    for field in required_fields:
        if data.get(field) is None:
            missing.append(field)
    
    if missing:
        return f"Missing required field(s): {', '.join(missing)}"
    
    return None


def create_book(data):
    """Nayi book banata hai. Returns (result_dict, status_code)."""
    error = validate_fields(data, ['title', 'author', 'isbn', 'copies_total'])
    if error:
        return {"error": error}, 400
    
    new_book = Book(
        title=data.get('title'),
        author=data.get('author'),
        isbn=data.get('isbn'),
        copies_total=data.get('copies_total'),
        copies_available=data.get('copies_total')
    )
    
    db.session.add(new_book)
    db.session.commit()
    
    return {
        "id": new_book.id,
        "title": new_book.title,
        "author": new_book.author,
        "isbn": new_book.isbn,
        "copies_total": new_book.copies_total,
        "copies_available": new_book.copies_available
    }, 201


def get_all_books():
    """Sari books ki list deta hai."""
    all_books = Book.query.all()
    result = []
    for book in all_books:
        result.append({
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "isbn": book.isbn,
            "copies_total": book.copies_total,
            "copies_available": book.copies_available
        })
    return {"books": result}, 200


def get_book_by_id(book_id):
    """Ek specific book ki detail deta hai."""
    book = Book.query.get(book_id)
    if book is None:
        return {"error": "Book not found"}, 404
    
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "isbn": book.isbn,
        "copies_total": book.copies_total,
        "copies_available": book.copies_available
    }, 200


def create_member(data):
    """Naya member register karta hai."""
    error = validate_fields(data, ['name', 'email'])
    if error:
        return {"error": error}, 400
    
    email = data.get('email')
    existing_member = Member.query.filter_by(email=email).first()
    if existing_member is not None:
        return {"error": "A member with this email already exists"}, 400
    
    new_member = Member(name=data.get('name'), email=email)
    db.session.add(new_member)
    db.session.commit()
    
    return {
        "id": new_member.id,
        "name": new_member.name,
        "email": new_member.email,
        "joined_date": str(new_member.joined_date)
    }, 201


def borrow_book(data):
    """Book borrow karta hai — Loan banata hai aur copies_available kam karta hai."""
    error = validate_fields(data, ['book_id', 'member_id'])
    if error:
        return {"error": error}, 400
    
    book_id = data.get('book_id')
    member_id = data.get('member_id')
    
    book = Book.query.get(book_id)
    if book is None:
        return {"error": "Book not found"}, 404
    
    member = Member.query.get(member_id)
    if member is None:
        return {"error": "Member not found"}, 404
    
    if book.copies_available <= 0:
        return {"error": "No copies available for this book"}, 400
    
    new_loan = Loan(
        book_id=book_id,
        member_id=member_id,
        borrowed_date=date.today(),
        due_date=date.today() + timedelta(days=14)
    )
    book.copies_available -= 1
    
    db.session.add(new_loan)
    db.session.commit()
    
    return {
        "id": new_loan.id,
        "book_id": new_loan.book_id,
        "member_id": new_loan.member_id,
        "borrowed_date": str(new_loan.borrowed_date),
        "due_date": str(new_loan.due_date),
        "returned_date": new_loan.returned_date
    }, 201


def return_loan(loan_id):
    """Book return karta hai — copies_available badhata hai."""
    loan = Loan.query.get(loan_id)
    if loan is None:
        return {"error": "Loan not found"}, 404
    
    if loan.returned_date is not None:
        return {"error": "This loan has already been returned"}, 400
    
    loan.returned_date = date.today()
    
    book = Book.query.get(loan.book_id)
    book.copies_available += 1
    
    db.session.commit()
    
    return {
        "id": loan.id,
        "book_id": loan.book_id,
        "member_id": loan.member_id,
        "borrowed_date": str(loan.borrowed_date),
        "due_date": str(loan.due_date),
        "returned_date": str(loan.returned_date)
    }, 200


def get_member_current_loans(member_id):
    """Member ki current (return na hui) loans deta hai."""
    member = Member.query.get(member_id)
    if member is None:
        return {"error": "Member not found"}, 404
    
    current_loans = Loan.query.filter_by(member_id=member_id, returned_date=None).all()
    
    result = []
    for loan in current_loans:
        result.append({
            "loan_id": loan.id,
            "book_title": loan.book.title,
            "borrowed_date": str(loan.borrowed_date),
            "due_date": str(loan.due_date)
        })
    
    return {"member": member.name, "current_loans": result}, 200


def get_overdue_loans():
    """Saari overdue loans deta hai (due_date guzar chuki, returned nahi)."""
    today = date.today()
    overdue_loans = Loan.query.filter(
        Loan.due_date < today,
        Loan.returned_date.is_(None)
    ).all()
    
    result = []
    for loan in overdue_loans:
        result.append({
            "loan_id": loan.id,
            "member_name": loan.member.name,
            "book_title": loan.book.title,
            "due_date": str(loan.due_date)
        })
    
    return {"overdue_loans": result}, 200


def get_stats():
    """Library ke overall stats deta hai."""
    total_books = Book.query.count()
    total_members = Member.query.count()
    active_loans = Loan.query.filter_by(returned_date=None).count()
    
    top_member = None
    top_count = 0
    all_members = Member.query.all()
    for member in all_members:
        loan_count = len(member.loans)
        if loan_count > top_count:
            top_count = loan_count
            top_member = member.name
    
    return {
        "total_books": total_books,
        "total_members": total_members,
        "active_loans": active_loans,
        "top_borrower": top_member
    }, 200