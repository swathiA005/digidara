from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory store for book requests (for demo)
book_requests = []

# Home / Student Verification Page
@app.route('/')
def home():
    return render_template('index.html')  # your student verification form

# Handle student verification
@app.route('/verify', methods=['POST'])
def verify_student():
    reg_no = request.form.get('reg_no')
    department = request.form.get('department')
    year = request.form.get('year')

    # Basic check — in real case, verify with database
    if reg_no and department and year:
        return redirect(url_for('request_book', reg_no=reg_no))
    else:
        return "Verification Failed. Please fill all fields."

# Book Request Form Page
@app.route('/request_book')
def request_book():
    return render_template('request_book.html')

# Handle Book Request Submission
@app.route('/submit_request', methods=['POST'])
def submit_request():
    request_id = request.form.get('requestId')
    name = request.form.get('name')
    email = request.form.get('email')
    book_title = request.form.get('bookTitle')
    author = request.form.get('author')
    description = request.form.get('description')
    status = request.form.get('status')
    request_on = request.form.get('requestOn')

    book_requests.append({
        'request_id': request_id,
        'name': name,
        'email': email,
        'book_title': book_title,
        'author': author,
        'description': description,
        'status': status,
        'request_on': request_on
    })

    return redirect(url_for('confirmation'))

# Confirmation Page
@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

# Admin Panel Page
@app.route('/admin_requests')
def admin_requests():
    return render_template('admin_requests.html', requests=book_requests)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)