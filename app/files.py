from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory, abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from .models import File
from . import db
import os

bp = Blueprint('files', __name__)

@bp.route('/')
@login_required
def list_files():
    if current_user.role == 'admin':
        files = File.query.all()
    else:
        files = File.query.filter((File.uploaded_by == current_user.id) | (File.is_global == True)).all()
    return render_template('files/list.html', files=files)

@bp.route('/upload', methods=['GET','POST'])
@login_required
def upload():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        file = request.files.get('file')

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            new_file = File(
                title=title,
                filename=filename,
                description=description,
                uploaded_by=current_user.id,
                is_global=current_user.role == 'admin'
            )
            db.session.add(new_file)
            db.session.commit()
            flash('File uploaded successfully!', 'success')
            return redirect(url_for('files.list_files'))

        flash('No file selected', 'error')

    return render_template('files/upload.html')

@bp.route('/view/<int:file_id>')
@login_required
def view_file(file_id):
    file = File.query.get_or_404(file_id)
    if file.uploaded_by != current_user.id:
        abort(403)

    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
    file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0

    # Try to read file content if it's text-based
    content = None
    is_text = False
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read(5000)  # Read first 5000 characters
            is_text = True
    except:
        pass

    return render_template('files/view.html', file=file, file_size=file_size, content=content, is_text=is_text)

@bp.route('/download/<int:file_id>')
@login_required
def download_file(file_id):
    file = File.query.get_or_404(file_id)
    if file.uploaded_by != current_user.id and not file.is_global and current_user.role != 'admin':
        abort(403)

    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)
    if not os.path.exists(file_path):
        flash('File not found on server', 'error')
        return redirect(url_for('files.list_files'))

    return send_from_directory(current_app.config['UPLOAD_FOLDER'], file.filename, as_attachment=True)

@bp.route('/delete/<int:file_id>', methods=['POST'])
@login_required
def delete_file(file_id):
    file = File.query.get_or_404(file_id)
    if file.uploaded_by != current_user.id and current_user.role != 'admin':
        abort(403)

    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)

    # Remove file from filesystem
    if os.path.exists(file_path):
        os.remove(file_path)

    # Remove from database
    db.session.delete(file)
    db.session.commit()

    flash('File deleted successfully!', 'success')
    return redirect(url_for('files.list_files'))
