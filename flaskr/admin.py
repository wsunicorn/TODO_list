import functools
from flask import Blueprint, g, redirect, render_template, url_for, flash
from .auth import login_required
from .db import get_db

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        if g.user['role'] != 'admin':
            flash('Bạn không có quyền truy cập trang này.')
            return redirect(url_for('index'))
        return view(**kwargs)
    return wrapped_view

@bp.route('/')
@admin_required
def index():
    db = get_db()
    users = db.execute("SELECT * FROM user WHERE role != 'admin' ORDER BY id").fetchall()
    return render_template('admin/index.html', users=users)

@bp.route('/delete/<int:id>', methods=['POST'])
@admin_required
def delete_user(id):
    db = get_db()
    if id == g.user['id']:
        flash('Bạn không thể xóa chính mình!')
        return redirect(url_for('admin.index'))
    
    db.execute('DELETE FROM todo WHERE user_id = ?', (id,))
    db.execute('DELETE FROM user WHERE id = ?', (id,))
    db.commit()
    flash('User đã được xóa thành công.')
    return redirect(url_for('admin.index'))

@bp.route('/toggle_role/<int:id>', methods=['POST'])
@admin_required
def toggle_role(id):
    db = get_db()
    user = db.execute('SELECT * FROM user WHERE id = ?', (id,)).fetchone()
    
    if id == g.user['id']:
        flash('Bạn không thể thay đổi vai trò của chính mình!')
        return redirect(url_for('admin.index'))
    
    new_role = 'admin' if user['role'] == 'user' else 'user'
    db.execute('UPDATE user SET role = ? WHERE id = ?', (new_role, id))
    db.commit()
    flash(f'Vai trò của {user["username"]} đã được thay đổi thành {new_role}.')
    return redirect(url_for('admin.index'))

@bp.route('/toggle_block/<int:id>', methods=['POST'])
@admin_required
def toggle_block(id):
    db = get_db()
    user = db.execute('SELECT * FROM user WHERE id = ?', (id,)).fetchone()

    if not user:
        flash('Người dùng không tồn tại!')
        return redirect(url_for('admin.index'))

    if id == g.user['id']:
        flash('Bạn không thể block chính mình!')
        return redirect(url_for('admin.index'))

    # Đảo trạng thái block
    new_status = 0 if user['blocked'] else 1
    db.execute('UPDATE user SET blocked = ? WHERE id = ?', (new_status, id))
    db.commit()

    action = "bỏ chặn" if new_status == 0 else "chặn"
    flash(f'{user["username"]} đã bị {action}.')
    return redirect(url_for('admin.index'))
