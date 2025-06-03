from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import uuid

app = Flask(__name__)

# In-memory storage of book requests
book_requests = []

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

@app.route('/request', methods=['GET', 'POST'])
def request_book():
    if request.method == 'POST':
        request_id = str(uuid.uuid4())[:8]
        name = request.form['name']
        email = request.form['email']
        title = request.form['bookTitle']
        author = request.form['author']
        description = request.form['description']
        status = "Pending"
        request_on = datetime.now().strftime('%Y-%m-%d')

        book_requests.append({
            'id': request_id,
            'name': name,
            'email': email,
            'title': title,
            'author': author,
            'description': description,
            'status': status,
            'request_on': request_on
        })

        return redirect(url_for('confirmation'))

    return render_template('request_book.html')

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

@app.route('/admin')
def admin_panel():
    return render_template('admin_requests.html', requests=book_requests)

@app.route('/admin/action/<request_id>/<action>')
def admin_action(request_id, action):
    for req in book_requests:
        if req['id'] == request_id:
            if action == 'approve':
                req['status'] = 'Approved'
            elif action == 'deny':
                req['status'] = 'Denied'
            elif action == 'delete':
                book_requests.remove(req)
            break
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    app.run(debug=True)