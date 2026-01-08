from app import create_app, db
from app.models import File, FlashcardSet

app = create_app()

with app.app_context():
    # Test if is_global column exists
    try:
        files = File.query.filter_by(is_global=True).all()
        print("File.is_global column exists")
    except Exception as e:
        print(f"File.is_global column error: {e}")

    try:
        sets = FlashcardSet.query.filter_by(is_global=True).all()
        print("FlashcardSet.is_global column exists")
    except Exception as e:
        print(f"FlashcardSet.is_global column error: {e}")

    print("Database check completed")
