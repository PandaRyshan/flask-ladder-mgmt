from flask import current_app
from src.models.user import User
from src.models.role import Role
from src.dto.user_dto import UserDTO
from src.extensions.db import db
from sqlalchemy.orm import joinedload
from itsdangerous import URLSafeTimedSerializer, SignatureExpired


def get_all_users():
    return User.query.options(joinedload(User.roles)).order_by(User.created_at).all()


def get_all_roles():
    return Role.query.all()


def create_user(user_dto: UserDTO):
    role_ids = [role_dto.id for role_dto in user_dto.roles]
    user = User(
        name=user_dto.name,
        email=user_dto.email,
        username=user_dto.email,
        password=user_dto.password,
        fs_uniquifier=user_dto.fs_uniquifier,
        roles=Role.query.filter(Role.id.in_(role_ids)).all()
    )

    print(user)
    db.session.add(user)

    token = generate_verification_token(user.email)


def verify_user(email: str):
    user = User.query.filter_by(email=email).first()
    user.is_verified = True
    db.session.add(user)
    return user.name


def reset_password():
    pass


def generate_verification_token(email):
    secret_key = current_app.config["SECRET_KEY"]
    salt = current_app.config["SECURITY_PASSWORD_SALT"]
    serializer = URLSafeTimedSerializer(secret_key)
    return serializer.dumps(email, salt=salt)


def verify_token(saved_token, expiration=10800):
    secret_key = current_app.config["SECRET_KEY"]
    salt = current_app.config["SECURITY_PASSWORD_SALT"]
    serializer = URLSafeTimedSerializer(secret_key)
    try:
        email = serializer.loads(saved_token, salt=salt, max_age=expiration)
    except SignatureExpired:
        return False
    return email
