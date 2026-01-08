from flask import Flask, render_template, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
import os

db = SQLAlchemy()
login_manager = LoginManager()
bootstrap = Bootstrap()

def unauthorized_handler():
    return render_template('unauthorized.html')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'devsecret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/data.db'
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, '..', 'uploads')
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    # Set unauthorized handler
    login_manager.unauthorized_callback = unauthorized_handler

    with app.app_context():
        from . import models, auth, files, flashcards
        db.create_all()
        app.register_blueprint(auth.bp)
        app.register_blueprint(files.bp, url_prefix='/files')
        app.register_blueprint(flashcards.bp, url_prefix='/flashcards')

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    return app
