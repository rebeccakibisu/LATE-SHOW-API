import pytest
from server.app import app
from server.models import db, Episode, Guest, Appearance

@pytest.fixture(scope='function')
def test_app():
    # Use a real SQLite file or keep memory — either is fine as long as we recreate per test.
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        # Drop & recreate tables for EVERY test
        db.drop_all()
        db.create_all()
        seed()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(test_app):
    return test_app.test_client()

def seed():
    # Ensure tables are empty
    Appearance.query.delete()
    Episode.query.delete()
    Guest.query.delete()
    db.session.commit()

    # Episodes
    e1 = Episode(date="1/11/2000", number=1)
    e2 = Episode(date="1/12/2000", number=2)

    # Guests
    g1 = Guest(name="Tom Hanks", occupation="Actor")
    g2 = Guest(name="Madonna", occupation="Singer")

    db.session.add_all([e1, e2, g1, g2])
    db.session.commit()

    # Appearances:
    # e1 → 2 appearances
    a1 = Appearance(rating=5, episode=e1, guest=g1)
    a2 = Appearance(rating=3, episode=e1, guest=g2)
    # e2 → 1 appearance
    a3 = Appearance(rating=1, episode=e2, guest=g1)

    db.session.add_all([a1, a2, a3])
    db.session.commit()

@pytest.fixture
def episode_model():
    return Episode

@pytest.fixture
def guest_model():
    return Guest

@pytest.fixture
def appearance_model():
    return Appearance

@pytest.fixture
def database():
    return db
