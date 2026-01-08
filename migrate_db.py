from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    # Add is_global column to file table if it doesn't exist
    try:
        with db.engine.connect() as conn:
            conn.execute(text('ALTER TABLE file ADD COLUMN is_global BOOLEAN DEFAULT FALSE'))
            conn.commit()
        print("Added is_global column to file table")
    except Exception as e:
        print(f"Column is_global already exists in file table or error: {e}")

    # Add is_global column to flashcard_set table if it doesn't exist
    try:
        with db.engine.connect() as conn:
            conn.execute(text('ALTER TABLE flashcard_set ADD COLUMN is_global BOOLEAN DEFAULT FALSE'))
            conn.commit()
        print("Added is_global column to flashcard_set table")
    except Exception as e:
        print(f"Column is_global already exists in flashcard_set table or error: {e}")

    print("Migration completed!")
