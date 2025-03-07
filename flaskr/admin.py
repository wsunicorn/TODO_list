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

from flask import request
from werkzeug.security import generate_password_hash

@bp.route('/reset_password/<int:id>', methods=['POST'])
@admin_required
def reset_password(id):
    db = get_db()
    user = db.execute('SELECT * FROM user WHERE id = ?', (id,)).fetchone()

    if not user:
        flash('Người dùng không tồn tại!')
        return redirect(url_for('admin.index'))

    if id == g.user['id']:
        flash('Bạn không thể đặt lại mật khẩu của chính mình!')
        return redirect(url_for('admin.index'))

    new_password = '123456'  # Mật khẩu mặc định sau khi reset
    hashed_password = generate_password_hash(new_password)

    db.execute('UPDATE user SET password = ? WHERE id = ?', (hashed_password, id))
    db.commit()

    flash(f'Mật khẩu của {user["username"]} đã được đặt lại thành "123456".')
    return redirect(url_for('admin.index'))