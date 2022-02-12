from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=True, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'




db.create_all()
# title = Book(title='Haroy Potter', author='J. K. Gowling', rating=9.3)
# db.session.add(title)
# db.session.commit()
# db = sqlite3.connect("books-collection.db")
# cursor = db.cursor()
# cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")
all_books = []
# cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', '9.3')")
# db.commit()

@app.route('/')
def home():
    global all_books
    all_books = db.session.query(Book).all()
    # print(Book.query.filter_by(title='Harry Potter').first())
    if len(all_books) > 0:
        flag = True
    else:
        flag = False
    return render_template("index.html", books=all_books, flag=flag)


@app.route("/add", methods=['GET', 'POST'])
def add():
    global all_books
    if request.method == 'POST':
        book_to_add = Book(title=request.form['book_name'],
                       author=request.form['book_autor'],
                       rating=request.form['book_rating'])
        db.session.add(book_to_add)
        db.session.commit()
        return home()
        # return all_books
    return render_template("add.html")

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    if request.method == 'GET':
        to_edit = Book.query.filter_by(id=id).first()
    # book_name =
    elif request.method == 'POST':
        edition = Book.query.get(id)
        edition.rating = request.form["new_rating"]
        db.session.commit()
        return home()
    return render_template("edit.html", book=to_edit, id=id)


@app.route("/delete/<int:id>")
def delete(id):
    # id = request.args.get('id')
    to_delete = Book.query.get(id)
    db.session.delete(to_delete)
    db.session.commit()
    return home()



if __name__ == "__main__":
    app.run(debug=True)

