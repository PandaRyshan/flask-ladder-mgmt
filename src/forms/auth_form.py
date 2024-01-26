from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from werkzeug.security import check_password_hash
from src.models.verification_code import VerificationCode
from src.models.user import User


class SignupForm(FlaskForm):

    def validate_invite_code(form, field):
        """
        Validate invite code, check if it exists in the database.
        And this validator will be called after all other validators.

        Raises:
            validators.ValidationError: This error won't stop other validators.
        """
        code = VerificationCode.query.filter_by(code=field.data).first()
        if code is None:
            raise validators.ValidationError("Invalid invite code.")
        if code.used:
            raise validators.ValidationError("Invite code has been used.")
        if code.expires_at < datetime.utcnow():
            raise validators.ValidationError("Invite code has expired.")
        

    def validate_email(form, field):
        """
        Validate email, check if it exists in the database.
        And this validator will be called after all other validators.

        Raises:
            validators.ValidationError: This error won't stop other validators.
        """
        if User.query.filter_by(email=field.data).first() is not None:
            raise validators.ValidationError("Email is already registered.")


    invite_code = StringField(
        "Invite Code", [validators.DataRequired()], name="inviteCode")
    email = StringField(
        "Email", [validators.DataRequired(), validators.Email()])
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


class SigninForm(FlaskForm):
    def validate_email(form, field):
        user = User.query.filter_by(email=field.data).first()
        if user is None or check_password_hash(user.password, form.password.data):
            raise validators.ValidationError("Email or Password is incorrect.")
        if user.active is False:
            raise validators.ValidationError("Please verify your email address.")
    email = StringField("Email", [validators.DataRequired(), validators.Email()])
    password = PasswordField("Password", validators=[validators.DataRequired()])
