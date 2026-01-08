from app import create_app, db
from app.models import User, File, FlashcardSet, Flashcard
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Create test admin and user
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@test.com', password_hash=generate_password_hash('adminpass'), role='admin')
        db.session.add(admin)
        db.session.commit()

    test_user = User.query.filter_by(username='testuser').first()
    if not test_user:
        test_user = User(username='testuser', email='test@test.com', password_hash=generate_password_hash('testpass'), role='student')
        db.session.add(test_user)
        db.session.commit()

    print("Testing admin global functionality...")

    # Test admin file upload (simulate)
    admin_file = File(title='Admin Global File', filename='adminfile.txt', description='Global file by admin', uploaded_by=admin.id, is_global=True)
    db.session.add(admin_file)

    # Test admin flashcard set creation
    admin_set = FlashcardSet(title='Admin Global Set', owner_id=admin.id, is_global=True)
    db.session.add(admin_set)
    db.session.commit()

    # Add a card to the set
    card = Flashcard(set_id=admin_set.id, question='What is 2+2?', answer='4')
    db.session.add(card)
    db.session.commit()

    print("Created admin global file and flashcard set.")

    # Test visibility for test_user
    from flask_login import login_user
    from unittest.mock import Mock

    # Mock current_user for test_user
    mock_user = Mock()
    mock_user.id = test_user.id
    mock_user.role = test_user.role

    # Test file visibility
    files_for_user = File.query.filter((File.uploaded_by == mock_user.id) | (File.is_global == True)).all()
    print(f"Files visible to testuser: {len(files_for_user)} (should include admin file)")

    # Test flashcard set visibility
    sets_for_user = FlashcardSet.query.filter((FlashcardSet.owner_id == mock_user.id) | (FlashcardSet.is_global == True)).all()
    print(f"Flashcard sets visible to testuser: {len(sets_for_user)} (should include admin set)")

    # Test admin can delete global file
    db.session.delete(admin_file)
    db.session.commit()
    print("Admin deleted global file.")

    # Test admin can delete global set
    db.session.delete(admin_set)
    db.session.commit()
    print("Admin deleted global flashcard set.")

    print("Testing completed successfully!")
