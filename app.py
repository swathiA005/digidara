from flask import Flask, render_template, request, redirect
import mysql.connector
from datetime import datetime

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
@app.route('/request_book', methods=['GET', 'POST'])
def request_book():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        title = request.form['bookTitle']
        author = request.form['author']
        description = request.form['description']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''INSERT INTO library_db (student_name, email, book_title, author, description, status) 
                       VALUES (%s, %s, %s, %s, %s, 'pending')''', 
                    (name, email, title, author, description))
        conn.commit()
        cur.close()
        conn.close()
        return render_template('confirmation.html', name=name)
    return render_template('request_book.html')

# User view to check request status
@app.route('/check_status', methods=['GET', 'POST'])
def check_status():
    if request.method == 'POST':
        email = request.form['email']
        conn = get_db_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM library_db WHERE email = %s", (email,))
        requests = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('check_status.html', requests=requests)
    return render_template('check_status.html', requests=None)

# Verify Route (Fixed to handle GET and POST)
@app.route('/confirmation', methods=['GET', 'POST'])
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
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        request_id = request.form['request_id']
        new_status = request.form['status']
        expected_date = request.form['expected_date'] if 'expected_date' in request.form else None
        
        update_query = "UPDATE library_db SET status = %s"
        params = [new_status]
        
        # if expected_date:
        #     update_query += ", expected_date = %s"
        #     params.append(expected_date)
            
        update_query += " WHERE request_id = %s"
        params.append(request_id)
        
        cursor.execute(update_query, params)
        conn.commit()

    cursor.execute("SELECT * FROM library_db")
    requests = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('admin_requests.html', requests=requests)

@app.route('/admin_request')
def admin_request():
    return render_template('admin_requests.html')

if __name__ == '__main__':
    app.run(debug=True)