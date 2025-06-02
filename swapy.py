from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Mock database
book_requests = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/request_book', methods=['GET', 'POST'])
def request_book():
    if request.method == 'POST':
        data = {
            'request_id': len(book_requests) + 1,
            'name': request.form['name'],
            'email': request.form['email'],
            'book_title': request.form['bookTitle'],
            'author': request.form['author'],
            'description': request.form['description'],
            'status': 'Pending',
            'date': request.form['requestOn']
        }
        book_requests.append(data)
        return redirect(url_for('confirmation'))
    return render_template('request_book.html')

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

@app.route('/admin_requests')
def admin_requests():
    return render_template('admin_requests.html', requests=book_requests)

@app.route('/update_status/<int:request_id>/<string:action>')
def update_status(request_id, action):
    for req in book_requests:
        if req['request_id'] == request_id:
            if action == 'approve':
                req['status'] = 'Approved'
            elif action == 'deny':
                req['status'] = 'Denied'
            elif action == 'delete':
                book_requests.remove(req)
            break
    return redirect(url_for('admin_requests'))

if __name__ == '__main__':
    app.run(debug=True)