from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates
from datetime import datetime, timezone
import re
import logging


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trainee.db'
app.logger.setLevel(logging.INFO)

db = SQLAlchemy(app)
Migrate(app,db)

class Trainee(db.Model):
    __tablename__ = 'trainees'

    id = db.Column(db.Integer, primary_key=True) # not included in init because the ID will be assigned
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    user_name = db.Column(db.String(25), unique=True, nullable=False, index=True)
    password = db.Column(db.Text, nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    registration_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    profile_photo_link = db.Column(db.String(255))

    def __init__(self, **kwargs):
            super(Trainee, self).__init__(**kwargs)

    def __repr__(self):
            return f"<Trainee {self.user_name} ({self.email})>"

    @validates('password')
    def validate_password(self, key, password):
        if not self.passwordValidation(password):
            raise ValueError('Password must contain at least one uppercase letter, one lowercase letter, and end with a number.')
        return generate_password_hash(password) 

    def passwordValidation(self, PWD):
        regex_list = [r'[A-Z]', r'[a-z]', r'[0-9]$']
        if all(re.search(reg, PWD) for reg in regex_list):
            return True
        return False
                
    def check_password(self, password):
        return check_password_hash(self.password, password)

with app.app_context():
    db.create_all()

@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
         pass
    return render_template('login.html')


@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            user_name = request.form.get('user_name')
            password = request.form.get('password') # TODO: add password validation + encryption
            confirm_password = request.form.get('confirm_password')
            if password != confirm_password:
                raise ValueError('Passwords do not match.')
            sex = request.form.get('sex')
            height = float(request.form.get('feet')) + float(request.form.get('inches'))/12
            weight = float(request.form.get('weight'))
            profile_photo_link = request.form.get('profile_photo_link')

            print(f"--- Form Submission ---")

            trainee = Trainee(
                name = name,
                email = email,
                user_name = user_name,
                password = password,
                sex = sex,
                height = height,
                weight = weight,
                profile_photo_link = 'profile_photo_link' # TODO: fix photo loading on form
            )
            with app.app_context():
                db.session.add(trainee)
                db.session.commit()
                app.logger.info('User {user_name} registered.')
                all_trainees = Trainee.query.all()
                print(all_trainees)
            return render_template('login.html')

        except ValueError as e:
             app.logger.error(f"Registration failed: {e}")
             return f"Registration Error: {e}", 400
        
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True, port=5001)