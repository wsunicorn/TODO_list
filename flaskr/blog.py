from flask import Blueprint, g, redirect, render_template, request, url_for, make_response
from .auth import login_required
from .db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
@login_required
def index():
    db = get_db()
    page = request.args.get('page', 1, type=int)
    per_page = 10  # Số task mỗi trang
    offset = (page - 1) * per_page
    
    todos = db.execute(
        'SELECT * FROM todo WHERE user_id = ? ORDER BY id DESC LIMIT ? OFFSET ?',
        (g.user['id'], per_page, offset)
    ).fetchall()
    
    total_tasks = db.execute(
        'SELECT COUNT(*) FROM todo WHERE user_id = ?', (g.user['id'],)
    ).fetchone()[0]
    total_pages = (total_tasks + per_page - 1) // per_page
    
    response = make_response(render_template('blog/index.html', todos=todos, page=page, total_pages=total_pages))
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        if not title:
            return render_template('blog/create.html', error='Tiêu đề không được để trống.')
        db = get_db()
        db.execute(
            'INSERT INTO todo (user_id, title) VALUES (?, ?)',
            (g.user['id'], title)
        )
        db.commit()
        return redirect(url_for('.index'))
    return render_template('blog/create.html')

@bp.route('/update/<int:id>', methods=('GET', 'POST'))
@login_required
def update(id):
    db = get_db()
    todo = db.execute('SELECT * FROM todo WHERE id = ? AND user_id = ?', (id, g.user['id'])).fetchone()

    if todo is None:
        return redirect(url_for('.index'))

    if request.method == 'POST':
        completed = 1 if 'completed' in request.form else 0
        db.execute(
            'UPDATE todo SET completed = ? WHERE id = ?',
            (completed, id)
        )
        db.commit()
        return redirect(url_for('.index'))

    return render_template('blog/update.html', todo=todo)

@bp.route('/delete/<int:id>', methods=('POST',))
@login_required
def delete(id):
    db = get_db()
    db.execute('DELETE FROM todo WHERE id = ? AND user_id = ?', (id, g.user['id']))
    db.commit()
    return redirect(url_for('.index'))

@bp.route('/delete_multiple', methods=['POST'])
@login_required
def delete_multiple():
    db = get_db()
    data = request.get_json()
    task_ids = data.get('task_ids', [])
    
    try:
        if task_ids == "all":  # Xóa tất cả task của người dùng
            db.execute('DELETE FROM todo WHERE user_id = ?', (g.user['id'],))
            db.commit()
            return '', 200
        elif not task_ids:  # Không có task nào được chọn
            return 'Không có task nào được chọn', 400
        else:  # Xóa các task được chọn
            task_ids = [int(id) for id in task_ids]
            placeholders = ','.join('?' * len(task_ids))
            db.execute(
                f'DELETE FROM todo WHERE id IN ({placeholders}) AND user_id = ?',
                task_ids + [g.user['id']]
            )
            db.commit()
            return '', 200
    except Exception as e:
        db.rollback()
        return f'Lỗi: {str(e)}', 500

@bp.route('/auto_add_tasks', methods=['POST'])
@login_required
def auto_add_tasks():
    db = get_db()
    try:
        # Đếm số task hiện tại của người dùng
        current_count = db.execute(
            'SELECT COUNT(*) FROM todo WHERE user_id = ?', (g.user['id'],)
        ).fetchone()[0]
        
        # Tính số bắt đầu và số kết thúc cho 30 task tiếp theo
        start = current_count + 1
        end = start + 9  # Thêm 30 task
        
        # Tạo 30 task mới
        for i in range(start, end + 1):
            title = f"Công việc mẫu {i}"
            db.execute(
                'INSERT INTO todo (user_id, title, completed) VALUES (?, ?, 0)',
                (g.user['id'], title)
            )
        db.commit()
        return '', 200
    except Exception as e:
        db.rollback()
        return f'Lỗi: {str(e)}', 500