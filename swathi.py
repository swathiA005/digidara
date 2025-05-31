from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Store book requests in memory (list)
book_requests = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/request_book', methods=['GET', 'POST'])
def request_book():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        book = request.form['book']
        author = request.form['author']

        # Save the request as a dictionary
        book_requests.append({
            'name': name,
            'email': email,
            'book': book,
            'author': author,
            'status': 'Pending'
        })

        return redirect(url_for('confirmation'))
    return render_template('request_book.html')

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

@app.route('/admin')
def admin():
    return render_template('admin.html', requests=book_requests)

if __name__ == '__main__':
    app.run(debug=True)