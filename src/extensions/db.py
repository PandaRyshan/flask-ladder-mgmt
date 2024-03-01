import click

from datetime import datetime, timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def init(app: Flask):
    db.init_app(app)
    app.cli.add_command(init_db_command)

    @app.teardown_request
    def session_commit(exception=None):
        if exception:
            db.session.rollback()
        db.session.commit()


@click.command("init-db")
@click.option("--drop", is_flag=True, help="Create after drop.")
@with_appcontext
def init_db_command(drop):

    """Clear existing data and create new tables."""
    if drop:
        click.confirm("This operation will delete the database, do you want to continue?", abort=True)
        db.drop_all()
        click.echo("Droped all tables.")

    db.create_all()


    from src.models.verification_code import VerificationCode
    verification_code = VerificationCode(
        code="123456", used=False, created_at=datetime.now(), expires_at=datetime.now() + timedelta(days=365))
    db.session.add(verification_code)

    import uuid
    from src.models.user import User
    from src.models.role import Role
    from werkzeug.security import generate_password_hash
    user = User(
        name="admin",
        email="admin@local.host",
        username="admin@local.host",
        password=generate_password_hash("admin"),
        fs_uniquifier=uuid.uuid4().hex,
        roles=[Role(id=1, name="ADMIN"), Role(id=2, name="USER")]
    )
    db.session.add(user)
    db.session.commit()

    click.echo("Initialized the database.")
