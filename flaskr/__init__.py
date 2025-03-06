import shutil  # Thêm thư viện để xóa thư mục session
import os
from flask import Flask, session, redirect, url_for
from flask_session import Session  

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        SESSION_TYPE="filesystem",
        SESSION_PERMANENT=False,
        SESSION_FILE_DIR=os.path.join(app.instance_path, 'flask_session'),
        SESSION_USE_SIGNER=True
    )

    # Xóa tất cả session cũ khi server khởi động lại
    if os.path.exists(app.config['SESSION_FILE_DIR']):
        shutil.rmtree(app.config['SESSION_FILE_DIR'])  # Xóa toàn bộ session cũ
    os.makedirs(app.config['SESSION_FILE_DIR'], exist_ok=True)  # Tạo lại thư mục rỗng

    Session(app)  # Khởi tạo Flask-Session

    from . import db
    db.init_app(app)

    from . import auth, blog, admin
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(admin.bp)

    @app.route('/')
    def home():
        return redirect(url_for('blog.about'))

    if __name__ == '__main__':
        app.run(debug=True)

    return app
