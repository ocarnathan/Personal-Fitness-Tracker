from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, timezone
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trainee.db'
db = SQLAlchemy(app)
Migrate(app,db)

def passwordValidation(PWD):
    regexCapLetter = r'[A-Z]'
    regexLowLetter = r'[a-z]'
    regexEndNumber = r'[0-9]$'
    regexList = [regexCapLetter, regexLowLetter, regexEndNumber]
    count = 0
    for regex in range(0,3):
        match = re.search(regexList[regex],PWD)
        if match:
            count+=1
    if count == 3:
        return True
    else:
        return False

class Trainee(db.Model):
    id = db.Column(db.Integer, primary_key=True) # not included in init because the ID will be assigned
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    user_name = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    sex = db.Column(db.Text, nullable=False)
    height = db.Column(db.Text, nullable=False)
    weight = db.Column(db.Text, nullable=False)
    registration_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    profile_photo_link = db.Column(db.Text)

    def __init__(self, name, email, user_name, password, sex, height, weight, profile_photo_link):
        self.name = name
        self.email = email
        self.user_name = user_name
        self.password = password
        self.sex = sex
        self.height = height
        self.weight = weight
        self.profile_photo_link = profile_photo_link

    def __repr__(self):
        return f"\nUser: {self.user_name}\nEmail: {self.email}>\nPassword: {self.password}\nSex: {self.sex}\nHeight: {self.height}\nWeight: {self.weight}\nPhoto: {self.profile_photo_link}\n"
    
with app.app_context():
    db.create_all()

@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        user_name = request.form.get('user_name')
        password = request.form.get('password') # TODO: add password validation + encryption
        sex = request.form.get('sex')
        height = request.form.get('height')
        weight = request.form.get('weight')
        profile_photo_link = request.form.get('profile_photo_link')

        print(f"--- Form Submission ---")

        trainee = Trainee(
            name = name,
            email = email,
            user_name = user_name,
            password = password,
            sex = sex,
            height = 'height', # TODO: fix height input on form
            weight = weight,
            profile_photo_link = 'profile_photo_link' # TODO: fix photo loading on form
        )
        with app.app_context():
            db.session.add(trainee)
            db.session.commit()
            all_trainees = Trainee.query.all()
            print(all_trainees)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)