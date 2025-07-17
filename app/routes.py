from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import Book, Member, Transaction
from .forms import BookForm, ImportForm, MemberForm, IssueForm, ReturnForm
from . import db
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return redirect(url_for('main.books'))

# ====================
# BOOK ROUTES
# ====================
@main_bp.route('/books')
def books():
    all_books = Book.query.all()
    return render_template('books.html', books=all_books)

@main_bp.route('/books/add', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            authors=form.authors.data,
            isbn=form.isbn.data,
            publisher=form.publisher.data,
            pages=form.pages.data,
            stock=form.stock.data
        )
        db.session.add(book)
        db.session.commit()
        flash('Book added!')
        return redirect(url_for('main.books'))
    return render_template('book_form.html', form=form, action="Add")

@main_bp.route('/books/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    book = Book.query.get_or_404(id)
    form = BookForm(obj=book)
    if form.validate_on_submit():
        form.populate_obj(book)
        db.session.commit()
        flash('Book updated!')
        return redirect(url_for('main.books'))
    return render_template('book_form.html', form=form, action="Edit")

@main_bp.route('/books/delete/<int:id>')
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted!')
    return redirect(url_for('main.books'))

# ====================
# MEMBER ROUTES
# ====================
@main_bp.route('/members')
def members():
    all_members = Member.query.all()
    return render_template('members.html', members=all_members)

@main_bp.route('/members/add', methods=['GET', 'POST'])
def add_member():
    form = MemberForm()
    if form.validate_on_submit():
        member = Member(name=form.name.data, email=form.email.data)
        db.session.add(member)
        db.session.commit()
        flash('Member added!')
        return redirect(url_for('main.members'))
    return render_template('member_form.html', form=form, action="Add")

@main_bp.route('/members/edit/<int:id>', methods=['GET', 'POST'])
def edit_member(id):
    member = Member.query.get_or_404(id)
    form = MemberForm(obj=member)
    if form.validate_on_submit():
        form.populate_obj(member)
        db.session.commit()
        flash('Member updated!')
        return redirect(url_for('main.members'))
    return render_template('member_form.html', form=form, action="Edit")

@main_bp.route('/members/delete/<int:id>')
def delete_member(id):
    member = Member.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    flash('Member deleted!')
    return redirect(url_for('main.members'))

# ====================
# TRANSACTION ROUTES
# ====================
@main_bp.route('/transactions/issue', methods=['GET', 'POST'])
def issue_book():
    form = IssueForm()
    form.member_id.choices = [(m.id, m.name) for m in Member.query.all()]
    form.book_id.choices = [(b.id, b.title) for b in Book.query.filter(Book.stock > 0).all()]

    if form.validate_on_submit():
        member = Member.query.get(form.member_id.data)
        if member.debt > 500:
            flash("Member has outstanding debt over ₹500.")
            return redirect(url_for('main.issue_book'))

        book = Book.query.get(form.book_id.data)
        book.stock -= 1
        transaction = Transaction(book_id=book.id, member_id=member.id)
        db.session.add(transaction)
        db.session.commit()
        flash('Book issued!')
        return redirect(url_for('main.books'))

    return render_template('issue_book.html', form=form)

@main_bp.route('/transactions/return', methods=['GET', 'POST'])
def return_book():
    form = ReturnForm()
    open_transactions = Transaction.query.filter(Transaction.return_date == None).all()
    form.transaction_id.choices = [(t.id, f"{t.book.title} to {t.member.name}") for t in open_transactions]

    if form.validate_on_submit():
        txn = Transaction.query.get(form.transaction_id.data)
        txn.return_date = datetime.utcnow()
        txn.fee = 50
        txn.member.debt += txn.fee
        txn.book.stock += 1
        db.session.commit()
        flash('Book returned!')
        return redirect(url_for('main.books'))

    return render_template('return_book.html', form=form)

import requests

@main_bp.route('/import-books', methods=['GET', 'POST'])
def import_books():
    form = ImportForm()
    if form.validate_on_submit():
        count = 0
        page = 1
        total_needed = form.num_books.data
        search_title = form.title.data or ''

        while count < total_needed:
            response = requests.get(
                'https://frappe.io/api/method/frappe-library',
                params={'page': page, 'title': search_title}
            )
            data = response.json().get('message', [])
            if not data:
                break

            for item in data:
                if count >= total_needed:
                    break
                if Book.query.filter_by(isbn=item.get('isbn')).first():
                    continue  # Skip if already exists

                book = Book(
                    title=item.get('title'),
                    authors=item.get('authors'),
                    isbn=item.get('isbn'),
                    publisher=item.get('publisher'),
                    pages=int(item.get('num_pages') or 0),
                    stock=1
                )
                db.session.add(book)
                count += 1
            db.session.commit()
            page += 1

        flash(f'{count} books imported successfully!')
        return redirect(url_for('main.books'))

    return render_template('import_books.html', form=form)

