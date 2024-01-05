from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators


class RegistrationForm(FlaskForm):
    invite_code = StringField("Invite Code", [validators.DataRequired()], name="inviteCode")
    email = StringField("Email", [validators.DataRequired(), validators.Email()])
    name = StringField("Name", [validators.DataRequired()])
    password = PasswordField("Password", validators=[
        validators.DataRequired(),
        # password at least 8 length and contains at least one letter and one number 
        validators.length(min=8, max=20, message="Password length must be between 8 and 20"),
        validators.Regexp("(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]+",
                          message="Password must be at least 8 characters long and \
                              contain at least one letter and one number")
    ])
    confirm_password = PasswordField("Confirm Password", validators=[
        validators.DataRequired(), 
        validators.EqualTo("password", message="Passwords must match"),
        ], name="confirmPassword"
    )
