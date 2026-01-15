from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, IntegerField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo

class RegistrationForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired(), Email()])
    user_name = StringField(validators=[DataRequired()])
    sex = StringField(validators=[DataRequired()])
    feet = IntegerField(validators=[DataRequired()])
    inches = IntegerField(validators=[DataRequired()])
    weight = FloatField(validators=[DataRequired()])
    # profile_photo_link = FileField()
    profile_photo_link = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    confirm_password = PasswordField(validators=[DataRequired(), EqualTo('password')])
