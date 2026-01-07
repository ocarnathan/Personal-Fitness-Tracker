from app import app, db, Trainee
from datetime import datetime, timezone


# constants
NAME = "Test User"
EMAIL = "Test@gmail.com"
USER_NAME = "testuser"
PASSWORD = "Test12"
SEX = "Male"
HEIGHT = 6.16
WEIGHT = 210
PROFILE_PHOTO_LINK = "photo.jpg"

def test_add_trainee():
    trainee = Trainee(
        name=NAME,
        email=EMAIL,
        user_name=USER_NAME,
        password=PASSWORD,
        sex=SEX,
        height=HEIGHT,
        weight=WEIGHT,
        profile_photo_link=PROFILE_PHOTO_LINK
    )
    with app.app_context():
        # db.session.add(trainee)
        # db.session.commit()
        all_trainees = Trainee.query.all()
        print(all_trainees)
        # db.session.delete(trainee)
        for trainee in all_trainees:
            db.session.delete(trainee)
        db.session.commit()

if __name__ == "__main__":
    test_add_trainee()
