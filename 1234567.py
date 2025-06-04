from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"

# MySQL Configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_mysql_password",
    database="library_db"
)
cursor = db.cursor()

# Home / Student Verification
@app.route('/')
def student_verification():
    return render_template("index.html")

# Book Request Form
@app.route('/request_book', methods=['GET', 'POST'])
def request_book():
    if request.method == 'POST':
        reg_no = request.form['reg_no']
        department = request.form['department']
        year = request.form['year']
        name = request.form['name']
        email = request.form['email']
        book_title = request.form['bookTitle']
        author = request.form['author']
        description = request.form['description']
        request_on = datetime.now().strftime('%Y-%m-%d')
        status = "Pending"

        insert_query = """
            INSERT INTO book_requests 
            (reg_no, department, year, name, email, book_title, author, description, request_on, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (reg_no, department, year, name, email, book_title, author, description, request_on, status)
        cursor.execute(insert_query, values)
        db.commit()

        return redirect(url_for('confirmation'))
    
    # If GET
    reg_no = request.args.get('reg_no')
    department = request.args.get('department')
    year = request.args.get('year')
    return render_template("request_book.html", reg_no=reg_no, department=department, year=year)

# Confirmation Page
@app.route('/confirmation')
def confirmation():
    return render_template("confirmation.html")

# Admin Panel
@app.route('/admin')
def admin_panel():
    cursor.execute("SELECT * FROM book_requests")
    requests = cursor.fetchall()
    return render_template("admin_requests.html", requests=requests)

# Admin Actions
@app.route('/update_status/<int:id>/<string:new_status>')
def update_status(id, new_status):
    cursor.execute("UPDATE book_requests SET status=%s WHERE id=%s", (new_status, id))
    db.commit()
    flash(f"Request {id} marked as {new_status}.")
    return redirect(url_for('admin_panel'))

# Delete Request
@app.route('/delete/<int:id>')
def delete_request(id):
    cursor.execute("DELETE FROM book_requests WHERE id=%s", (id,))
    db.commit()
    flash(f"Request {id} deleted.")
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    app.run(debug=True)