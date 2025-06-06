@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        request_id = request.form['request_id']
        new_status = request.form['status']
        cursor.execute("UPDATE book_requests SET status = ? WHERE request_id = ?", (new_status, request_id))
        conn.commit()

    cursor.execute("SELECT * FROM book_requests")
    requests = [
        {
            'request_id': row[0],
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