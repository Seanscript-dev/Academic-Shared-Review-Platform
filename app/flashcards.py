from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from .models import FlashcardSet, Flashcard
from . import db

bp = Blueprint('flashcards', __name__)

@bp.route('/sets')
@login_required
def sets():
    if current_user.role == 'admin':
        sets = FlashcardSet.query.all()
    else:
        sets = FlashcardSet.query.filter((FlashcardSet.owner_id == current_user.id) | (FlashcardSet.is_global == True)).all()
    return render_template('flashcards/sets.html', sets=sets)

@bp.route('/sets/create', methods=['POST'])
@login_required
def create_set():
    title = request.form.get('title')
    is_global = current_user.role == 'admin'
    if not title:
        flash('Set title is required', 'error')
        return redirect(url_for('flashcards.sets'))

    new_set = FlashcardSet(title=title, owner_id=current_user.id, is_global=is_global)
    db.session.add(new_set)
    db.session.commit()
    flash('Flashcard set created successfully!', 'success')
    return redirect(url_for('flashcards.sets'))

@bp.route('/sets/<int:set_id>')
@login_required
def view_set(set_id):
    set_obj = FlashcardSet.query.get_or_404(set_id)
    if set_obj.owner_id != current_user.id and not set_obj.is_global and current_user.role != 'admin':
        abort(403)

    return render_template('flashcards/set_detail.html', set=set_obj)

@bp.route('/sets/<int:set_id>/add_card', methods=['GET', 'POST'])
@login_required
def add_card(set_id):
    set_obj = FlashcardSet.query.get_or_404(set_id)
    if set_obj.owner_id != current_user.id and current_user.role != 'admin':
        abort(403)

    if request.method == 'POST':
        question = request.form.get('question')
        answer = request.form.get('answer')

        if not question or not answer:
            flash('Both question and answer are required', 'error')
            return redirect(url_for('flashcards.add_card', set_id=set_id))

        new_card = Flashcard(set_id=set_id, question=question, answer=answer)
        db.session.add(new_card)
        db.session.commit()
        flash('Flashcard added successfully!', 'success')
        return redirect(url_for('flashcards.view_set', set_id=set_id))

    return render_template('flashcards/edit_card.html', set=set_obj, card=None, action='Add')

@bp.route('/sets/<int:set_id>/edit_card/<int:card_id>', methods=['GET', 'POST'])
@login_required
def edit_card(set_id, card_id):
    set_obj = FlashcardSet.query.get_or_404(set_id)
    card = Flashcard.query.get_or_404(card_id)

    if set_obj.owner_id != current_user.id or card.set_id != set_id:
        abort(403)

    if request.method == 'POST':
        question = request.form.get('question')
        answer = request.form.get('answer')

        if not question or not answer:
            flash('Both question and answer are required', 'error')
            return redirect(url_for('flashcards.edit_card', set_id=set_id, card_id=card_id))

        card.question = question
        card.answer = answer
        db.session.commit()
        flash('Flashcard updated successfully!', 'success')
        return redirect(url_for('flashcards.view_set', set_id=set_id))

    return render_template('flashcards/edit_card.html', set=set_obj, card=card, action='Edit')

@bp.route('/sets/<int:set_id>/delete_card/<int:card_id>', methods=['POST'])
@login_required
def delete_card(set_id, card_id):
    set_obj = FlashcardSet.query.get_or_404(set_id)
    card = Flashcard.query.get_or_404(card_id)

    if (set_obj.owner_id != current_user.id and current_user.role != 'admin') or card.set_id != set_id:
        abort(403)

    db.session.delete(card)
    db.session.commit()
    flash('Flashcard deleted successfully!', 'success')
    return redirect(url_for('flashcards.view_set', set_id=set_id))

@bp.route('/sets/<int:set_id>/delete', methods=['POST'])
@login_required
def delete_set(set_id):
    set_obj = FlashcardSet.query.get_or_404(set_id)
    if set_obj.owner_id != current_user.id:
        abort(403)

    db.session.delete(set_obj)
    db.session.commit()
    flash('Flashcard set deleted successfully!', 'success')
    return redirect(url_for('flashcards.sets'))

@bp.route('/sets/<int:set_id>/study')
@login_required
def study_set(set_id):
    set_obj = FlashcardSet.query.get_or_404(set_id)
    if set_obj.owner_id != current_user.id and current_user.role != 'admin' and not set_obj.is_global:
        abort(403)

    cards = set_obj.cards
    if not cards:
        flash('This set has no cards to study', 'warning')
        return redirect(url_for('flashcards.view_set', set_id=set_id))

    # Convert to list of dicts for safe JSON serialization
    cards_data = [{"question": card.question, "answer": card.answer} for card in cards]
    return render_template('flashcards/study.html', set=set_obj, cards=cards_data)
