from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators


class RegistrationForm(FlaskForm):
    invite_code = StringField("Invite Code", [validators.DataRequired()], name="inviteCode")
    email = StringField("Email", [validators.DataRequired(), validators.Email()])
    name = StringField("Name", [validators.DataRequired()])
    password = PasswordField("Password", [validators.DataRequired()])
