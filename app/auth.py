from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from . import db, login_manager
import os
from datetime import datetime

bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('home'))
        flash('Invalid username or password', 'error')
    return render_template('login.html')

@bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('auth.register'))

        user = User(username=username, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    from .models import File, FlashcardSet

    files_count = File.query.filter_by(uploaded_by=current_user.id).count()
    flashcards_count = FlashcardSet.query.filter_by(owner_id=current_user.id).count()
    recent_files = File.query.filter_by(uploaded_by=current_user.id).order_by(File.uploaded_at.desc()).limit(5).all()
    recent_flashcard_sets = FlashcardSet.query.filter_by(owner_id=current_user.id).order_by(FlashcardSet.id.desc()).limit(5).all()
    return render_template('profile.html', files_count=files_count, flashcards_count=flashcards_count, recent_files=recent_files, recent_flashcard_sets=recent_flashcard_sets)
