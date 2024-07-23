from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS comments
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        comment TEXT NOT NULL);''')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        comment = request.form['comment']
        session['username'] = username  # Save username in session
        with sqlite3.connect('database.db') as conn:
            conn.execute('INSERT INTO comments (username, comment) VALUES (?, ?)', (username, comment))
        return redirect(url_for('index'))
    
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT id, username, comment FROM comments ORDER BY id DESC')
        comments = cur.fetchall()
    
    return render_template('index.html', comments=comments, username=session.get('username'))

@app.route('/delete/<int:id>')
def delete_comment(id):
    with sqlite3.connect('database.db') as conn:
        conn.execute('DELETE FROM comments WHERE id = ?', (id,))
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
