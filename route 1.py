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
    return render_template('request_book.
