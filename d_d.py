app.route('/admin', methods=['GET', 'POST'])
def admin_requests():
    if request.method == 'POST':
        request_id = request.form['request_id']
        status = request.form['status']
        cur = mysql.connection.cursor()
        cur.execute("UPDATE book_requests SET status = %s WHERE request_id = %s", (status, request_id))
        mysql.connection.commit()

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM book_requests ORDER BY requested_on DESC")
    requests = cur.fetchall()
    return render_template('admin_requests.html', requests=requests)
