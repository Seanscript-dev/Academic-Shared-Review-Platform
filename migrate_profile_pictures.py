from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Update all users to have icon9.png as profile picture
    users = User.query.all()
    for user in users:
        user.profile_picture = 'icon9.png'
    db.session.commit()
    print(f"Updated profile pictures for {len(users)} users")
