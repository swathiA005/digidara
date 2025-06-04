from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS book_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reg_no TEXT,
            department TEXT,
            year TEXT,
            name TEXT,
            email TEXT,
            book_title TEXT,
            author TEXT,
            description TEXT,
            status TEXT DEFAULT 'Pending',
            request_on TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/request_book', methods=['GET', 'POST'])
def request_book():
    if request.method == 'POST':
        reg_no = request.form.get('reg_no')
        department = request.form.get('department')
        year = request.form.get('year')
        name = request.form.get('name')
        email = request.form.get('email')
        book_title = request.form.get('bookTitle')
        author = request.form.get('author')
        description = request.form.get('description')
        request_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO book_requests (
                reg_no, department, year, name, email,
                book_title, author, description, request_on
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (reg_no, department, year, name, email, book_title, author, description, request_on))
        conn.commit()
        conn.close()

        return redirect(url_for('confirmation'))

    return render_template('request_book.html')

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

@app.route('/admin_requests')
def admin_requests():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('SELECT * FROM book_requests ORDER BY request_on DESC')
    requests = c.fetchall()
    conn.close()
    return render_template('admin_requests.html', requests=requests)

@app.route('/admin_action/<int:req_id>/<action>')
def admin_action(req_id, action):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    if action == 'delete':
        c.execute('DELETE FROM book_requests WHERE id = ?', (req_id,))
    elif action in ['approve', 'deny']:
        new_status = 'Approved' if action == 'approve' else 'Denied'
        c.execute('UPDATE book_requests SET status = ? WHERE id = ?', (new_status, req_id))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_requests'))

if __name__ == '__main__':
    app.run(debug=True)