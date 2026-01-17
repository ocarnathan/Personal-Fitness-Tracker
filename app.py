from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from sqlalchemy.orm import validates
from datetime import datetime, timezone
import re
import logging
from forms import RegistrationForm
from utils import save_photo
import os


app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_NAME")
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
        user_name = request.form.get('user_name')
        password = request.form.get('password')

        user = Trainee.query.filter_by(user_name=user_name).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            session['user_name'] = user.user_name
            session['logged_in'] = True
            app.logger.info(f'User {user_name} logged in.')
            return redirect(url_for('dashboard', user_name=user.user_name))
        return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')


@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        height = form.feet.data + form.inches.data / 12
        app.logger.info(f"--- Form Submission ---")
        photo = form.profile_photo_link.data

        try:
            file_name = save_photo(photo, app.instance_path)
            trainee = Trainee(
                name = form.name.data,
                email = form.email.data,
                user_name = form.user_name.data,
                password = form.password.data,
                sex = form.sex.data,
                height = height,
                weight = form.weight.data,
                profile_photo_link = file_name         
                )
            with app.app_context():
                db.session.add(trainee)
                db.session.commit()
                app.logger.info('User {user_name} registered.')
                all_trainees = Trainee.query.all()
                print(all_trainees)
            return redirect('login')
    
        except ValueError as e:
             app.logger.error(f"Registration failed: {e}")
            #  return f"Registration Error: {e}", 400
        return render_template('register.html', form=form, error=form.errors)
    else:
        app.logger.error(f"Registration failed: {form.errors}")
        return render_template('register.html', form=form, error=form.errors)


@app.route("/dashboard/<string:user_name>", methods=['POST', 'GET'])
def dashboard(user_name):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    trainee = Trainee.query.filter_by(user_name=user_name).first()
    return render_template('dashboard.html', trainee=trainee)


if __name__ == "__main__":
    app.run(debug=True, port=5001)