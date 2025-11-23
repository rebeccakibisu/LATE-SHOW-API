import pytest
from sqlalchemy.exc import IntegrityError

def test_episode_guest_appearance_relationships(test_app, database, episode_model, guest_model, appearance_model):
    with test_app.app_context():
        e1 = episode_model.query.filter_by(number=1).first()
        g1 = guest_model.query.filter_by(name="Tom Hanks").first()

        # Episode -> Appearances
        assert len(e1.appearances) == 2

        # Appearance -> Guest
        assert e1.appearances[0].guest == g1

        # Guest -> Appearances
        assert len(g1.appearances) == 2

        # Serialization should include appearances
        e1_dict = e1.to_dict()
        assert 'appearances' in e1_dict

        # Serialization should NOT include full episode inside appearances
        assert 'episode' not in e1_dict['appearances'][0]

        # Guest serialization
        g1_dict = g1.to_dict()
        assert 'appearances' in g1_dict
        assert 'guest' not in g1_dict['appearances'][0]

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
            try:
                appearance_model(rating=rating, episode=e1, guest=g1)
            except ValueError:
                pytest.fail(f"Valid rating {rating} failed validation.")
        else:
            with pytest.raises(ValueError):
                appearance_model(rating=rating, episode=e1, guest=g1)

def test_episode_cascade_delete(test_app, database, episode_model, appearance_model):
    with test_app.app_context():
        initial_appearances = appearance_model.query.count()

        e2 = episode_model.query.filter_by(number=2).first()
        e2_appearance_count = appearance_model.query.filter_by(episode_id=e2.id).count()

        assert e2_appearance_count == 1

        database.session.delete(e2)
        database.session.commit()

        assert episode_model.query.filter_by(number=2).first() is None

        final_appearances = appearance_model.query.count()

        assert final_appearances == initial_appearances - e2_appearance_count
