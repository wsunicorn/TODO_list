import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not email:
            error = 'Email is required.'
        elif not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                # Tìm ID nhỏ nhất chưa tồn tại, bỏ qua admin
                missing_id = db.execute("""
                    SELECT MIN(t1.id + 1) 
                    FROM user t1 
                    LEFT JOIN user t2 ON t1.id + 1 = t2.id 
                    WHERE t2.id IS NULL AND t1.role = 'user'
                """).fetchone()[0]

                # Nếu chưa có user nào, bắt đầu từ 1
                next_id = 1 if missing_id is None else missing_id

                # Chèn user mới, đảm bảo admin không bị ảnh hưởng
                db.execute(
                    "INSERT INTO user (id, email, username, password, role) VALUES (?, ?, ?, ?, ?)",
                    (next_id, email, username, generate_password_hash(password), 'user')
                )
                db.commit()
                return redirect(url_for('auth.login'))

            except db.IntegrityError:
                error = f"Email {email} hoặc User {username} đã tồn tại."

        flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        identifier = request.form['identifier']  # Nhận email hoặc username
        password = request.form['password']
        db = get_db()
        error = None

        # Tìm user bằng email hoặc username
        user = db.execute(
            'SELECT * FROM user WHERE email = ? OR username = ?', (identifier, identifier)
        ).fetchone()

        if user is None or not check_password_hash(user['password'], password):
            error = 'Sai email/tên đăng nhập hoặc mật khẩu.'
        elif user['blocked']:  # Kiểm tra nếu tài khoản bị block
            error = 'Tài khoản của bạn đã bị khóa. Vui lòng liên hệ quản trị viên.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            # Chuyển hướng theo vai trò
            return redirect(url_for('admin.index' if user['role'] == 'admin' else 'index'))

        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view