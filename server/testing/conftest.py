# server/testing/conftest.py
import pytest
from ..app import app
from ..models import db, Episode, Guest, Appearance


@pytest.fixture(scope='session')
def test_app():
    # Configure the app for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Use in-memory SQLite for fast tests
    
    with app.app_context():
        # Create tables and seed data
        db.create_all()
        seed_test_data()
        yield app
        db.drop_all()

@pytest.fixture(scope='function')
def client(test_app):
    return test_app.test_client()

def seed_test_data():
    # Clear all existing data
    Appearance.query.delete()
    Episode.query.delete()
    Guest.query.delete()

    # Create sample data for testing
    e1 = Episode(date="1/11/2000", number=1)
    e2 = Episode(date="1/12/2000", number=2)
    
    g1 = Guest(name="Tom Hanks", occupation="Actor")
    g2 = Guest(name="Madonna", occupation="Singer")

    db.session.add_all([e1, e2, g1, g2])
    db.session.commit()

    a1 = Appearance(rating=5, episode=e1, guest=g1)
    a2 = Appearance(rating=3, episode=e1, guest=g2)
    a3 = Appearance(rating=1, episode=e2, guest=g1)

    db.session.add_all([a1, a2, a3])
    db.session.commit()

# Expose the models for easier imports in test files
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