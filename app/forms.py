from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email

class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    authors = StringField('Authors')
    isbn = StringField('ISBN')
    publisher = StringField('Publisher')
    pages = IntegerField('Pages')
    stock = IntegerField('Stock')
    submit = SubmitField('Save')

class MemberForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    submit = SubmitField('Save')

class IssueForm(FlaskForm):
    member_id = SelectField('Member', coerce=int, validators=[DataRequired()])
    book_id = SelectField('Book', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Issue Book')

class ReturnForm(FlaskForm):
    transaction_id = SelectField('Transaction', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Return Book')

class ImportForm(FlaskForm):
    title = StringField('Title Contains')
    num_books = IntegerField('Number of Books', default=20, validators=[DataRequired()])
    submit = SubmitField('Import Books')
