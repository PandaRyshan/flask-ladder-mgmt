from datetime import datetime
from flask_security.forms import ConfirmRegisterForm
from wtforms import StringField, validators
from src.models.verification_code import VerificationCode


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
    if code.expires_at < datetime.now():
        raise validators.ValidationError("Invite code has expired.")



class ConfirmRegisterFormExtended(ConfirmRegisterForm):
    invite_code = StringField(
        "Invite Code",
        [validators.DataRequired(), validate_invite_code],
        name="invite_code"
    )
    name = StringField(
        "Name",
        [validators.DataRequired()],
        name="name"
    )
