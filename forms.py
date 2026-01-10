from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired(), Email()])
    user_name = StringField(validators=[DataRequired()])
    sex = StringField(validators=[DataRequired()])
    height = StringField(validators=[DataRequired()])
    weight = StringField(validators=[DataRequired()])
    profile_photo_link = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo(password)])
