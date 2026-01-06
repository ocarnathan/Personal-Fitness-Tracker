from app import app, db, Trainee
from datetime import datetime, timezone

def test_add_trainee():
    trainee = Trainee(
        name = "Test User",
        email = "Test@gmail.com",
        user_name = "testuser",
        password = "Test12",
        sex = "Male",
        height = 170,
        weight = 70,
        profile_photo_link = "photo.jpg"
    )
    with app.app_context():
        db.session.add(trainee)
        db.session.commit()
        all_trainees = Trainee.query.all()
        print(all_trainees)
        db.session.delete(trainee)
        db.session.commit()

if __name__ == "__main__":
    test_add_trainee()
