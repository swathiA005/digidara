from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# MySQL Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'book_request'
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/')
def home():
    return render_template('homepage.html')

# Book Request Form
@app.route('/request_book', methods=['POST'])
def request_book():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        title = request.form['bookTitle']
        author = request.form['author']
        description = request.form['description']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''INSERT INTO books (student_name, email, book_title, author, description)VALUES (%s, %s, %s, %s, %s)''', (name, email, title, author, description))
        conn.commit()
        cur.close()
        conn.close()
        return render_template('confirmation.html', name=name)
    return render_template('request_book.html')

@app.route('/verify', methods=['POST'])
def confirmation():
    if request.method == 'POST':
        reg = request.form['reg_no']
        department = request.form['department']
        year = request.form['year']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''INSERT INTO book_request (reg, department, year) VALUES (%s, %s, %s)''', (reg, department, year))
        conn.commit()
        cur.close()
        conn.close()
        return render_template('request_book.html')
    return render_template('confirmation.html')

# Admin Panel
@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        email = request.form['email']
        new_status = request.form['status']
        cursor.execute("UPDATE book_requests SET status = ? WHERE eamil = ?", (new_status, email))
        conn.commit()

    cursor.execute("SELECT * FROM books")
    requests = [
        {
            
            'student_name': row[1],
            'email': row[2],
            'book_title': row[3],
            'author': row[4],
            'status': row[5]
        }
        for row in cursor.fetchall()
    ]
    conn.close()
    return render_template('admin.html', requests=requests)
@app.route('/admin_request')
def admin_request():
    return render_template('admin_requests.html')

if __name__ == '__main__':
    app.run(debug=True)