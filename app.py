from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/ramabook.sqlite'
db = SQLAlchemy(app)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    text = db.Column(db.String(500), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        text = request.form['comment']
        if username and text:
            new_comment = Comment(username=username, text=text)
            db.session.add(new_comment)
            db.session.commit()
            flash('Comment added successfully!', 'success')
        else:
            flash('Both fields are required!', 'danger')
        return redirect(url_for('index', username=username))

    username = request.args.get('username', '')
    comments = Comment.query.order_by(Comment.id.desc()).all()
    return render_template('index.html', comments=comments, username=username)

@app.route('/delete_comment/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
