# server/testing/models_test.py

import pytest
from sqlalchemy.exc import IntegrityError
from server.models import Episode, Guest, Appearance, db

# Test Relationships and Serialization
def test_episode_guest_appearance_relationships(test_app, database, episode_model, guest_model, appearance_model):
    # Verify the relationships are correctly established
    with test_app.app_context():
        e1 = episode_model.query.filter_by(number=1).first()
        g1 = guest_model.query.filter_by(name="Tom Hanks").first()
        
        # Check Episode -> Appearance
        assert len(e1.appearances) == 2
        # Check Appearance -> Guest
        assert e1.appearances[0].guest == g1
        # Check Guest -> Appearance
        assert len(g1.appearances) == 2

        # Check serialization (no infinite recursion)
        e1_dict = e1.to_dict()
        assert 'appearances' in e1_dict
        assert 'episode' not in e1_dict['appearances'][0] # Check Episode serialization rule
        
        g1_dict = g1.to_dict()
        assert 'appearances' in g1_dict
        assert 'guest' not in g1_dict['appearances'][0] # Check Guest serialization rule

# Test Validation
@pytest.mark.parametrize("rating, should_pass", [
    (1, True),
    (5, True),
    (3, True),
    (0, False),
    (6, False),
    ("text", False)
])
def test_appearance_rating_validation(test_app, database, episode_model, guest_model, appearance_model, rating, should_pass):
    with test_app.app_context():
        e1 = episode_model.query.get(1)
        g1 = guest_model.query.get(1)
        
        if should_pass:
            # Test valid rating
            try:
                Appearance(rating=rating, episode=e1, guest=g1)
            except ValueError:
                pytest.fail(f"Valid rating {rating} failed validation.")
        else:
            # Test invalid rating (should raise ValueError)
            with pytest.raises(ValueError):
                Appearance(rating=rating, episode=e1, guest=g1)

# Test Cascade Deletes
def test_episode_cascade_delete(test_app, database, episode_model, appearance_model):
    with test_app.app_context():
        # Get initial counts
        initial_appearances = appearance_model.query.count()
        e2 = episode_model.query.filter_by(number=2).first()
        
        # Check how many appearances belong to episode 2
        e2_appearances_count = appearance_model.query.filter_by(episode_id=e2.id).count()
        assert e2_appearances_count == 1 # Based on seed data
        
        # Delete episode 2
        database.session.delete(e2)
        database.session.commit()
        
        # Check if episode 2 is gone
        assert episode_model.query.filter_by(number=2).first() is None
        
        # Check if its appearances are also deleted (cascade='all, delete-orphan')
        final_appearances = appearance_model.query.count()
        assert final_appearances == initial_appearances - e2_appearances_count