from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import uuid

app = Flask(__name__)

# In-memory "database"
requests_db = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        reg_no = request.form['reg_no']
        department = request.form['department']
        year = request.form['year']
        return redirect(url_for('request_book', reg_no=reg_no, department=department, year=year))
    return render_template('verify.html')

@app.route('/request_book', methods=['GET', 'POST'])
def request_book():
    if request.method == 'POST':
        req_id = str(uuid.uuid4())[:8]
        request_data = {
            'id': req_id,
            'name': request.form['name'],
            'email': request.form['email'],
            'book_title': request.form['bookTitle'],
            'author': request.form['author'],
            'description': request.form['description'],
            'status': 'Pending',
            'request_on': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        requests_db[req_id] = request_data
        return redirect(url_for('confirmation'))
    return render_template('request_book.html')

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

@app.route('/admin_requests')
def admin_requests():
    return render_template('admin_requests.html', requests=list(requests_db.values()))

@app.route('/admin_action/<req_id>/<action>')
def admin_action(req_id, action):
    if req_id in requests_db:
        if action == 'approve':
            requests_db[req_id]['status'] = 'Approved'
        elif action == 'deny':
            requests_db[req_id]['status'] = 'Denied'
        elif action == 'delete':
            del requests_db[req_id]
    return redirect(url_for('admin_requests'))

if __name__ == '__main__':
    app.run(debug=True)