from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trainee.db'
db = SQLAlchemy(app)
Migrate(app,db)

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
        return f"<User {self.user_name}>"
    
with app.app_context():
    db.create_all()

@app.route("/", methods=['POST', 'GET'])
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)