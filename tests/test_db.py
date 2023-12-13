import pytest

from src.db import db
from src import create_app
from sqlalchemy import text


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'postgresql://postgres:postgres@localhost:5432/vpn_admin',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_db_connection(app):
    with app.app_context():
        assert db.session is not None
        result = db.session.execute(text("SELECT 1")).fetchone()
        assert result is not None and result[0] == 1
