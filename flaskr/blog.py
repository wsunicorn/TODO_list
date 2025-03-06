from flask import Blueprint, g, redirect, render_template, request, url_for, make_response

from .auth import login_required
from .db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
@login_required
def index():
    db = get_db()
    todos = db.execute(
        'SELECT * FROM todo WHERE user_id = ? ORDER BY id DESC',
        (g.user['id'],)
    ).fetchall()
    return render_template('blog/index.html', todos=todos)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        db = get_db()
        db.execute(
            'INSERT INTO todo (user_id, title) VALUES (?, ?)',
            (g.user['id'], title)
        )
        db.commit()
        return redirect(url_for('index'))
    return render_template('blog/create.html')

@bp.route('/update/<int:id>', methods=('GET', 'POST'))
@login_required
def update(id):
    db = get_db()
    todo = db.execute('SELECT * FROM todo WHERE id = ? AND user_id = ?', (id, g.user['id'])).fetchone()

    if todo is None:
        return redirect(url_for('index'))

    if request.method == 'POST':
        completed = 1 if 'completed' in request.form else 0
        db.execute(
            'UPDATE todo SET completed = ? WHERE id = ?',
            (completed, id)
        )
        db.commit()
        return redirect(url_for('index'))

    return render_template('blog/update.html', todo=todo)

@bp.route('/delete/<int:id>', methods=('POST',))
@login_required
def delete(id):
    db = get_db()
    db.execute('DELETE FROM todo WHERE id = ? AND user_id = ?', (id, g.user['id']))
    db.commit()
    return redirect(url_for('index'))