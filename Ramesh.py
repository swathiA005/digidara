from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'yourpassword'
app.config['MYSQL_DB'] = 'library_db'

mysql = MySQL(app)

# Book Request Form
@app.route('/request', methods=['GET', 'POST'])
def request_book():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        title = request.form['title']
        author = request.form['author']
        description = request.form['description']

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO book_requests (student_name, email, book_title, author, description)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, email, title, author, description))
        mysql.connection.commit()
        return render_template('confirmation.html', name=name)
    return render_template('request_book.html')

# Admin Panel
@app.route('/admin', methods=['GET', 'POST'])
def admin_requests():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        request_id = request.form['request_id']
        status = request.form['status']
        cur.execute("UPDATE book_requests SET status = %s WHERE request_id = %s", (status, request_id))
        mysql.connection.commit()
    cur.execute("SELECT * FROM book_requests ORDER BY requested_on DESC")
    requests = cur.fetchall()
    return render_template('admin_requests.html', requests=requests)

if __name__ == '__main__':
    app.run(debug=True)